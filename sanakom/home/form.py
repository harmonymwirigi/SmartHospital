# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField,validators, TimeField, IntegerField, SubmitField, SelectMultipleField, widgets, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class Questions(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget =widgets.CheckboxInput() 

class Appointment(FlaskForm):
    Doctor = SelectField('Hospital', validators=[DataRequired()])
    Phoneno = StringField('Phone Number', validators=[DataRequired()])
    Name = StringField('FULL NAME', validators=[DataRequired()])
    Date = DateField('Date',format='%Y-%m-%d', validators = [validators.DataRequired()])
    Time = TimeField('TIME', validators=[DataRequired()])
    weight = IntegerField('WEIGHT IN KG', validators = [DataRequired()])
    height = IntegerField("HEIGHT IN METERS", validators=[DataRequired()])
    Age = IntegerField('AGE', validators=[DataRequired()])
    Question = Questions('Questions', choices=[("Question1?"),("question2?"),("question3?")])
    Submit = SubmitField('BOOK')

class CheckAppointment(FlaskForm):
    Check = SubmitField('Done')


class QuestionForm(FlaskForm):
    options = RadioField('Options: ', validators=[DataRequired()], default=1)
    submit = SubmitField('Next')


class Add(FlaskForm):
    ques = StringField("quistion", validators=[DataRequired()])
    a = StringField("a", validators=[DataRequired()])
    b = StringField("b", validators=[DataRequired()])
    c = StringField("c", validators=[DataRequired()])
    d = StringField("d", validators=[DataRequired()])
    ans1 = StringField("ans1", validators=[DataRequired()])
    ans2 = StringField("ans2", validators=[DataRequired()])
    ans3 = StringField("ans3", validators=[DataRequired()])
    ans4 = StringField("ans4", validators=[DataRequired()])
    file = FileField("ATTACH FILE", validators=[FileAllowed(['docx', 'png', 'jpg', 'pdf', 'mp4', 'mp3'])])
    submit = SubmitField('add')

class Testone(FlaskForm):
    fileone = FileField("CHOOSE PICTURE", validators=[FileAllowed(['png', 'jpg'])])
    filetwo = FileField("CHOOSE PICTURE", validators=[FileAllowed(['png', 'jpg'])])
    filethree = FileField("CHOOSE PICTURE", validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField("PREDICT")