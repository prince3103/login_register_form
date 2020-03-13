from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
        else:
            form.error_msg.label = 'Invalid Email Address or Password'
    else:
        for key in form.errors.keys():
            form.error_msg.label = form.errors[key][0]
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        check_email = form.check_email(form.email)
        check_username = form.check_username(form.username)    
        if check_email and check_username:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('login'))
        elif not check_email:
            flash('Your email has been registered already!')
            form.error_msg.label = 'Your email has been registered already!'
        else:
            flash('Sorry, that username is taken!')
            form.error_msg.label = 'Sorry, that username is taken!'
    else:
        for key in form.errors.keys():
            form.error_msg.label = form.errors[key][0]

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)
