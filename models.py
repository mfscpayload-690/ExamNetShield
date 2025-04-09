# models.py
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

class Exam(db.Model):

    __tablename__ = 'exam' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)  # in hours
    reg_number_prefix = db.Column(db.String(10), nullable=False)
    reg_number_range = db.Column(db.String(20), nullable=False)
    is_started = db.Column(db.Boolean, default=False)
    is_ended = db.Column(db.Boolean, default=False)
    students = db.relationship('Student', backref='exam', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(50), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    ip_address = db.Column(db.String(50), nullable=True)
    allocated_questions = db.Column(db.String(255), nullable=True)  # Single question as a string
    submitted_file = db.Column(db.String(255), nullable=True)

    def set_question(self, question_text):
        self.allocated_questions = question_text
        db.session.commit()
    def get_question(self):
        return self.allocated_questions 

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)


class ExamSession(db.Model):
    __tablename__ = 'exam_sessions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # Foreign key to Student
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)  # Foreign key to Exam
    start_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in seconds
    is_closed = db.Column(db.Boolean, default=False) 
    # Relationships
    student = db.relationship('Student', backref='exam_sessions', lazy=True)
    exam = db.relationship('Exam', backref='exam_sessions', lazy=True)

    __table_args__ = (db.UniqueConstraint('student_id', 'exam_id', name='unique_student_exam'),)