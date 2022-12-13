# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from apps.authentication.models import request_loader, scores, Users
from apps.home.form import Appointment, CheckAppointment, QuestionForm, Add, Testone
from flask import render_template, request,Flask
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
from flask_sqlalchemy import SQLAlchemy
from apps import db, login_manager
import base64
from apps.home.models import AppointMent, Question, Exam, FirstTest, SecondTest
from apps.authentication.models import Doctors
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit
from threading import Thread

import logging
from sys import stdout
from apps.home.camera2 import VideoCamera
from flask import request,redirect
from flask import Flask, render_template, request,url_for,g,session
import copy
from flask import Flask, render_template, Response, request, jsonify
from apps.home.camera2 import VideoCamera
from apps.home.camera3 import VideoCamera3
from apps.home.camera4 import VideoCamera4
from apps.home.readCoordinates import graph
import apps.home.Funcs as f
import datetime, time
from flask import current_app
from .. import socketio
imagelist={"static/images/image1.png","static/images/image2.png"}

original_questions = {
 #Format is 'question':[options]
 'Relating to People':['No evidence of difficulty or abnormality in relating to people.','Mildly abnormal relationships.','Moderately abnormal relationships.','Severely abnormal relationships.'],
 'imitation':['Appropriate imitation','mildly abnormal imitation','moderately abnormal imitation','severely abnormal imitation'],
 'Emotional Response':['Age-appropriate and situation-appropriate emotional response','mildly abnormal emotional response','moderately abnormal emotional response','severely abnormal emotional response'],
 'body use':['age appropriate body use','mildly abnormal body use','moderately abnormal body use','severely abnormal body use'],
 'object use':['Appropriate interest in,or use of toys and other objects','Mildly inappropriate interest in,or use of toys and other objects','Moderately interest in,or use of toys and other objects','Severely interest in,or use of toys and other objects'],
 'Adaption to change':['Age-appropriate adaption to change','Mildly abnormal adaption to change','Moderately abnormal adaption to change','Severely abnormal adaption to change'],
 'Visual Response':['Age-appropriate visual response','Mildly abnormal visual response','Moderately abnormal visual response','Severely abnormal visual response'],
 'Listening Response':["Age-appropriate listening response","Mildly abnormal listening reponse","Moderetly abnormal listening reponse","severely abnormal listening reponse"],
 'Taste, Smell, and Touch Response and Use': ["Normal use of, and response to, taste, smell, and touch", "Mildly abnormal use of, and response to, taste, smell and touch","Moderately abnormal use of, and response to, taste, smell, and touch", "Severely abnormal use of, and response to, taste, smell, and touch"],
 'Fear or Nervousness':["Normal fear or nervousness", "Mildly abnormal fear or nervousness", "Moderately abnormal fear or nervousness", "Severely abnormal fear or nervousness"],
 'Verbal Communication': ["Normal verbal communication, age and situation appropriate", "Mildly abnormal verbal communication", "Moderately abnormal verbal communication","Severely abnormal verbal communication"],
 'Nonverbal Communication':["Normal use of nonverbal communication, age and situation appropriate","Mildly abnormal use of nonverbal communication","Moderately abnormal use of nonverbal communication","Severely abnormal use of nonverbal communication"],
 'Activity level':["Normal activity level for age and circumstances","Mildly abnormal activity level", "Moderately abnormal activity level", "Severely abnormal activity level"],
 'Level and Consistency of intellectual response': ["Intelligence is normal and reasonably consistent across various areas", "Mildly abnormal intellectual functioning", "Moderately abnormal intellectual functioning","Severely abnormal intellectual functioning"],
 'General impressions': ["No autism spectrum disorder","Mild autism spectrum disorder", "Moderate autism spectrum disorder", "Severe autism disorder"]
}
questions = copy.deepcopy(original_questions)
import os

global rec, rec_frame
rec = 0

@blueprint.route('/diagnosis')
@login_required
def diagnosis():
    return render_template('home/diagnose.html')


@blueprint.route('/home')
@login_required
def home():
    return render_template('home/homepage.html')


@blueprint.route('/landing')
def landing():
    return render_template('home/hmpage.html')


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/appnt',  methods = ['GET', 'POST'])
@login_required
def appnt():
    my_appointment = AppointMent.query.filter_by(made_by=current_user.id).all()
    formm = Appointment(request.form)
    formm.Doctor.choices = [(hospital.Hospital) for hospital in Doctors.query.all()]
    if formm.validate_on_submit():
        print("form validated")
        doctor = Doctors.query.filter_by(Hospital=formm.Doctor.data).first()
        appointmentobj = AppointMent(made_by = current_user.id,made_to = doctor.id, Date= formm.Date.data,Time = formm.Time.data, weight = formm.weight.data,height = formm.height.data, Age = formm.Age.data, Name = formm.Name.data, Phoneno = formm.Phoneno.data)
        db.session.add(appointmentobj)
        db.session.commit()
        for i in formm.Question.data:
            question = Question(my_appointment=appointmentobj.id, question=i)
            db.session.add(question)
            db.session.commit()

        return redirect(url_for('home_blueprint.appnt'))
    else:
        print("invalid data")
    return render_template('home/appnt.html', segment= 'tables',form=formm, my_appointment=my_appointment)



