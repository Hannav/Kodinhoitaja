from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.datastructures import MultiDict

from application import app, db
from application.tasks.models import Task
from application.tasks.forms import TaskForm, OperationForm

@app.route("/tasks/", methods=["GET"])
@login_required
def tasks_index():
    return render_template("tasks/list.html", tasks = Task.query.order_by(Task.id.asc()).all())

@app.route("/tasks/new/")
@login_required
def tasks_form():
    return render_template("tasks/new.html", form = TaskForm())

@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_operation(task_id):

    form = OperationForm(request.form)
    t = Task.query.get(task_id)
    
    if not form.validate():
        print("ERROR: OPERATIONFORM ERROR")
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
        return redirect(url_for("tasks_index"))

    if form.data["operation"] == 'Muokkaa':
        Task.modify_task(task_id, form.data["name"])
        db.session().commit()
        print("MUOKKAA")

    return redirect(url_for("tasks_index"))

@app.route("/tasks/<task_id>/", methods=["GET"])
@login_required
def tasks_modify(task_id):
    
    task = Task.query.get(task_id)
    return render_template("tasks/modify.html", form = TaskForm(MultiDict([('name', task.name), ('done', task.done)])), task_id=task_id)

@app.route("/tasks/", methods=["POST"])
@login_required
def tasks_create():
    form = TaskForm(request.form)
  
    if not form.validate():
        return render_template("tasks/new.html", form = form)
  
    t = Task(form.name.data)
    t.done = form.done.data
    t.account_id = current_user.id
  
    db.session().add(t)
    db.session().commit()
  
    return redirect(url_for("tasks_index"))