from flask import Blueprint,request,flash,redirect,url_for
from flask.templating import render_template
from flask_login.utils import login_required, logout_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from . import db
auth = Blueprint('auth', __name__)

def login():
    email = request.form.get('email2')
    password = request.form.get('password')

    user= User.query.filter_by(email=email).first()


    if user:
        if check_password_hash(user.password, password):            
            login_user(user, remember=True)
            return redirect('/')
        else:
            #wrong password
            return render_template('index.html',user=current_user)
    else:
        #wrong email
        return render_template('index.html',user=current_user)
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/welcome')

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    email = request.form.get('email')
    schoolClass = request.form.get('schoolClass')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')        
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email already exists in the system.', category='error')
        return render_template("index.html", user=current_user)
    else:
        wrong = False
        if len(email)<4:
            wrong=True
            #Email must be greater than 3 characters
        if len(schoolClass)<2:
            wrong=True
            #First name must be greater than 1 characters
        if len(password1)<7:
            wrong=True
            #Password must be at least 7 characters.
        if password1 !=password2:
            wrong=True
            #Passwords don\'t match.
        if not wrong:
            new_user = User(email=email, schoolClass=schoolClass, password=generate_password_hash(password1, method='sha256'),last_date='')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