@blueprint.route('/doctor')
@login_required
def doctor():
    appointments = AppointMent.query.filter_by(made_to = current_user.id).all()
    return render_template('home/doctor.html', segment='index', appointments = appointments)



@blueprint.route('/appointment/<id>', methods = ['POST', 'GET'])
@login_required
def appointment(id):
    appointment = AppointMent.query.filter_by(id = id).first()
    made_by = Users.query.filter_by(id = appointment.made_by).first()
    testone = FirstTest.query.filter_by(made_by = appointment.made_by).first()
    testtwo =  SecondTest.query.filter_by(made_by = appointment.made_by).first()
    results = made_by.marks
    completeAppintment = CheckAppointment(request.form)
    if completeAppintment.validate_on_submit():
        appointment.status = True
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('home_blueprint.doctor'))
    return render_template('home/appointment_profile.html', appointment = appointment, completeAppintment = completeAppintment, results = results, testone = testone, testtwo = testtwo)

t = []
#pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
@blueprint.route('/upload_image.html',methods=['GET', 'POST'])
@login_required
def predict():
    predict_form = Testone(request.form)
    if predict_form.validate_on_submit():
        file1 = request.files['fileone']
        file2 = request.files['filetwo']
        file3 = request.files['filethree']
        data1 = render_picture(file1.read())
        data2 = render_picture(file2.read())
        data3 = render_picture(file3.read())
        imagepath = [file1.filename, file2.filename, file3]
        res= []
        avg=0
        for y in imagepath:
            z=f.autisticpic(y)
            res.append(f.autisticpic(y))
            if z == "Autistic":
                avg = avg+1
            else:
                avg=avg+0
        avg=avg/3
        print(avg)
        if avg > 1/3:
            res="Autistic"
            avg = 1
            testresults = FirstTest(dataone = data1,datatwo = data2, datathree = data3, result = avg, made_by = current_user.id)
            db.session.add(testresults)
            db.session.commit()
            return redirect(url_for("home_blueprint.thanks"))
        else:
            res="Non Autistic"
            avg = 0
            testresults = FirstTest(dataone = data1,datatwo = data2, datathree = data3, result = avg, made_by = current_user.id)
            db.session.add(testresults)
            db.session.commit()
            return redirect(url_for("home_blueprint.thanks"))

    return render_template('home/test.html', form = predict_form)

@blueprint.route("/thanks")
@login_required
def thanks():
    return render_template("home/thanks.html")

# print("hi")
# @blueprint.route('upload_image.html', methods=['POST'])
# @login_required
# def predict():
#     imagefile1= request.files["imagefile1"]
#     imagefile2= request.files["imagefile2"]
#     imagefile3= request.files["imagefile3"]
#     imagepath=[imagefile1.filename,imagefile2.filename,imagefile3.filename]
#     imagepath2=[imagefile1, imagefile2, imagefile3]
#     zz=0
#     for z in imagepath:
#         imagepath2[zz].save(z)


#         zz=zz+1
#     idd = current_user.id
#     picss = pics(id=idd, pic1=imagepath[0],pic2=imagepath[1],pic3=imagepath[2])
#     db.session.add(picss)
#     db.session.commit()

#     res= []
#     avg=0
#     for y in imagepath:
#         z=f.autisticpic(y)
#         res.append(f.autisticpic(y))
#         if z == "Autistic":
#             avg = avg+1
#         else:
#             avg=avg+0
#     avg=avg/3
#     print(avg)
#     if avg > 1/3:
#         res="Autistic"
#         avg = 1
#         idd = current_user.id
#         score1 = scores(id=idd, score1=avg)
#         db.session.add(score1)
#         db.session.commit()
#     else:
#         res="Non Autistic"
#         avg = 0
#         idd = current_user.id
#         score1 = scores(id=idd, score1=avg)
#         db.session.add(score1)
#         db.session.commit()
#     segment = get_segment(request)




#     #return render_template("home/upload_image.html",prediction=res,Croppedpic="face.jpg", segment=segment)
#     return redirect(url_for("home_blueprint.vv"))


