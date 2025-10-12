# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort, send_file, safe_join
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from models import *
from config import config
from utils import secure_file_upload, validate_registration_range
import random
import os
from datetime import datetime, timedelta
import logging

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(env, config['default']))

# Initialize database
db.init_app(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

with app.app_context():
    db.create_all()


from collections import defaultdict

def distribute_questions(num_people, questions):
    """
    Distribute questions among students such that:
    - Each student gets one question.
    - Questions are distributed as evenly as possible.
    - No two adjacent students get the same question.
    
    Args:
        num_people (int): Number of students
        questions (list): List of question texts
        
    Returns:
        list: List of questions assigned to each student
    """
    if not questions or num_people <= 0:
        return []
    
    # If only one question, everyone gets the same one
    if len(questions) == 1:
        return [questions[0]] * num_people
    
    min_per_question = num_people // len(questions)
    result = [None] * num_people
    question_count = defaultdict(int)
    max_attempts = num_people * 10  # Prevent infinite recursion
    attempts = 0

    for i in range(num_people):
        available = []
        for q in questions:
            # Ensure the question is not the same as the previous student's question
            adjacent_ok = i == 0 or q != result[i - 1]
            # Ensure the question is distributed evenly
            distribution_ok = question_count[q] < min_per_question or (
                all(question_count[other] >= min_per_question for other in questions)
            )
            if adjacent_ok and distribution_ok:
                available.append(q)

        if not available:
            # Fallback: if no valid question is available, use any question except the previous one
            available = [q for q in questions if i == 0 or q != result[i - 1]]
            
        if not available:
            # Last resort: use any question
            available = questions
            
        # Randomly select a question from the available options
        selected = random.choice(available)
        result[i] = selected
        question_count[selected] += 1

    return result

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Validate inputs
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return render_template('login.html')

        # Authenticate against the User table
        try:
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session['logged_in'] = True
                session['username'] = username
                session.permanent = True
                logger.info(f'User {username} logged in successfully')
                flash('Login successful!', 'success')
                return redirect(url_for('create_exam'))
            else:
                logger.warning(f'Failed login attempt for username: {username}')
                flash('Invalid credentials!', 'danger')
        except Exception as e:
            logger.error(f'Error during login: {str(e)}')
            flash('An error occurred during login. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f'User {username} logged out')
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/create_exam', methods=['GET', 'POST'])
def create_exam():
    """Create a new exam."""
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        duration_str = request.form.get('duration', '').strip()
        reg_prefix = request.form.get('reg_prefix', '').strip()
        reg_range = request.form.get('reg_range', '').strip()
        
        # Validate inputs
        if not all([name, duration_str, reg_prefix, reg_range]):
            flash('All fields are required!', 'danger')
            return render_template('create_exam.html', exams=Exam.query.all())
        
        try:
            duration = float(duration_str)
            if duration <= 0 or duration > 24:
                flash('Duration must be between 0 and 24 hours', 'danger')
                return render_template('create_exam.html', exams=Exam.query.all())
        except ValueError:
            flash('Invalid duration format', 'danger')
            return render_template('create_exam.html', exams=Exam.query.all())
        
        # Validate registration range
        success, start, end, error = validate_registration_range(reg_range)
        if not success:
            flash(error, 'danger')
            return render_template('create_exam.html', exams=Exam.query.all())
            
        # Create exam
        try:
            new_exam = Exam(
                name=name,
                duration=duration,
                reg_number_prefix=reg_prefix,
                reg_number_range=reg_range
            )
            db.session.add(new_exam)
            db.session.flush()  # Get the ID without committing
            
            # Create students for the range
            for i in range(start, end + 1):
                reg_number = f"{reg_prefix}{i:03d}" 
                student = Student(
                    registration_number=reg_number,
                    exam_id=new_exam.id
                )
                db.session.add(student)
                
            db.session.commit()
            logger.info(f'Exam "{name}" created with {end-start+1} students by user {session.get("username")}')
            flash(f'Exam "{name}" created with {end-start+1} students!', 'success')
            return redirect(url_for('add_questions', exam_id=new_exam.id))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error creating exam: {str(e)}')
            flash('An error occurred while creating the exam. Please try again.', 'danger')
        
    # Pass all ongoing exams to the template
    try:
        exams = Exam.query.all()
    except Exception as e:
        logger.error(f'Error fetching exams: {str(e)}')
        exams = []
        flash('Error loading exams', 'warning')
        
    return render_template('create_exam.html', exams=exams)

@app.route('/add_questions/<int:exam_id>', methods=['GET', 'POST'])
def add_questions(exam_id):
    """Add questions to an exam."""
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
        
    exam = Exam.query.get_or_404(exam_id)
    
    if request.method == 'POST':
        question_number = request.form.get('question_number', '').strip()
        question_text = request.form.get('question_text', '').strip()
        
        # Validate inputs
        if not question_number or not question_text:
            flash('Both question number and text are required!', 'danger')
        else:
            try:
                # Convert question_number to integer
                q_num = int(question_number)
                
                if q_num <= 0:
                    flash('Question number must be positive!', 'danger')
                elif len(question_text) > 5000:
                    flash('Question text is too long (max 5000 characters)!', 'danger')
                else:
                    # Check if this question number already exists for this exam
                    existing_question = Question.query.filter_by(
                        exam_id=exam_id, 
                        question_number=q_num
                    ).first()
                    
                    if existing_question:
                        flash(f'Question number {q_num} already exists for this exam!', 'danger')
                    else:
                        new_question = Question(
                            question_number=q_num,
                            question_text=question_text,
                            exam_id=exam_id
                        )
                        db.session.add(new_question)
                        db.session.commit()
                        logger.info(f'Question {q_num} added to exam {exam_id} by user {session.get("username")}')
                        flash('Question added successfully!', 'success')
            except ValueError:
                flash('Question number must be an integer!', 'danger')
            except Exception as e:
                db.session.rollback()
                logger.error(f'Error adding question: {str(e)}')
                flash('An error occurred while adding the question.', 'danger')
        
    # Get all questions for this exam
    try:
        questions = Question.query.filter_by(exam_id=exam_id).order_by(Question.question_number).all()
    except Exception as e:
        logger.error(f'Error fetching questions: {str(e)}')
        questions = []
        flash('Error loading questions', 'warning')
    
    return render_template('add_questions.html', exam=exam, questions=questions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_number = request.form.get('reg_number')
        exam_id = request.form.get('exam_id')
        current_ip = request.remote_addr
        exam = Exam.query.get_or_404(exam_id)
        # chexk exam is ended
        if exam.is_ended:
            flash('The exam has ended. Registration is not allowed.', 'danger')
            return redirect(url_for('register'))
        # Find the student
        student = Student.query.filter_by(
            registration_number=reg_number,
            exam_id=exam_id
        ).first()

        if student:
            # Check if the student has already submitted their answer
            if student.submitted_file:
                flash('You have already submitted your answer. Login is not allowed.', 'danger')
                return redirect(url_for('register'))  # Redirect back to the registration page

            # Check if the student already has an IP address and it's different
            if student.ip_address and student.ip_address != current_ip:
                flash('Please login from your registered PC!', 'danger')
            else:
                # Record IP address (only if not previously set)
                if not student.ip_address:
                    student.ip_address = current_ip
                    db.session.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('student_exam', student_id=student.id))
        else:
            flash('Invalid registration number or exam ID!', 'danger')

    exams = Exam.query.all()
    return render_template('register.html', exams=exams)

@app.route('/stop_exam', methods=['POST'])
def stop_exam():
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))

    exam_id = request.form.get('exam_id')
    exam = Exam.query.get_or_404(exam_id)
    
    # Mark the exam as ended
    exam.is_ended = True
    db.session.commit()
    
    flash(f'Exam "{exam.name}" has been stopped!', 'success')
    return redirect(url_for('exam_details', exam_id=exam_id))

