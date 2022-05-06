from logging import debug
import re
import time
import datetime
from unicodedata import name
from flask import Flask, render_template, request, session,jsonify
from DBConnection import Db
import random
app = Flask(__name__)
app.secret_key = "hi"

staticpath="Z:\\Face Recognition\\static\\"


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_post',  methods=['post'])
def login_post():

    user_name = request.form['textfield']
    password=request.form['textfield2']
    d = Db()
    qry = "SELECT * FROM login WHERE `username`='"+user_name+"' AND `password`='"+password+"'"
    res = d.selectOne(qry)
    if res!= None:
        session['lid']=res['login_id']
        type = res['type']

        if res['type']=='admin':
            return '''<script>alert('Login Success');window.location='/home'</script>'''
        # elif res['type']=='staff':
        #     return  '''<script>alert('Login Success');window.location='/staff_home'</script>'''
        elif res['type']=='student':
            return '''<script>alert('Login Success');window.location='/stud_home'</script>'''
        elif res['type'] == 'guardian':
            qq="select stud_login_id from student where guardian_login='"+str(res["login_id"])+"'"
            dd=d.selectOne(qq)
            if dd is not None:
                session["stt"]=dd["stud_login_id"]
                return '''<script>alert('Login Success');window.location='/parent_view_attendence'</script>'''
            else:
                return '''<script>alert('Invalid user');window.location='/'</script>'''
        else:
            return '''<script>alert('Invalid user');window.location='/'</script>'''
    else:
        return '''<script>alert(' Invalid user!');window.location='/'</script>'''
        
           






@app.route('/home')
def hello_world():
    return render_template('admin/home.html')



@app.route('/add_staff')
def add_staff():
    qry="SELECT*FROM department"
    d=Db()
    rev=d.select(qry)
    return render_template('admin/Add staff.html',dept=rev)

@app.route('/add_staff_post',methods=['post'])
def add_staff_post():
    sname=request.form['textfield']
    gender=request.form['radio']
    photo=request.files['fileField']
    place=request.form['textfield2']
    pin=request.form['textfield3']
    post=request.form['textfield4']
    district=request.form['select']
    department=request.form['select2']
    phone=request.form['textfield5']
    email=request.form['textfield6']
    qualification=request.form['textfield7']
    password = random.randint(1000,9999)

    d = Db()
    dt = time.strftime("%Y%m%d-%H%M%S")
    photo.save(staticpath+"staff_media\\"+dt+".jpg")
    path = "/static/staff_media/"+dt+".jpg"

    qry1= "INSERT INTO `login`(`username`,`password`,`type`) VALUES('"+email+"','"+str(password)+"','staff')"
    lid = d.insert(qry1)

    qry="INSERT INTO `staff`(`s_name`,`s_gender`,`s_photo`,`s_palce`,`s_pin`,`s_post`,`s_district`,`dep_id`,`s_phone`,`s_email`,`s_login_id`,`qualification`) VALUES('"+sname+"','"+gender+"','"+path+"','"+place+"','"+pin+"','"+post+"','"+district+"','"+department+"','"+phone+"','"+email+"','"+str(lid)+"','"+qualification+"')"
    res=d.insert(qry)
    # print(res)

    return '''<script>alert('success');window.location='/add_staff'</script>'''




@app.route('/add_student')
def add_student():
    d=Db()
    qry1="select * from course"
    res=d.select(qry1)
    return render_template('admin/Add student.html',course=res)


@app.route('/add_student_post',methods=['post'])
def add_student_post():
    stdname=request.form['textfield']
    gender=request.form['radio']
    photo=request.files['fileField']
    place=request.form['textfield2']
    pin=request.form['textfield3']
    post=request.form['textfield4']
    district=request.form['select2']
    course=request.form['select']
    phone=request.form['textfield5']
    email=request.form['textfield6']
    guardian=request.form['textfield7']
    guardian_email=request.form['textfield8']
    sem=request.form["sem"]
    password=random.randint(1000,9999)
    d=Db()
    dt=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    photo.save(staticpath+"student_media\\"+dt+".jpg")
    path="/static/student_media/"+dt+".jpg"
    qry2="INSERT INTO login(username,password,type)VALUES('"+email+"','"+str(password)+"','student')"
    lid = d.insert(qry2)


    qry4="INSERT INTO`student`(stud_name, sem,stud_gender, stud_photo, stud_place, stud_pin, stud_post, stud_district, course_id, stud_phone,stud_email, stud_login_id, guardian, guardian_email, guardian_login) values('"+stdname+"','"+sem+"','"+gender+"','"+path+"','"+place+"','"+pin+"','"+post+"','"+district+"','"+course+"','"+phone+"','"+email+"','"+str(lid)+"','"+guardian+"','"+guardian_email+"','"+str(lid)+"')"
    # print(qry4)
    res=d.insert(qry4)
    return '''<script>alert('success');window.location='/add_student'</script>'''

