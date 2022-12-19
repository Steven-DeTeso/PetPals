from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Event import Event
from flask_app.models.Friend import Friend
from flask_app.models.Status import Status

### RENDERING METHODS ###

@app.route('/new-event')
def newevent():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    return render_template('CreateEvent.HTML', user=user)

@app.route('/eventinfo/<int:event_id>')
def eventinfo(event_id):
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    event = Event.get_by_id(event_id)
    return render_template('Event_Information.HTML', user=user, event = event)

@app.route('/event-list')
def eventlist():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    events = Event.get_all_events()
    return render_template('eventlist.HTML', user=user, events=events)



### POST METHODS ###

@app.route('/event', methods=['POST'])
def f_create_a_event():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    valid_event = Event.create_valid_event(request.form)
    if valid_event:
        return redirect(f'/dashboard')
    return redirect('/new-tournament')
    
@app.route('/join_event', methods=['POST'])
def join_event():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    Event.join_event(request.form)
    return redirect('/event-search')

@app.route('/leave_event', methods=['POST'])
def leave_event():
    if 'user_id' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    Event.leave_event(request.form)
    return redirect('/event-search')