@app.route('/start_exam', methods=['GET', 'POST'])
def start_exam():
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        
        # Get all questions for this exam
        exam_questions = Question.query.filter_by(exam_id=exam_id).all()
        
        if not exam_questions:
            flash('No questions available for this exam!', 'danger')
            return redirect(url_for('add_questions', exam_id=exam_id))
            
        # Get all students for this exam
        students = Student.query.filter_by(exam_id=exam_id).all()
        exam = Exam.query.get(exam_id)
        exam.is_started = True

        # Prepare question texts for random allocation
        question_texts = [q.question_text for q in exam_questions]
        num_students = len(students)

        # Use the custom function to distribute questions
        distributed_questions = distribute_questions(num_students, question_texts)
        print(distributed_questions)
        # Assign questions to students
        for student, question in zip(students, distributed_questions):
            student.set_question(question)
              
        db.session.commit()
        flash(f'Exam "{exam.name}" started and questions allocated to {len(students)} students!', 'success')
        return redirect(url_for('exam_details', exam_id=exam_id))
        
    exams = Exam.query.all()
    return render_template('start_exam.html', exams=exams)  
@app.route('/student_exam/<int:student_id>', methods=['GET', 'POST'])
def student_exam(student_id):
    """Handle student exam interface and submission."""
    student = Student.query.get_or_404(student_id)
    exam = Exam.query.get_or_404(student.exam_id)

    # Check if the student session is already closed
    if student.submitted_file:
        flash('You have already submitted your answer. Further edits are not allowed.', 'warning')
        return redirect(url_for('register'))
        
    # Check if the exam has ended
    if exam.is_ended:
        flash('The exam has ended.', 'danger')
        return redirect(url_for('register'))
        
    # Handle file upload
    if request.method == 'POST':
        uploaded_file = request.files.get('answer_file')
        
        if not uploaded_file or uploaded_file.filename == '':
            flash('Please upload a valid file!', 'danger')
        else:
            # Save the file in a directory structure: uploads/exam_id/registration_number/
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(exam.id), student.registration_number)
            
            success, file_path, error = secure_file_upload(uploaded_file, upload_folder)
            
            if success:
                try:
                    # Mark the student's session as closed
                    student.submitted_file = file_path
                    db.session.commit()
                    logger.info(f'Student {student.registration_number} submitted file for exam {exam.id}')
                    flash('Answer submitted successfully! You cannot make further changes.', 'success')
                    return redirect(url_for('register'))
                except Exception as e:
                    db.session.rollback()
                    logger.error(f'Error saving submission: {str(e)}')
                    flash('An error occurred while saving your submission.', 'danger')
            else:
                flash(error, 'danger')

    # Get the student's assigned question
    questions = student.get_question()
    return render_template('student_exam.html', student=student, exam=exam, questions=questions)