@app.route("/f")
def f():
    return render_template("admin/fileuploads.html")

@app.route("/adminfileupload",methods=['post'])
def adminfileupload():


    # file2=request.files["file2"]
    # file3=request.files["file3"]


    fp1="Z:\\Face Recognition\\static\\sg\\a1.jpg"
    fp2="Z:\\Face Recognition\\static\\sg\\a2.jpg"
    fp3="Z:\\Face Recognition\\static\\sg\\a3.jpg"

    a=[]

    if "file1"  in request.files:
        file1 = request.files["file1"]
        if file1.filename!="":
            a.append(fp1)
            file1.save(fp1)

    if "file2"  in request.files:
        file2 = request.files["file2"]
        if file2.filename != "":
            a.append(fp2)
            file2.save(fp2)

    if "file3"  in request.files:
        file3 = request.files["file3"]
        if file3.filename != "":
            a.append(fp3)
            file3.save(fp3)

    db = Db()
    results = db.select("SELECT * FROM `student`")
    import face_recognition
    known_faces = []
    userids = []
    if results is not None:
        for result in results:
            img = result['stud_photo']
            # print(img)
            ss = "Z:\\Face Recognition" + img
            img = ss
            b_img = face_recognition.load_image_file(img)
            b_imgs = face_recognition.face_encodings(b_img)[0]
            known_faces.append(b_imgs)
            userids.append(result["stud_id"])
    studentids=[]
    import face_recognition

    l=request.form["hour"]
    dates=request.form["date"]
    subname=request.form["subname"]
    for m in a:
        unknown_image = face_recognition.load_image_file(m)
        try:
            m = len(face_recognition.face_encodings(unknown_image))
            for a in range(m):
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[a]
                results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.48)
                for i in range(len(results)):
                    if results[i] == True:
                        studentid = userids[i]
                        db = Db()
                        if studentid not in studentids:
                            studentids.append(studentid)
                        qry = "SELECT * FROM `attendance` WHERE DATE='"+dates+"' and stud_id='" + str(
                            studentid) + "' AND HOUR='" + str(l) + "'"
                        res = db.select(qry)
                        if len(res) == 0:
                            qry = "INSERT INTO `attendance` (`stud_id`,`date`,`hour`,subname) VALUES ('" + str(
                                studentid) + "','"+dates+"','"+str(l)+"','"+subname+"')"
                            db.insert(qry)
        except Exception as a:
            # print("okkkkkkk", a)
            pass

    k=[]

    studentids.sort()
    for i in studentids:
        qry="SELECT * FROM `student` WHERE stud_id='"+str(i)+"'"
        res=db.selectOne(qry)
        k.append(res)




    return render_template("admin/View student_attview.html",data=k)
@app.route('/course')
def course():
    d=Db()
    qry="SELECT * FROM `department`"
    res=d.select(qry)

    return render_template('admin/course.html',dept=res)



@app.route('/course_post',methods=['post'])
def course_add_post():
    department=request.form['select']
    course=request.form['textfield']
    semester=request.form['textfield2']
    qry = "INSERT INTO course (dep_id,course_name,sem)VALUES('" + department + "','" + course + "','" + semester + "')"
    # print(qry)
    d = Db()
    d.insert(qry)
    return '''<script> alert('success');window.location='/course'</script>'''



@app.route('/dep_add')
def dep_add():
    return render_template('admin/dep add.html')


@app.route('/dep_add_post',methods=['post'])
def dep_add_post():
    depname=request.form['textfield']
    qry="INSERT INTO  `department`(`dep_name`)VALUES('"+depname+"')"
    d=Db()
    d.insert(qry)
    return '''<script> alert('success');window.location='/dep_add'</script>'''





