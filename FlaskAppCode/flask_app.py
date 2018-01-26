import os
import csv
from dbconn import connection
from dbconn2 import connection2
from wtforms import Form, TextField, validators, FileField, BooleanField, StringField, PasswordField, TextAreaField
from flask import Flask, render_template, request, url_for, flash, redirect, session, send_file
from MySQLdb import escape_string as thwart
from wtforms.fields.html5 import EmailField
import gc
from werkzeug import secure_filename
import requests
os.environ["ODBCSYSINI"] = "/home/s1mple"
UPLOAD_FOLDER = 'SiteFiles/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug=True
app.secret_key ='yoursecretkey' 

class DmForm(Form):
    message_d = TextAreaField('',render_kw={"placeholder":" Message","cols":"80","rows":"9"})
class AcvForm(Form):
    acv_a = TextAreaField('',render_kw={"placeholder": " Current Activity","id": "acv_a","cols":"35"})
    place_a = TextAreaField('',render_kw={"placeholder": " Name of Place","id": "place_a","cols":"35"})
    locality_a = TextAreaField('',render_kw={"placeholder": " Locality","id": "locality_a","cols":"35"})
    city_a = TextAreaField('',render_kw={"placeholder": " City","id": "city_a","cols":"35"})
    country_a = TextAreaField('',render_kw={"placeholder": " Country","id": "country_a","cols":"35"})
    pincode_a = TextAreaField('',render_kw={"placeholder": " Pincode","id": "pincode_a","cols":"35"})
class MsgForm(Form):
    recipient_m = TextAreaField('',[validators.Required()],render_kw={"placeholder": " Recipient's username","id": "recipient_m","cols":"35"})
    message_m = TextAreaField('',[validators.Required()],render_kw={"placeholder": " Message","id": "message_m","cols":"80","rows":"9"})
class RegForm(Form):
    name_r = TextField('',[validators.Length(min=1,max=50), validators.Required()],render_kw={"placeholder": " Name","id": "name_r"})
    username_r = TextField('',[validators.Length(min=1,max=50), validators.Required()],render_kw={"placeholder": " Username","id": "username_r"})
    email_r = EmailField('', [validators.DataRequired(), validators.Email()],render_kw={"placeholder": " Email","id": "email_r"})
    password_r = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm_r', message='Passwords must match')
    ],render_kw={"placeholder": " Password","id": "password_r"})
    confirm_r = PasswordField('',render_kw={"placeholder": " Confirm Password","id": "confirm_r"})

class SettingsForm(Form):
    name_s = TextField('',render_kw={"placeholder": " Name","id": "name_s"})
    username_s = TextField('',render_kw={"placeholder": " Username","id": "username_s"})
    email_s = EmailField('',render_kw={"placeholder": " Email","id": "email_s"})
    mobile_s = TextField('',render_kw={"placeholder": " Mobile","id": "mobile_s"})
    description_s = TextField('',render_kw={"placeholder": " Description","id": "mobile_s"})
    oldpassword_s = PasswordField('',render_kw={"placeholder": " Current Password","id": "oldpassword_s"})
    website_s = TextField('',render_kw={"placeholder": " Website","id": "website_s"})
    password_s = PasswordField('', [
        validators.EqualTo('confirm_s', message='Passwords must match')
    ],render_kw={"placeholder": " New Password","id": "password_s"})
    confirm_s = PasswordField('',render_kw={"placeholder": " Confirm Password","id": "confirm_s"})

class LogForm(Form):
    username_l = TextField('',[validators.Length(min=1,max=50), validators.Required()],render_kw={"placeholder": " Username","id": "username_l"})
    password_l = PasswordField('',[validators.Required()],render_kw={"placeholder": " Password","id": "password_l"})

@app.route('/',methods=["GET","POST"])
def index():
    return render_template("index.html")
@app.route('/social',methods=["GET","POST"])
def social():
    err = False
    forml = LogForm(request.form)
    try:
        if session['logged_in']==True:
            return redirect("http://s1mple.pythonanywhere.com/profile?username="+session['username'])
    except Exception as e:
        return render_template("social.html",forml=forml,err=err)

@app.route('/login',methods=["GET","POST"])
def login():
    err = False
    forml = LogForm(request.form)
    try:
        if request.method=="POST" and forml.validate()==True:
            username = forml.username_l.data
            password = forml.password_l.data
            c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username = (%s) AND password = (%s) ",
                          (thwart(username),thwart(password)))
            if int(x) > 0:
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                session['password'] = password
                return redirect("http://s1mple.pythonanywhere.com/profile?username="+session['username'])
            else:
                err = True
                return render_template("index.html",forml=forml,err=err)
        if request.method=="POST" and forml.validate()!=True:
            err = True
            return render_template("index.html",forml=forml,err=err)
    except Exception as e:
        err = True
        return render_template("index.html",forml=forml,err=err)


