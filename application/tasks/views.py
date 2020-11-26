from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_

from application import app, db
from application.tasks.models import Task, Trip, TripParticipant
from application.tasks.forms import TaskForm, TaskOperationForm, TripForm, TripOperationForm, TripParticipantForm
from application.auth.models import User

@app.route("/trips/", methods=["GET"])
@login_required
def tasks_index():
    return redirect(url_for("index"))

@app.route("/trips/<trip_id>/tasks/new/")
@login_required
def tasks_form(trip_id):
    return render_template("tasks/new.html", form = TaskForm(), trip_id=trip_id)

@app.route("/trips/<trip_id>/participants/new/")
@login_required
def trip_participants_form(trip_id):
    return render_template("trip_participants/new.html", form = TripParticipantForm(), trip_id=trip_id)

@app.route("/participant/<participant_id>/delete/", methods=["POST"])
@login_required
def participant_delete(participant_id):

    participant = TripParticipant.query.get(participant_id)
    if participant.trip.owner_id != current_user.id:
        return "Ei onnistu"

    db.session().delete(participant)

    db.session().commit()

    return redirect(url_for("trip_details", trip_id=participant.trip.id))

@app.route("/trips/<trip_id>/participants/new/", methods=["POST"])
@login_required
def participants_add(trip_id):
    form = TripParticipantForm(request.form)
    trip = Trip.query.get(trip_id)

    if request.method=="POST" and form.validate():
        user = User.query.filter_by(username=form.participant_id.data).first()
        if TripParticipant.query.filter_by(participant=user, trip=trip).count():
            return redirect(url_for("trip_details", trip_id=trip_id))
        t = TripParticipant(user.id, trip_id)
        t.account_id = current_user.id
  
        db.session().add(t)
        db.session().commit()
    
        return redirect(url_for("trip_details", trip_id=trip_id))

    return render_template("trip_participants/new.html", form = form, trip_id=trip_id)

@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_operation(task_id):

    form = TaskOperationForm(request.form)
    t = Task.query.get(task_id)
    print(t.trip_id)
    
    if not form.validate():
        print("ERROR: *TASK*OPERATIONFORM ERROR")
        print(form.data)
        print(form.errors)

    print(form.data)
    if form.data["operation"] == 'Muuta status':
        print(t.done)
        if t.done == True:
            Task.booleanToFalse_task(task_id)
        else:
            Task.booleanToTrue_task(task_id)
        db.session().commit()

    if form.data["operation"] == 'Poista':
        Task.delete_task(task_id)

    if form.data["operation"] == 'Muokkaa':
        Task.modify_task(task_id, form.data["name"])
        db.session().commit()
        print("MUOKKAA")

    return redirect(url_for("trip_details", trip_id=t.trip_id))

@app.route("/tasks/<task_id>/", methods=["GET"])
@login_required
def tasks_modify(task_id):
    
    task = Task.query.get(task_id)
    return render_template("tasks/modify.html", form = TaskForm(MultiDict([('name', task.name), ('done', task.done)])), task_id=task_id)

@app.route("/trips/<trip_id>/tasks/new/", methods=["POST"])
@login_required
def tasks_create(trip_id):
    form = TaskForm(request.form)
  
    if not form.validate():
        return render_template("tasks/new.html", form=form, trip_id=trip_id)
  
    t = Task(form.name.data, trip_id)
    t.done = form.done.data
    t.account_id = current_user.id
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("trip_details", trip_id=trip_id))

@app.route('/')
@login_required
def index():
    trips = Trip.query.filter(or_(Trip.owner_id==current_user.id,Trip.participants.any(TripParticipant.participant_id==current_user.id)))
    return render_template("index.html", trips=trips.order_by(Trip.date_modified.desc()))

@app.route("/trips/new/")
@login_required
def trip_form():
    return render_template("trips/new.html", form = TripForm())

@app.route("/trips/", methods=["POST"])
@login_required
def trips_create():
    form = TripForm(request.form)
  
    if not form.validate():
        return render_template("trips/new.html", form = form)
  
    t = Trip(form.name.data)
    t.owner_id = current_user.id
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("index"))

@app.route("/trips/<trip_id>/", methods=["GET"])
@login_required
def trip_details(trip_id):

    t = Trip.query.get(trip_id)
    if t is None:
        return redirect(url_for("index"))
    tasks = Task.query.filter_by(trip_id=t.id).all()
    trip_participants = TripParticipant.query.filter_by(trip_id=t.id).all()
    is_owner = current_user.id == t.owner_id
    return render_template(
        "trips/details.html", trip=t, tasks=tasks, trip_participants=trip_participants,
        is_owner=is_owner
    )

@app.route("/trips/<trip_id>/delete/", methods=["POST"])
@login_required
def trip_delete(trip_id):

    trip = Trip.query.get(trip_id)
    if trip.owner_id != current_user.id:
        return "Ei onnistu"

    session = db.session()
    session.query(Task).filter(Task.trip_id==trip.id).delete()
    session.delete(trip)

    session.commit()

    return redirect(url_for("index"))