@app.route('/edit_dept/<id>')
def edit_dept(id):
    d=Db()
    qry="SELECT * FROM `department` WHERE `department_id`='"+id+"' "
    res=d.selectOne(qry)
    return  render_template('admin/Edit dept.html', data=res)



@app.route('/edit_dept_post',methods=['post'])
def edit_dept_post ():
    dep_id = request.form['did']
    department=request.form['textfield']
    d=Db()
    qry = "UPDATE `department` SET `dep_name`='" + department + "' WHERE `department_id`='" + dep_id + "'"
    res = d.update(qry)
    return'''<script> alert ('edit updated');window.location='/View_dept'</script>'''


@app.route("/adminindex")
def adminindex():
    return render_template("admin/adminindex.html")



@app.route('/edit_staff/<id>')
def edit_staff (id):
    qry="select * from staff where staff_id='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    qry="SELECT * FROM `department`"
    rres=db.select(qry)
    session["sid"]=id
    return render_template('admin/Edit staff.html',i=res,rr=rres)


@app.route('/edit_staff_post',methods=['post'])
def edit_staff_post ():
    name=request.form['textfield']
    gender=request.form['radio']
    id=str(session["sid"])
    place=request.form['textfield2']
    pin=request.form['textfield3']
    post=request.form['textfield4']
    district=request.form['select']
    department=request.form['select2']
    phone=request.form['textfield5']
    email=request.form['textfield6']
    qualification=request.form['textfield7']
    

    d = Db()
    if 'fileField' in request.files:
        photo=request.files['fileField']
        if photo.filename!="":
            dt = time.strftime("%Y%m%d-%H%M%S")
            photo.save(staticpath+"staff_media\\"+dt+".jpg")
            path = "/static/staff_media/"+dt+".jpg"

   

            qry="update staff set s_name='"+name+"',s_gender='"+gender+"',s_photo='"+path+"',s_palce='"+place+"',s_pin='"+pin+"',s_post='"+post+"',s_district='"+district+"',dep_id='"+department+"',s_phone='"+phone+"',s_email='"+email+"',qualification='"+qualification+"' where staff_id='"+id+"'"
            res=d.insert(qry)
        else:
            qry = "update staff set s_name='" + name + "',s_gender='" + gender + "'s_palce='" + place + "',s_pin='" + pin + "',s_post='" + post + "',s_district='" + district + "',dep_id='" + department + "',s_phone='" + phone + "',s_email='" + email + "',qualification='" + qualification + "' where staff_id='" + id + "'"
            res = d.insert(qry)

    else:
        qry="update staff set s_name='"+name+"',s_gender='"+gender+"'s_palce='"+place+"',s_pin='"+pin+"',s_post='"+post+"',s_district='"+district+"',dep_id='"+department+"',s_phone='"+phone+"',s_email='"+email+"',qualification='"+qualification+"' where staff_id='"+id+"'"
        res=d.insert(qry)
        # print(res)
    return '''<script>alert('success');window.location='/view_staff'</script>'''






@app.route('/edit_student/<id>')
def edit_student (id):
    d=Db()
    res="select * from student where stud_id='"+str(id)+"'"
    var=d.selectOne(res)
    print(var)
    return render_template('admin/Edit student.html',abcd=var)


