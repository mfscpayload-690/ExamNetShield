# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import *
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
                return render_template('create_exam.html')
        except ValueError:
            flash('Invalid range format. Use start-end (e.g., 1-10)', 'danger')
            return render_template('create_exam.html')
            
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
        
    return render_template('create_exam.html')

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
            # Check if student already has an IP address and it's different
            if student.ip_address and student.ip_address != current_ip:
                flash('Please login from your registered PC!', 'danger')
            else:
                # Record IP address (only if not previously set)
                if not student.ip_address:
                    student.ip_address = current_ip
                    db.session.commit()
                flash('Registration successful!', 'success')
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
            return redirect(url_for('start_exam'))
            
        # Get all students for this exam
        students = Student.query.filter_by(exam_id=exam_id).all()
        
        # Prepare question texts for random allocation
        question_texts = [q.question_text for q in exam_questions]
        
        # Assign random questions to each student
        for student in students:
            # Determine how many questions to assign 
            num_questions = min(1, len(question_texts))
            
            # Randomly select questions
            selected_questions = random.sample(question_texts, num_questions)
            student.set_questions(selected_questions)
            
        db.session.commit()
        flash(f'Questions allocated to {len(students)} students!', 'success')
        
    exams = Exam.query.all()
    return render_template('start_exam.html', exams=exams)

if __name__ == '__main__':
    app.run(debug=True)