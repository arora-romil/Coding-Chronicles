from flask import Flask , render_template, request,session,redirect,flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import math
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'super-secret-key'
with open ('config.json', "r") as c:
    params = json.load(c)["params"]
local_server = True
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_uname'],
    MAIL_PASSWORD = params['gmail_pass']
)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_URI']

with app.app_context():
    db = SQLAlchemy(app)

class Contacts(db.Model):
    SerialN = db.Column(db.Integer, default = 0 ,primary_key = True)
    Name = db.Column(db.String(80),nullable = False)
    Email = db.Column(db.String(20), nullable = False)
    PhoneNum = db.Column(db.String(12), nullable = False)
    Message = db.Column(db.String(120), nullable = False)
    Date = db.Column(db.String(12), nullable = True)

class Posts(db.Model):
    sno = db.Column(db.Integer, default = 0 ,primary_key = True)
    title = db.Column(db.String(80),nullable = False)
    slug = db.Column(db.String(20), nullable = False)
    content = db.Column(db.String(120), nullable = False)
    date = db.Column(db.String(12), nullable = True)
    img_file = db.Column(db.String(25), nullable = True)
    tagline = db.Column(db.String(25), nullable = True)

@app.route('/')
def index():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    
    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)

@app.route('/index')
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html',params = params, posts = posts)

@app.route('/about')
def about():
    return render_template('about.html',params = params)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    posts = Posts.query.all()
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard.html',params=params,posts = posts)
    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_pass']):
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html',params=params, posts = posts)
    
    return render_template('login.html',params = params)

@app.route('/post/<string:post_slug>', methods = ['GET'])

def post_show(post_slug):

    post = Posts.query.filter_by(slug = post_slug).first()

    return render_template('post.html',params = params,post = post)

@app.route('/edit/<string:sno>', methods = ['GET','POST'])

def edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            box_title = request.form.get('title')
            tline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno == '0':
                post = Posts(title= box_title,slug = slug, content = content, tagline = tline, img_file = img_file,date= date)
                db.session.add(post)
                db.session.commit()
                flash("Your Post Has Been Added!", "success")

            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.tagline = tline
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
                flash("Your Post Has Been Edited!", "success")
                return redirect('/edit/'+sno)
                # return redirect('/dashboard')
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params = params,date = datetime.now(),post = post,sno = sno)

@app.route('/delete/<string:sno>', methods = ['GET','POST'])
def delete(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        flash("Your Post Has Been Deleted!", "danger")
        return redirect('/dashboard')
@app.route('/uploader', methods = ['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if (request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "UPLOADED Successfully"

@app.route('/logout')

def logout():
    session.pop('user')
    return redirect('/')

@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(Name = name,Email = email,PhoneNum = phone,Message = message,Date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New Message from' + name , sender = email, recipients = [params['gmail_uname']],
                        #   body = message + "\n" + phone )
        flash("Thanks for submitting your message, We will get back to you soon!", "success")

    return render_template('contact.html',params = params)



if __name__ == "__main__":
    app.run(debug = True)