@app.route('/edit_student_post',methods=['post'])
def edit_student_post ():
    stdname = request.form['textfield']
    gender = request.form['radio']
    filename="Z:\\Face Recognition\\static\\student_media\\"
    pth="/static/student_media/"
    place = request.form['textfield2']
    pin = request.form['textfield3']
    post = request.form['textfield4']
    district = request.form['select2']
    course = request.form['select']
    phone = request.form['textfield5']
    email = request.form['textfield6']
    sem=request.form["sem"]
    id = request.form['sid']
    if 'fileField' in request.files:
        photo = request.files['fileField']
        if photo.filename!="":
            from datetime import datetime
            a= datetime.now().strftime("%Y%m%d_%H%M%S")
            photo.save(filename+ a+".jpg")
            pth=pth+ a+".jpg"
            qry="update student set stud_name='"+stdname+"',stud_gender='"+gender+"',stud_photo='"+pth+"',stud_place='"+place+"',stud_pin='"+pin+"',stud_post='"+post+"',stud_district='"+district+"',course_id='"+course+"',stud_phone='"+phone+"',stud_email='"+email+"',sem='"+sem+"' where stud_id='"+str(id)+"'"
            d=Db()
            d.update(qry)
        else:
            qry = "update student set stud_name='" + stdname + "',stud_gender='" + gender + "',stud_place='" + place + "',stud_pin='" + pin + "',stud_post='" + post + "',stud_district='" + district + "',course_id='" + course + "',stud_phone='" + phone + "',stud_email='" + email + "',sem='" + sem + "' where stud_id='" + str(
                id) + "'"
            d = Db()
            d.update(qry)
    else:
        qry = "update student set stud_name='" + stdname + "',stud_gender='" + gender + "',stud_place='" + place + "',stud_pin='" + pin + "',stud_post='" + post + "',stud_district='" + district + "',course_id='" + course + "',stud_phone='" + phone + "',stud_email='" + email + "',sem='" + sem + "' where stud_id='" + str(
            id) + "'"
        d = Db()
        d.update(qry)


    return "<Script>alert('Updated successfully');window.location='/view_student'</script>"





@app.route('/edit_subject/<id>')
def edit_subject(id):
    d=Db()
    qry="SELECT subject.*,course.course_name FROM SUBJECT INNER JOIN course ON course.course_id=subject.course_id where `subject`.`sub_id`='"+id+"'"
    res=d.selectOne(qry)
    qry2="SELECT * FROM `subject` WHERE `course_id`='"+id+"'"
    resb=d.selectOne(qry2)
    qry3="SELECT * FROM `course`"
    res3=d.select(qry3)
    return render_template('admin/Edit subject.html',data=res,resb=res,data3=res3)



@app.route('/edit_subject_post',methods=['post'])
def edit_subject_post ():
    course=request.form['ss']
    semester=request.form['select2']
    subject=request.form['textfield']
    id = request.form['did']
    d=Db()
    qry="UPDATE `subject` SET `course_id`='"+course+"', `semester`='"+semester+"', `subject`='"+subject+"' WHERE `sub_id`='"+str(id)+"'"
    d.update(qry)
    # print(qry)
    return '''<script> alert('update succesfully');window.location='/view_subject'</script>'''


@app.route('/home')
def home() :
    return render_template('admin/home.html')






@app.route('/send_reply')
def send_reply ():
    return render_template('admin/send reply.html')




@app.route('/Staff')
def Staff ():
    return render_template('admin/Staff.html')



@app.route('/staff_subject')
def staff_subject():
    d = Db()
    qry="SELECT * FROM `course`"
    resa = d.select(qry)
    # qry = "SELECT * FROM `subject`"
    # resb = d.select(qry)
    return render_template('admin/staff-subject.html',data=resa)
@app.route("/changevalue")
def change():
    id=request.args.get('id')
    query12 = "select * from subject where course_id='"+id+"'"
    db=Db()
    datt=db.select(query12)
    return jsonify(datt)

@app.route("/getsubaccbatch")
def changev():
    g=request.args.get('crs')
    id=request.args.get('id')
    query12 = "select * from subject where course_id='"+g+"' and semester='"+id+"'"
    db=Db()
    datt=db.select(query12)
    return jsonify(datt)

@app.route("/getstaffacccourse")
def changest():
    id=request.args.get('id')
   
    db=Db()
    query12 ="select staff.* from staff inner join course on  course.dep_id=staff.dep_id where course.dep_id='"+id+"'"
    datt=db.select(query12)
    return jsonify(datt)

@app.route('/staff_subject_post',methods=['post'])
def staff_subject_post():
    sub=request.form['select2']
    staff = request.form['select']
    qry="INSERT INTO `staff-subject_alllocation`(`staff_id`,`subject_id`,`date`)VALUES('"+staff+"','"+sub+"',curdate())"
    d=Db()
    d.insert(qry)
    return '''<script> alert('success');window.location='/staff_subject'</script>'''

# @app.route('/view_allocated_subject_post',methods=['post'])
# def view_allocated_subject_post():
#     sub=request.form['select2']
#     staff = request.form['select']
#     qry="INSERT INTO `staff-subject_alllocation`(`staff_id`,`subject_id`,`date`)VALUES('"+staff+"','"+sub+"',curdate())"
#     d=Db()
#     d.insert(qry)