@app.route('/exam/start', methods=['POST'])
def start_exam_student():
    data = request.get_json()
    student_id = data.get('student_id')
    exam_id = data.get('exam_id')
    exam = Exam.query.get_or_404(exam_id)
    # Check if the exam has Ended
    if exam.is_ended:
        return jsonify({'error': 'The exam has ended.'}), 400
    # Check if the session already exists
    session = ExamSession.query.filter_by(student_id=student_id, exam_id=exam_id).first()

    if session:
        # Calculate remaining time
        elapsed_time = (datetime.now() - session.start_time).total_seconds()
        remaining_time = max(0, session.duration - elapsed_time)
    else:
        # Create a new session
        exam = Exam.query.get(exam_id)
        duration = int(exam.duration * 60 * 60)  # Convert hours to seconds
        session = ExamSession(
            student_id=student_id,
            exam_id=exam_id,
            start_time=datetime.now(),
            duration=duration
        )
        db.session.add(session)
        db.session.commit()
        remaining_time = duration

    return jsonify({'remaining_time': remaining_time})



@app.route('/preview_answer/<path:file_path>')
def preview_answer(file_path):
    """
    Serve the file for preview or download.
    """
    try:
        # Ensure file_path is not absolute
        if os.path.isabs(file_path):
            abort(400, "Invalid file path")

        # Base directory where submissions are stored
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
        # Safely join the base directory with the requested file path
        full_path = safe_join(base_dir, file_path)

        # Check if the file exists
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            abort(404)  # File not found

        # Check if the request is for preview or download
        if request.args.get('download') == 'true':
            # Serve the file as a download
            return send_file(full_path, as_attachment=True)

        # Serve the file content for preview (only for text files)
        text_extensions = ['.txt', '.py', '.html', '.css', '.js', '.json', '.md']
        _, ext = os.path.splitext(full_path)
        if ext.lower() in text_extensions:
            with open(full_path, 'r') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/plain'}

        # If the file is not a text file, return an error
        return "Preview not supported for this file type.", 400

    except (ValueError, TypeError):
        abort(404)  # Invalid file path
        

@app.route('/exam/<int:exam_id>', methods=['GET'])
def exam_details(exam_id):
    # Fetch the exam details
    exam = Exam.query.get_or_404(exam_id)

    # Fetch all students for this exam
    students = Student.query.filter_by(exam_id=exam_id).all()

    # Prepare the data to pass to the template
    student_data = []
    for student in students:
        allocated_question = student.allocated_questions  # Single question as a string
        submission_status = bool(student.submitted_file)  # Check if the student has submitted a file

        # Handle the case where submitted_file is None
        if student.submitted_file:
            submitted_file = os.path.relpath(student.submitted_file, app.config['UPLOAD_FOLDER'])
        else:
            submitted_file = None  # Or set to an empty string ""

        student_data.append({
            'registration_number': student.registration_number,
            'ip_address': student.ip_address,
            'allocated_question': allocated_question,
            'is_submitted': submission_status,
            'submitted_file': submitted_file  # Use the processed value
        })

    return render_template('exam_details.html', exam=exam, students=student_data)

if __name__ == '__main__':
    app.run(debug=True)