@blueprint.route('/quiz1<int:id>', methods = ['POST','GET'])
def quiz(id):
    q = Exam.query.filter_by(q_id = id).first()
    user = Users.query.filter_by(id = current_user.id).first()
    ma = float(user.marks)
    form = QuestionForm()
    if not q:
        return redirect(url_for('home_blueprint.score'))
    if request.method == 'POST':
        option = request.form['options']
        if option == q.ans1:
            ma = ma + 1.5
            user.marks = str(ma)
            db.session.add(user)
            db.session.commit()
        if option == q.ans2:
            ma = ma + 2.5
            user.marks = str(ma)
            db.session.add(user)
            db.session.commit()
        if option == q.ans3:
            ma = ma + 3.5
            user.marks = str(ma)
            db.session.add(user)
            db.session.commit()
        if option == q.ans4:
            ma = ma + 4.5
            user.marks = str(ma)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('home_blueprint.quiz', id=(id+1)))
    form.options.choices = [(q.a, q.a), (q.b, q.b), (q.c, q.c), (q.d, q.d)]
    return render_template('home/quiz.html', form=form, q=q, title='Question {}'.format(id))

# render picture function
def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic



@blueprint.route('/retake')
@login_required
def retake():
    user = Users.query.filter_by(id = current_user.id).first()
    user.marks = '0.0'
    db.session.add(user)
    db.session.commit()
    if user:
        return redirect(url_for("home_blueprint.quiz", id= 1))
    return "<h1>redirecting</h1>"


@blueprint.route('/question/<int:id>', methods=['GET', 'POST'])
@login_required
def question(id):
    form = QuestionForm()
    q = Exam.query.filter_by(q_id=id).first()
    session['marks']=0
    if not q:
        return redirect(url_for('home_blueprint.score'))
    if request.method == 'POST':
        option = request.form['options']
        if option == q.ans1:
            session['marks'] += 10
        elif option == q.ans2:
            session['marks'] += 20
        elif option == q.ans3:
            session['marks'] += 30
        elif option == q.ans4:
            session['marks'] += 40
        print(session['marks'])
        return redirect(url_for('home_blueprint.question', id=(id+1)))
    form.options.choices = [(q.a, q.a), (q.b, q.b), (q.c, q.c), (q.d, q.d)]
    return render_template('exam/question.html', form=form, q=q, title='Question {}'.format(id))

@blueprint.route("/add", methods=['POST','GET'])
def add():
    fom = Add()
    k = Exam.query.all()
    if fom.validate_on_submit():
        file1 = request.files['file']
        data = file1.read()
        render_file = render_picture(data)
        teo = Exam(ques = fom.ques.data, a = fom.a.data,data=data, rendered_data=render_file,b = fom.b.data, c = fom.c.data,d = fom.d.data, ans1 = fom.ans1.data, ans2 = fom.ans2.data, ans3 = fom.ans3.data, ans4 = fom.ans4.data)
        db.session.add(teo)
        db.session.commit()
        
        return redirect(url_for("home_blueprint.add"))
    return render_template("home/add.html", fom = fom, k = k)
@blueprint.route('/score')
@login_required
def score():
    idd = Users.query.filter_by(id= current_user.id).first()
    totalmarks = idd.marks
    return render_template('exam/score.html', title='Final Score', totalmarks = totalmarks)

Cam = VideoCamera()
Cam2 = VideoCamera4()
choose = 0
@socketio.on('input image', namespace='/test')
@login_required
def test_message(input):
    input = input.split(",")[1]
    if choose==0:
        Cam.enqueue_input(input)
    elif choose==1:
        Cam2.enqueue_input(input)

    #camera.enqueue_input(base64_to_pil_image(input))





@socketio.on('connect', namespace='/test')
@login_required
def test_connect():
    #app.logger.info("client connected")
    print("hi")

@blueprint.route('/video')
@login_required

def vv():
    #data = Cam.data()
    #print(data)


    """Video streaming home page."""
    return render_template('home/video.html')

@blueprint.route("/heatmap")
@login_required
def heatmap():
    id = current_user.id
    k = 1
    if k:
        graph(id)
        return redirect(url_for("home_blueprint.thanks"))
    
    return render_template('home/heatmap.html')

def gen(Camera,no):
    while True:
        frame = Camera.get_frame()[no]

        yield (b"--frame\r\n"
            b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@blueprint.route('/video_feed')
@login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if choose==0:
        frame = gen(Cam,0)
    elif choose==1:
        frame = gen(Cam2,0)



    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')


@blueprint.route('/video_feed2')
@login_required
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    frame = gen(Cam,1)

    return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

@blueprint.route('/video2')
@login_required
def vvv():
    global choose
    choose=1
    

    #data = Cam.data()
    #print(data)


    """Video streaming home page."""
    return render_template('home/video.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

@blueprint.route('/requests',methods=['POST','GET'])
@login_required
def action():
    return render_template('home/recording.html')

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
