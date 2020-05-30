from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.datastructures import MultiDict

from application import app, db
from application.tasks.models import Task, Trip
from application.tasks.forms import TaskForm, TaskOperationForm, TripForm, TripOperationForm

@app.route("/trips/", methods=["GET"])
@login_required
def tasks_index():
    return redirect(url_for("index"))

@app.route("/trips/<trip_id>/tasks/new/")
@login_required
def tasks_form(trip_id):
    return render_template("tasks/new.html", form = TaskForm(), trip_id=trip_id)

@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_operation(task_id):

    form = TaskOperationForm(request.form)
    t = Task.query.get(task_id)
    print("MUUMI")
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
        return render_template("tasks/new.html", form = form)
  
    t = Task(form.name.data, trip_id)
    t.done = form.done.data
    t.account_id = current_user.id
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("trip_details", trip_id=trip_id))

@app.route('/')
@login_required
def index():
    return render_template("index.html", trips=Trip.query.order_by(Trip.date_modified.desc()).all())

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

# ei toimi
@app.route("/trips/<trip_id>/", methods=["GET"])
@login_required
def trip_details(trip_id):

    t = Trip.query.get(trip_id)
    if t is None:
        return redirect(url_for("index"))
    tasks = Task.query.filter_by(trip_id=t.id).all()
    return render_template("trips/details.html", trip=t, tasks=tasks)

    form = TripOperationForm(request.form)
    
    if not form.validate():
        print("ERROR: *TRIP*OPERATIONFORM ERROR")
        print(form.data)
        print(form.errors)

#tätä ei ole vielä olemassa eikä toimi
    print(form.data)
    if form.data["operation"] == 'Muokkaa osallistujia':
        Trip.participants_trip(trip_id)
        db.session().commit()
        return redirect(url_for("index"))

#tehdäkö boolean kuten taskissa:
#   print(form.data)
#    if form.data["operation"] == 'Osallistuuko':
#        print(t.done)
#        if t.done == True:
#            Task.booleanToFalse_trip(trip_id)
#        else:
#            Task.booleanToTrue_trip(trip_id)
#        db.session().commit()

    if form.data["operation"] == 'Poista':
        Trip.delete_trip(trip_id)
        return redirect(url_for("trips_index"))

    if form.data["operation"] == 'Muokkaa nimeä':
        Trip.modify_trip(trip_id, form.data["name"])
        db.session().commit()
        print("MUOKKAA")

    return redirect(url_for("trips_index"))