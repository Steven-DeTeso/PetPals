from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Event import Event
from flask_app.models.Status import Status, Status_getall
from flask_app.models.Friend import Friend

### RENDERING METHODS ###

@app.route('/')
def home():
    return render_template('Login_Page.html')

    
@app.route('/register')
def register():
    return render_template('Registration_Page.HTML')

@app.route('/register_user', methods = ['POST'])
def r_register_user():
    valid_user = User.create_user(request.form)
    if not valid_user:
        return redirect('/')
    session['user_id'] = valid_user.id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    valid_user = User.user_login_authentication(request.form)
    if not valid_user:
        return redirect('/')
    session['user_id'] = valid_user.id
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    events = Event.get_all_events()
    statuses = Status_getall.get_all_statuses()
    return render_template('dashboard.html', user=user, events=events, statuses=statuses)

@app.route('/profile')
def render_profile():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    events = Event.get_all_events()
    statuses = Status_getall.get_all_statuses()
    return render_template('profile.html', user=user, events=events, statuses=statuses)


### POST METHODS ###


@app.route("/update_User_account", methods=["POST"])
def update_user():
    if 'user_id' not in session:
        flash("You must be logged in to delete magazines.")
        return redirect('/') 
    valid_user = User.update_user_account(request.form, session["user_id"])
    # print(valid_user)
    if valid_user:
        return redirect(f"/user/account/")
    return redirect(f"/user/account/")
