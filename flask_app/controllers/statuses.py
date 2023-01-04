from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Event import Event
from flask_app.models.Friend import Friend
from flask_app.models.Status import Status, Status_getall

## POST METHODS ##

@app.route('/create_new_status', methods=['POST'])
def create_new_status():
    if 'user_logged_in' not in session:
        return redirect('/')
    print(request.form)
    valid_status = Status.create_status(request.form)
    if valid_status:
        return redirect('/dashboard')
    # need an else for a different end to this function, not just redirect dashboard again. 
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_status(id):
    if 'user_logged_in' not in session:
        return redirect('/')
    Status_getall.delete_status({'id':id})
    return redirect('/dashboard')