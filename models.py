# models.py
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)  # in hours
    reg_number_prefix = db.Column(db.String(10), nullable=False)
    reg_number_range = db.Column(db.String(20), nullable=False)
    is_started = db.Column(db.Boolean, default=False)
    is_ended = db.Column(db.Boolean, default=False)
    students = db.relationship('Student', backref='exam', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    allocated_questions = db.Column(db.Text, nullable=True)  # stored as JSON
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)

    def set_questions(self, questions_list):
        self.allocated_questions = json.dumps(questions_list)
        
    def get_questions(self):
        if self.allocated_questions:
            return json.loads(self.allocated_questions)
        return []

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)