@app.route('/student')
def student():
    return render_template('admin/student.html')




@app.route('/add_subject')
def subject():
    d=Db()
    qry="SELECT * FROM  `course`"
    res=d.select(qry)
    return render_template('admin/Add subject.html',data=res)


@app.route('/add_subject_post',methods=[ 'post'])
def add_subject():
    course=request.form['select']
    semester=request.form['select2']
    subject=request.form['textfield']
    qry="INSERT INTO `subject`(`course_id`,`semester`,`subject`)VALUES('"+ course +"','"+ semester +"','"+ subject +"')"
    d=Db()
    d.insert(qry)
    return'''<script> alert('success');window.location='/add_subject'</script>'''




@app.route('/time_table')
def time_table ():
    d = Db()
    qry="SELECT * FROM `course`"
    resa = d.select(qry)
    return render_template('admin/timetable.html',data=resa)

@app.route('/time_table_post',methods=['post'])
def time_table_post():
    sub=request.form["sub"]
    day=request.form["day"]
    hr=request.form["hr"]
    d = Db()
    qry="insert into timetable(sub_id,day,hour) values('"+sub+"','"+day+"','"+hr+"')"
    resa = d.insert(qry)
    return '''<script>alert('Sucessfuly added');window.location='/time_table'</script>'''



@app.route('/view_allocated_subject')
def view_allocated_subject ():
    qry="SELECT `staff-subject_alllocation`.*,`staff`.`s_name`, `subject`.`subject` FROM `staff` INNER JOIN `staff-subject_alllocation` ON `staff-subject_alllocation`.`staff_id`=`staff`.`staff_id` INNER JOIN `subject` ON `subject`.`sub_id`=`staff-subject_alllocation`.`subject_id`"
    d=Db()
    res=d.select(qry)
    return render_template('admin/view allocated subject.html',data=res)



@app.route('/delete_allocated_subject/<id>')
def delete_allocated_sub(id):
    d = Db()
    qry ="DELETE FROM `staff-subject_alllocation`WHERE `alloc_id`='" + id + "'"
    res = d.delete(qry)
    return '''<script> alert('delete');window.location='/view_allocated_subject'</script>'''




@app.route('/view_complaint')
def view_complaint ():
    d=Db()
    qry="SELECT * FROM complaint INNER JOIN student ON complaint.stud_login_id=student.stud_login_id"
    res=d.select(qry)
    return render_template('admin/View complaint.html',data=res)







@app.route('/view_course')
def view_course ():
    d=Db()
    qry="SELECT `department`.`dep_name`,`course`.*  FROM `course` INNER JOIN `department` ON `course`.`dep_id`=`department`.`department_id`"
    res=d.select(qry)
    return render_template('admin/View Course.html',data=res)

@app.route('/view_course_post',methods=['POST'])
def view_course_post ():
    name=request.form["textfield"]
    d=Db()
    qry="SELECT `department`.`dep_name`,`course`.*  FROM `course` INNER JOIN `department` ON `course`.`dep_id`=`department`.`department_id` where dep_name like '%"+name+"%' or course_name like '%"+name+"%'"
    res=d.select(qry)
    return render_template('admin/View Course.html',data=res)

@app.route('/delete_course/<id>')
def delete_course(id):
    d = Db()
    qry = "DELETE FROM `course` WHERE `course_id`='"+id+"'"
    res = d.delete(qry)
    return '''<script> alert('delete');window.location='/view_course'</script>'''
@app.route('/edit_course/<id>')
def edit_course(id):
    d=Db()
    qry="SELECT * FROM `department`"
    res=d.select(qry)
    qry1="SELECT * FROM course where course_id='"+id+"'"
    res1=d.selectOne(qry1)
    session["crsid"]=id
    return render_template("admin/Edit Course.html",dept=res,data=res1)

@app.route('/course_edit_post',methods=['post'])
def course_edit_post():
    department=request.form['select']
    course=request.form['textfield']
    semester=request.form['textfield2']
    id=str(session["crsid"])
    qry = "update course set dep_id='"+department+"',course_name='"+course+"',sem='"+semester+"' where course_id='"+id+"'"
    # print(qry)
    d = Db()
    d.update(qry)
    return '''<script> alert('success');window.location='/view_course'</script>'''



