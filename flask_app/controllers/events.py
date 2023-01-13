from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.User import User
from flask_app.models.Event import Event, Event_nouserid
from flask_app.models.Friend import Friend
from flask_app.models.Status import Status

### RENDERING METHODS ###

@app.route('/new-event')
def newevent():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        print('test')
        return redirect('/')
    user = User.get_by_id(session['user_logged_in']['id'])
    print(user)
    return render_template('create_event.html', user=user)

@app.route('/eventinfo/<int:event_id>')
def eventinfo(event_id):
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_logged_in']['id'])
    event = Event.get_by_id(event_id)
    party = Event.get_joined_users(event_id)
    print(event_id)
    return render_template('event_info.html', user=user, event = event, party = party)

@app.route('/event-list')
def eventlist():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_logged_in']['id'])
    events = Event.get_all_events()
    hosts = Event.get_events_with_og_hosts()
    previous_event = events[0].id-1
    print('A', previous_event)
    distinct_events = []
    for event in events:
        print('B', previous_event)
        print('C', event.id)
        if event.id != previous_event:
            distinct_events.append(event)
        previous_event = event.id
    return render_template('events.html', user=user, events=distinct_events, hosts=hosts)

@app.route('/confirm_event')
def confirm_event():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    user = User.get_by_id(session['user_logged_in']['id'])
    events = Event_nouserid.get_most_recent_event()
    return render_template('confirm_event.html', user=user, events=events)


### POST METHODS ###

@app.route('/event', methods=['POST'])
def f_create_a_event():
    if 'user_logged_in' not in session:
        # flash("You must be logged in to edit a user's account.")
        return redirect('/')
    print('Printing data entered in event form')
    print(request.form)
    valid_event = Event.create_valid_event(request.form)
    if not valid_event:
        return redirect('/new-event')
    return redirect('/confirm_event') 
    
@app.route('/join_event', methods=['POST'])
def join_event():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    print(f"Priting join_event method {request.form}")
    Event.join_event(request.form)
    return redirect('/dashboard')

@app.route('/leave_event', methods=['POST'])
def leave_event():
    if 'user_logged_in' not in session:
        flash("You must be logged in to edit a user's account.")
        return redirect('/')
    Event.leave_event(request.form)
    return redirect('/event-list')

# When creating the form for the Join or leave routes this is the form i created in my solo for reference:

# <td>
#     <form action="/join_event" method="post">
#         <input type="hidden" value="{{session['user_logged_in']}}" name="user_logged_in">
#         <input type="hidden" value="{{event.id}}" name="event_id">
#         <input type="submit" value="Join">
#     </form>
# </td>


# <form action="/leave_event" method="post">
#     <input type="hidden" value="{{session['user_logged_in']}}" name="user_logged_in">
#     <input type="hidden" value="{{event.id}}" name="event_id">
#     <input type="submit" value="Leave">
# </form>

