# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify , abort, send_file, safe_join

from models import *
import random
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (in a real app, check against database)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('create_exam'))
        else:
            flash('Invalid credentials!', 'danger')
            
    return render_template('login.html')

@app.route('/create_exam', methods=['GET', 'POST'])
def create_exam():
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        duration = float(request.form.get('duration'))
        reg_prefix = request.form.get('reg_prefix')
        reg_range = request.form.get('reg_range')
        
        # Validate inputs
        try:
            start, end = map(int, reg_range.split('-'))
            if start >= end:
                flash('Range start must be less than end', 'danger')
                return render_template('create_exam.html', exams=Exam.query.all())
        except ValueError:
            flash('Invalid range format. Use start-end (e.g., 1-10)', 'danger')
            return render_template('create_exam.html', exams=Exam.query.all())
            
        # Create exam
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
        flash(f'Exam "{name}" created with {end-start+1} students!', 'success')
        return redirect(url_for('add_questions', exam_id=new_exam.id))
        
    # Pass all ongoing exams to the template
    exams = Exam.query.all()
    return render_template('create_exam.html', exams=exams)

@app.route('/add_questions/<int:exam_id>', methods=['GET', 'POST'])
def add_questions(exam_id):
    if not session.get('logged_in'):
        flash('Please login first!', 'warning')
        return redirect(url_for('login'))
        
    exam = Exam.query.get_or_404(exam_id)
    
    if request.method == 'POST':
        question_number = request.form.get('question_number')
        question_text = request.form.get('question_text')
        
        # Validate inputs
        if not question_number or not question_text:
            flash('Both question number and text are required!', 'danger')
        else:
            try:
                # Convert question_number to integer
                q_num = int(question_number)
                
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
                    flash('Question added successfully!', 'success')
            except ValueError:
                flash('Question number must be an integer!', 'danger')
        
    # Get all questions for this exam
    questions = Question.query.filter_by(exam_id=exam_id).order_by(Question.question_number).all()
    
    return render_template('add_questions.html', exam=exam, questions=questions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_number = request.form.get('reg_number')
        exam_id = request.form.get('exam_id')
        current_ip = request.remote_addr

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
        
        # Assign random questions to each student
        for student in students:
            selected_question = random.choice(question_texts)
            student.set_question(selected_question)
              
        db.session.commit()
        flash(f'Exam "{exam.name}" started and questions allocated to {len(students)} students!', 'success')
        return redirect(url_for('exam_details', exam_id=exam_id))
        
    exams = Exam.query.all()
    return render_template('start_exam.html', exams=exams)
    
@app.route('/student_exam/<int:student_id>', methods=['GET', 'POST'])
def student_exam(student_id):
    student = Student.query.get_or_404(student_id)
    exam = Exam.query.get_or_404(student.exam_id)

    # Check if the student session is already closed
    if student.submitted_file:
        flash('You have already submitted your answer. Further edits are not allowed.', 'warning')
        return redirect(url_for('register'))  # Redirect to login or another appropriate page

    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files.get('answer_file')
        if uploaded_file and uploaded_file.filename != '':
            # Save the file in a directory structure: uploads/exam_id/registration_number/
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(exam.id), student.registration_number)
            os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
            file_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Mark the student's session as closed
            student.submitted_file = file_path
            db.session.commit()

            flash('Answer submitted successfully! You cannot make further changes.', 'success')
            return redirect(url_for('register'))  # Redirect to login or another appropriate page
        else:
            flash('Please upload a valid file!', 'danger')

    # Get the student's assigned question
    questions = student.get_question()
    return render_template('student_exam.html', student=student, exam=exam, questions=questions)

@app.route('/exam/start', methods=['POST'])
def start_exam_student():
    data = request.get_json()
    student_id = data.get('student_id')
    exam_id = data.get('exam_id')

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
        print(f"Full path: {full_path}")

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

    print(student_data)
    return render_template('exam_details.html', exam=exam, students=student_data)

if __name__ == '__main__':
    app.run(debug=True)