@app.route('/register',methods=["GET","POST"])
def register():
    formr = RegForm(request.form)
    err = False
    try:
        if request.method=="POST" and formr.validate()==True:
            name = formr.name_r.data
            username = formr.username_r.data
            email = formr.email_r.data
            password = formr.password_r.data
            c, conn = connection()
            x=c.execute("SELECT * FROM users WHERE username= (%s) AND email= (%s)",
                          (thwart(username), thwart(email)))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            if int(x)>0:
                err=True
                return render_template("register.html",formr=formr,err=err)
            else:
                c,conn = connection()
                c.execute("INSERT INTO users (name,username,email,password) VALUES(%s,%s,%s,%s)",(thwart(name),thwart(username),thwart(email),thwart(password)))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                session['password'] = password
                return redirect("http://s1mple.pythonanywhere.com/settings")
        elif request.method=="POST" and formr.validate()!=True:
            err = True
            return render_template("register.html",formr=formr,err=err)
        else:
            return render_template("register.html",formr=formr,err=err)

    except Exception as e:
        return render_template("register.html",formr=formr,err=err)

@app.route('/logout',methods=["GET","POST"])
def logout():
    session['logged_in'] = False
    session['username'] = None
    session['password'] = None
    session.clear()
    return render_template("index.html")