@app.route('/View_dept')
def View_dept():
    d=Db()
    qry="SELECT * FROM `department`"
    res=d.select(qry)
    return render_template('admin/View dept.html',data=res)


@app.route('/View_deptpost',methods=['POST'])
def View_dept_post():
    name=request.form["textfield"]
    d=Db()
    qry="SELECT * FROM `department` where dep_name like '%"+name+"%'"
    res=d.select(qry)
    return render_template('admin/View dept.html',data=res)

@app.route('/delete_department/<id>')
def delete_department(id):
    d = Db()
    qry = "DELETE FROM `department` WHERE `department_id`='"+id+"'"
    res = d.delete(qry)
    return '''<script>alert('delete');window.location='/View_dept'</script>'''





@app.route('/view_staff')
def view_staff ():
    d=Db()
    qry=" SELECT * FROM `staff`"
    res=d.select(qry)
    d = Db()

    qry = "SELECT * FROM `department`"
    resb = d.select(qry)
    return render_template('admin/View staff.html',data=res,resb=resb)



@app.route('/delete_staff/<id>')
def delete_staff(id):
    d = Db()
    qry = "DELETE FROM `staff` WHERE `staff_id`='"+id+"'"
    res = d.delete(qry)
    return '''<script> alert('delete');window.location='/view_staff'</script>'''




@app.route('/admin_attendanceview')
def adminattendanceview():
    db=Db()
    qry="SELECT * FROM `course`"
    data=db.select(qry)
    return render_template("admin/Viewattendance.html",crs=data)

@app.route("/adminviewattendanceviewpost",methods=['post'])
def adminviewattendanceviewpost():
    db=Db()
    crs=request.form["crs"]
    sem=request.form["sem"]
    date=request.form["date"]
    hour=request.form["hour"]
    qry="SELECT `attendance`.*,`student`.* FROM  student  LEFT  JOIN  `attendance` ON `attendance`.`stud_id`=`student`.`stud_id` WHERE `attendance`.date='"+date+"' AND `course_id`='"+crs+"' AND `hour`='"+hour+"'"
    res=db.select(qry)

    qry = "SELECT * FROM `course`"
    data = db.select(qry)

    a=""
    if len(res)>0:
        a=res[0]['subname']


    return render_template("admin/Viewattendance.html",datas=res,crs=data,a=a)




@app.route('/view_staffsearch',methods=['post'])
def view_staffsearch ():
    d=Db()
    department=request.form['select']
    qry="SELECT * FROM `department`"
    res=d.select(qry)
    qry = " SELECT * FROM `staff` where dep_id='"+department+"'"
    res1 = d.select(qry)






    return render_template('admin/View staff.html',resb=res,data=res1)


@app.route('/view_student')
def view_student ():
    d=Db()
    qry="SELECT * FROM `student` order by stud_name ASC"
    res=d.select(qry)
    qry = "SELECT * FROM `course`"
    resa = d.select(qry)
    qry = "SELECT * FROM `department`"
    resb = d.select(qry)

    return render_template('admin/View student.html',data=res,resa=resa,resb=resb)


@app.route('/delete_student/<id>')
def delete_stud(id):
        d = Db()
        qry ="DELETE FROM `student`WHERE `stud_id`='" + id + "'"
        res = d.delete(qry)
        return '''<script> alert('delete');window.location='/view_student'</script>'''


@app.route('/view_student_post',methods=['POST'])
def view_student_post ():
    d=Db()
    button=request.form["button"]
    if button =="Go":
        dept=request.form["select"]
        crs = request.form["select2"]
        qry = "SELECT * FROM student WHERE `course_id`='"+crs+"'"
        res = d.select(qry)
    else:
        name=request.form["textfield"]
        qry = "SELECT * FROM `student` where stud_name like '%"+name+"%'  order by stud_name ASC"
        res = d.select(qry)
    qry = "SELECT * FROM `course`"
    resa = d.select(qry)
    qry = "SELECT * FROM `department`"
    resb = d.select(qry)

    return render_template('admin/View student.html',data=res,resa=resa,resb=resb)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
