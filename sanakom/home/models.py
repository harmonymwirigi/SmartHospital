# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime, time
from apps import db
class AppointMent(db.Model):
    __tablename__ = 'AppointMent'
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date(), nullable = False)
    Time = db.Column(db.Time(), nullable = False)
    questions = db.relationship('Question', backref='appointment', lazy=True)
    weight = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Integer, nullable = False)
    Age = db.Column(db.Integer, nullable = False)
    Name = db.Column(db.String(30), nullable = False)
    Phoneno = db.Column(db.String(15), nullable = False)
    status = db.Column(db.Boolean, default = False)
    made_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    made_to = db.Column(db.Integer, db.ForeignKey('Doctors.id'))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    my_appointment = db.Column(db.Integer, db.ForeignKey('AppointMent.id'))
    question = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.question}'

class Exam(db.Model):
    __tablename__ = 'questions'
    made_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    q_id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(350), unique=True)
    a = db.Column(db.String(100))
    b = db.Column(db.String(100))
    c = db.Column(db.String(100))
    d = db.Column(db.String(100))
    ans1 = db.Column(db.String(100))
    ans2 = db.Column(db.String(100))
    ans3 = db.Column(db.String(100))
    ans4 = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)
    rendered_data = db.Column(db.Text)
    
    def __repr__(self):
        return '<Question: {}>'.format(self.ques)

class FirstTest(db.Model):
    __tablename__ = 'pics'
    id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    dataone = db.Column(db.Text)
    datatwo = db.Column(db.Text)
    datathree = db.Column(db.Text)
    result = db.Column(db.Integer)
class SecondTest(db.Model):
    __tablename__ = 'testtwo'
    id = db.Column(db.Integer, primary_key=True)
    made_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    picture = db.Column(db.Text)