@app.route('/profile/',methods=["GET","POST"])
def profile():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    formd = DmForm(request.form)
    try:

        username = request.args.get('username',type=str)
        username_for_pics = username
        if request.method=="POST" and formd.validate()==True:
            recipient = request.form.get('recipient',type=str)
            c, conn = connection()
            c.execute("INSERT INTO messages (recipient,sender,message) VALUES (%s,%s,%s)",(recipient,str(session['username']),str(formd.message_d.data),))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            return redirect("http://s1mple.pythonanywhere.com")
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        interests = [item1[9] for item1 in c.fetchall()]
        interests_arr = interests[0].split(';')
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        interests_arr.pop(len(interests_arr)-1)

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        subs = [item1[8] for item1 in c.fetchall()]
        subs_arr = subs[0].split(';')
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        subs_arr.pop(len(subs_arr)-1)

        activity_bool = False
        try:
            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_username = [item1[1] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            if len(acv_username)>0:
                activity_bool = True

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_acv = [item1[2] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_place = [item1[3] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_locality = [item1[4] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_city = [item1[5] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            acv_pin = [item1[7] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

        except:
            activity_bool = False
        return render_template("profile.html",username=username,username_for_pics=username_for_pics,name=name,email=email,website=website,desc=desc,mobile=mobile,formd=formd,interests_arr=interests_arr,subs_arr=subs_arr,activity_bool=activity_bool,acv_acv=acv_acv,acv_place=acv_place,acv_locality=acv_locality,acv_city=acv_city,acv_pin=acv_pin)
    except Exception as e:
        return str(e)
@app.route('/subscribe/',methods=["GET","POST"])
def subs():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    try:
        username = request.args.get('username',type=str)+";"
        current_user = session['username']
        c, conn = connection()
        c.execute("UPDATE users SET subs=CONCAT(subs,(%s)) WHERE username=(%s)",(username,current_user,))
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        return redirect("http://s1mple.pythonanywhere.com")

    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")

@app.route('/settings/',methods=["GET","POST"])
def settings():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    forms = SettingsForm(request.form)
    try:

        username = session['username']
        if request.method=="POST":
            try:
                file1 = request.files['file1']
                filename1 = secure_filename(session['username'])+"dp"+".jpg"
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                file2 = request.files['file2']
                filename2 = secure_filename(session['username'])+"cover"+".jpg"
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            except:
                pass
        if request.method=="POST" and forms.validate()==True:
            oldpassword = forms.oldpassword_s.data
            name_update = forms.name_s.data
            try:
                if str(oldpassword)==str(session['password']):
                    file1 = request.files['file1']
                    filename1 = secure_filename(session['username'])+'dp'+'.jpg'
                    file1.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))

                    file2 = request.files['file2']
                    filename2 = secure_filename(session['username'])+'cover'+'.jpg'
                    file2.save(os.path.join(app.config['UPLOAD_FOLDER'],filename2))
                if len(str(name_update))>0 and str(oldpassword)==str(session['password']):
                    c, conn = connection()
                    c.execute("UPDATE users SET name=(%s) WHERE username=(%s)",(name_update,username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
            except:
                pass

            username_update = forms.username_s.data
            if len(str(username_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET username=(%s) WHERE username=(%s)",(username_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                session['username'] = username_update
            description_update = forms.description_s.data
            if len(str(description_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET description=(%s) WHERE username=(%s)",(description_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            email_update = forms.email_s.data
            if len(str(email_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET email=(%s) WHERE username=(%s)",(email_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            website_update = forms.website_s.data
            if len(str(website_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET website=(%s) WHERE username=(%s)",(website_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            mobile_update = forms.mobile_s.data
            if len(str(mobile_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET mobile=(%s) WHERE username=(%s)",(mobile_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
            password_update = forms.password_s.data
            if len(str(password_update))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET password=(%s) WHERE username=(%s)",(password_update,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                session['password'] = password_update
            interests = ""
            simpsubs = ""
            if request.form.get('interests_gaming'):
                interests = interests + "Gaming;"
            if request.form.get('interests_sports'):
                interests = interests + "Sports;"
            if request.form.get('interests_olympics'):
                interests = interests + "Olympics;"
            if request.form.get('interests_party'):
                interests = interests + "Party;"
            if request.form.get('interests_movies'):
                interests = interests + "Movies;"
            if request.form.get('interests_political'):
                interests = interests + "Political;"
            if request.form.get('interests_events'):
                interests = interests + "Events;"
            if request.form.get('interests_quiz'):
                interests = interests + "Quizzing;"
            if request.form.get('interests_books'):
                interests = interests + "Books;"
            if request.form.get('interests_nature'):
                interests = interests + "Nature;"
            if request.form.get('interests_travel'):
                interests = interests + "Travel;"
            if request.form.get('interests_cooking'):
                interests = interests + "Cooking;"
            if request.form.get('interests_coding'):
                interests = interests + "Coding;"
            if request.form.get('interests_mitmanipal'):
                simpsubs = simpsubs + "MITManipal;"
                c, conn = connection()
                x = c.execute("SELECT * FROM simp WHERE username=(%s)",(session['username'],))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                if int(x) > 0:
                    c, conn = connection()
                    c.execute("UPDATE simp SET subs=CONCAT(interests,(%s)) WHERE username=(%s)",(simpsubs,session['username'],))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                else:
                    c, conn = connection()
                    c.execute("INSERT INTO simp (username,subs) VALUES(%s,%s)",(session['username'],simpsubs,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
            if len(str(interests))>0 and str(oldpassword)==str(session['password']):
                c, conn = connection()
                c.execute("UPDATE users SET interests=CONCAT(interests,(%s)) WHERE username=(%s)",(interests,username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()


        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        return render_template("settings.html",username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,forms=forms)
    except Exception as e:
        return str(e)

@app.route('/messages/',methods=["GET","POST"])
def messages():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    formm = MsgForm(request.form)
    try:
        username=session['username']
        if request.method=="POST" and formm.validate()==True:
            c, conn = connection()
            c.execute("INSERT INTO messages (recipient,sender,message) VALUES (%s,%s,%s)",(str(formm.recipient_m.data),str(session['username']),str(formm.message_m.data)))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM messages WHERE recipient=%s",(username,))
        messages = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM messages WHERE recipient=%s",(username,))
        senders = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        return render_template("messages.html",username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,formm=formm,messages=messages,senders=senders,le=len(messages))
    except Exception as e:
        return str(e)
@app.route('/activities/',methods=["GET","POST"])
def activities():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    forma = AcvForm(request.form)
    try:
        username=session['username']
        if request.method=="POST" and forma.validate()==True:
            c, conn = connection()
            x=c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            if int(x)>0:
                if len(str(forma.acv_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET acv=(%s) WHERE username=(%s)",(str(forma.acv_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.place_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET place=(%s) WHERE username=(%s)",(str(forma.place_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.locality_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET locality=(%s) WHERE username=(%s)",(str(forma.locality_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.city_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET city=(%s) WHERE username=(%s)",(str(forma.city_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.country_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET country=(%s) WHERE username=(%s)",(str(forma.country_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.pincode_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET pincode=(%s) WHERE username=(%s)",(str(forma.pincode_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
            else:
                c, conn = connection()
                c.execute("INSERT INTO acvtab (username) VALUES (%s)",(username,))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                if len(str(forma.acv_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET acv=(%s) WHERE username=(%s)",(str(forma.acv_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.place_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET place=(%s) WHERE username=(%s)",(str(forma.place_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.locality_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET locality=(%s) WHERE username=(%s)",(str(forma.locality_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.city_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET city=(%s) WHERE username=(%s)",(str(forma.city_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.country_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET country=(%s) WHERE username=(%s)",(str(forma.country_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
                if len(str(forma.pincode_a.data))>0:
                    c, conn = connection()
                    c.execute("UPDATE acvtab SET pincode=(%s) WHERE username=(%s)",(str(forma.pincode_a.data),username,))
                    conn.commit()
                    c.close()
                    conn.close()
                    gc.collect()
            return redirect("http://s1mple.pythonanywhere.com")
            ''' ADD NOTIFICATION LINK HERE '''

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()



        return render_template("activities.html",username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,forma=forma)
    except Exception as e:
        return str(e)

@app.route('/search/',methods=["GET","POST"])
def search():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    try:
        query = request.form.get('searchtext',type=str)
        username = session['username']
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE name=%s",(query,))
        name_search = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE name=%s",(query,))
        username_search = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE name=%s",(query,))
        desc_search = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        return render_template("search.html",username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,name_search=name_search,username_search=username_search,desc_search=desc_search,le=len(username_search))
    except Exception as e:
        return str(e)

@app.route('/simp/',methods=["GET","POST"])
def simp():
    simp_sub_bool = False
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    try:

        username = session['username']
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM simp WHERE username=%s",(username,))
        simpsubs = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM simp_data")
        h1 = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM simp_data")
        h2 = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM simp_data")
        h3 = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        try:
            simpsubs = simpsubs[0]
        except:
            simpsubs = ""
        if len(simpsubs)>0:
            simp_sub_bool = True
        else:
            simp_sub_bool = False
        le = len(h1)
        return render_template("simp.html",le=le,h1=h1,h2=h2,h3=h3,username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,simp_sub_bool=simp_sub_bool)
    except Exception as e:
        return str(e)

@app.route('/notifications/',methods=["GET","POST"])
def notf():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    try:

        username = session['username']
        notfplanbool = True
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        notfplan = [item1[10] for item1 in c.fetchall()]
        notfplan = notfplan[0].split(";")
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        notfuserplan = [item1[11] for item1 in c.fetchall()]
        notfuserplan = notfuserplan[0].split(";")
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        lenotf = len(notfplan)
        if lenotf==1:
            notfplanbool = False


        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        subs = [item1[8] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        subs = subs[0].split(';')
        subs.pop(len(subs)-1)
        acv_acv = [""]
        acv_place= [""]

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
        user_acv_current = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
        user_place_current = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(username,))
        user_city_current = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s",(user_acv_current,))
        matched_acv_username = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s",(user_acv_current,))
        matched_acv_acv = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s",(user_acv_current,))
        matched_acv_place = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE place=%s",(user_place_current,))
        matched_place_username = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE place=%s",(user_place_current,))
        matched_place_acv = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE place=%s",(user_place_current,))
        matched_place_place = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s AND place=%s",(user_acv_current,user_place_current,))
        matched_city_username = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s AND place=%s",(user_acv_current,user_place_current,))
        matched_city_acv = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE acv=%s AND place=%s",(user_acv_current,user_place_current,))
        matched_city_place = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        for item in subs:
            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(item,))
            acv_acv.append(str(([item1[2] for item1 in c.fetchall()])[0]))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM acvtab WHERE username=%s",(item,))
            acv_place.append(str(([item1[3] for item1 in c.fetchall()])[0]))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
        notf_bool = False
        if len(acv_acv)>1:
            notf_bool=True
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        if len(matched_acv_username)>0:
            notf_bool = True
        if len(matched_place_username)>0:
            notf_bool = True
        if len(matched_city_username)>0:
            notf_bool = True

        return render_template("notf.html",notfplanbool=notfplanbool,lenotf=lenotf,notfplan=notfplan,notfuserplan=notfuserplan,username=username,name=name,matched_city_place=matched_city_place,matched_city_username=matched_city_username,matched_city_acv=matched_city_acv,matched_place_username=matched_place_username,matched_place_acv=matched_place_acv,matched_place_place=matched_place_place,matched_acv_username=matched_acv_username,matched_acv_acv=matched_acv_acv,matched_acv_place=matched_acv_place,email=email,website=website,desc=desc,mobile=mobile,notf_bool=notf_bool,acv_acv=acv_acv,acv_place=acv_place,le=len(acv_acv),le2=len(matched_acv_username),le3=len(matched_place_username),le4=len(matched_city_username),subs=subs)
    except Exception as e:
        return str(e)

@app.route('/getimgdp')
def getimgdp():
    filename = str(request.args.get('username_dp'))+"dp"+".jpg"
    if os.path.isfile(app.config['UPLOAD_FOLDER']+str(request.args.get('username_dp'))+"dp"+".jpg"):
        indicator = "no problem lulz"
    else:
        filename = "defaultdp.jpg"
    return send_file(filename)

@app.route('/getimgcover')
def getimgcover():
    filename = str(request.args.get('username_cover'))+"cover"+".jpg"
    if os.path.isfile(app.config['UPLOAD_FOLDER']+str(request.args.get('username_cover'))+"cover"+".jpg"):
        indicator = "no problem lulz"
    else:
        filename = "defaultcover.jpg"
    return send_file(filename)
@app.route('/makeplan')
def makeplan():
    try:
        user1 = str(session['username'])
        user2 = request.args.get('username',type=str)
        planid = request.args.get('id',type=str)
        c, conn = connection()
        c.execute("SELECT * FROM planner WHERE id=%s",(planid,))
        d1 = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM planner WHERE id=%s",(planid,))
        l1 = [item1[2] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM planner WHERE id=%s",(planid,))
        c1 = [item1[3] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM planner WHERE id=%s",(planid,))
        i1 = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        notf = str(d1[0]) + " @ " + str(l1[0]) + ", "+str(c1[0])+" ( "+str(i1[0])+" )"+";"
        notfuser = str(user1)+";"
        c, conn = connection()
        c.execute("UPDATE users SET notifications=CONCAT(notifications,(%s)),notfuser=CONCAT(notfuser,(%s)) WHERE username=(%s)",(notf,notfuser,user2,))
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return str(e)

@app.route('/planner')
def planner():
    try:
        if session['logged_in']==False:
            return redirect("http://s1mple.pythonanywhere.com")
    except Exception as e:
        return redirect("http://s1mple.pythonanywhere.com")
    try:
        username = session['username']
        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        name = [item1[1] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        email = [item1[4] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        website = [item1[6] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        desc = [item1[7] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(username,))
        mobile = [item1[5] for item1 in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        user1 = str(session['username'])
        user2 = request.args.get('username',type=str)

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(user1,))
        interests1 = [item1[9] for item1 in c.fetchall()]
        interests1 = interests1[0].split(";")
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM users WHERE username=%s",(user2,))
        interests2 = [item1[9] for item1 in c.fetchall()]
        interests2 = interests2[0].split(";")
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(user1,))
        locality1 = [item1[4] for item1 in c.fetchall()]
        locality1 = locality1[0]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(user2,))
        locality2 = [item1[4] for item1 in c.fetchall()]
        locality2 = locality2[0]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(user1,))
        city1 = [item1[5] for item1 in c.fetchall()]
        city1 = city1[0]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        c, conn = connection()
        c.execute("SELECT * FROM acvtab WHERE username=%s",(user2,))
        city2 = [item1[5] for item1 in c.fetchall()]
        city2 = city2[0]
        conn.commit()
        c.close()
        conn.close()
        gc.collect()
        common = []
        for item1 in interests1:
            for item2 in interests2:
                if item1==item2:
                    common.append(item1)
        interests = []
        destinations = []
        city = []
        locality = []
        idp = []
        for item in common:
            c, conn = connection()
            c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            d1 = [item1[4] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            idp1 = [item1[0] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            l1 = [item1[2] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            c1 = [item1[3] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            x=c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

            c, conn = connection()
            c.execute("SELECT * FROM planner WHERE interests=%s",(item,))
            i1 = [item1[1] for item1 in c.fetchall()]
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            if int(x)>0:
                destinations.extend(d1)
                interests.extend(i1)
                city.extend(c1)
                locality.extend(l1)
                idp.extend(idp1)
            le = len(interests)
        return render_template("planner.html",idp=idp,locality=locality,city=city,le=le,user2=user2,username=username,name=name,email=email,website=website,desc=desc,mobile=mobile,destinations=destinations,interests=interests)
    except Exception as e:
        return str(e)
@app.route('/social_intro')
def social_intro():
    return render_template("social_intro.html")
@app.route('/view_intro')
def view_intro():
    return render_template("view_intro.html")
@app.route('/nearby_intro')
def nearby_intro():
    return render_template("nearby_intro.html")
@app.route('/health_intro')
def health_intro():
    return render_template("health_intro.html")
@app.route('/enterprise_intro')
def enterprise_intro():
    return render_template("enterprise_intro.html")
