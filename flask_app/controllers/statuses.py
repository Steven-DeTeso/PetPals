from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Event import Event
from flask_app.models.Friend import Friend
from flask_app.models.Status import Status

## POST METHODS ##

@app.route('/create_new_status', methods=['POST'])
def create_new_status():
    if 'user_id' not in session:
        print('user not in session')
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    valid_status = Status.create_status(request.form)
    if valid_status:
        print('valid status')
        return redirect('/dashboard')
    return redirect('/dashboard')