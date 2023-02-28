from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app.models.User import User
from flask_app.models.Event import Event
from flask_app.models.Friend import Friend
from flask_app.models.Status import Status

### RENDERING METHODS ###

@app.route('/friends')
def view_friends():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    friends = Friend.get_all_freinds_of_user(session['user_logged_in']['id'])
    user = User.get_by_id(session['user_logged_in']['id'])
    return render_template('friends.html', friends=friends, user=user)

### POST METHODS ###

@app.route('/add_friends', methods=['POST'])
def add_friends():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    Friend.add_friend(request.form)
    return redirect('/friends')
# May have to look into how this works with the add friend button we are gonna implement.
# For the way the request form is going to work we can have the id as hidden values then have it linked to a add friend button that will create the relationship for us by submitting the form and the informaiton into our query and thus the database.