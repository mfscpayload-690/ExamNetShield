# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Exam, Student
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Sample questions (in a real app, these would come from a database)
SAMPLE_QUESTIONS = [
    "Explain the concept of inheritance in OOP.",
    "What is the difference between a stack and a queue?",
    "How does HTTP work?",
    "Explain the principle of REST API.",
    "What is normalization in databases?",
    "How does public key cryptography work?",
    "Explain the concept of recursion.",
    "What is the time complexity of quicksort?",
    "How does a hash table work?",
    "Explain the MVC architecture."
]

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
            reg_number = f"{reg_prefix}{i}"
            student = Student(
                registration_number=reg_number,
                exam_id=new_exam.id
            )
            db.session.add(student)
            
        db.session.commit()
        flash(f'Exam "{name}" created with {end-start+1} students!', 'success')
        return redirect(url_for('create_exam'))
        
    return render_template('create_exam.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_number = request.form.get('reg_number')
        exam_id = request.form.get('exam_id')
        
        # Find the student
        student = Student.query.filter_by(
            registration_number=reg_number,
            exam_id=exam_id
        ).first()
        
        if student:
            # Record IP address
            student.ip_address = request.remote_addr
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
        
        # Get all students for this exam
        students = Student.query.filter_by(exam_id=exam_id).all()
        
        # Assign 3 random questions to each student
        for student in students:
            questions = random.sample(SAMPLE_QUESTIONS, min(3, len(SAMPLE_QUESTIONS)))
            student.set_questions(questions)
            
        db.session.commit()
        flash(f'Questions allocated to {len(students)} students!', 'success')
        
    exams = Exam.query.all()
    return render_template('start_exam.html', exams=exams)

if __name__ == '__main__':
    app.run(debug=True)