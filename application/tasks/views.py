from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Task
from application.tasks.forms import TaskForm, OperationForm


@app.route("/tasks/", methods=["GET"])
@login_required
def tasks_index():
    return render_template("tasks/list.html", tasks = Task.query.all())

@app.route("/tasks/new/")
@login_required
def tasks_form():
    return render_template("tasks/new.html", form = TaskForm())

#@app.route("/tasks/modify/")
#@login_required
#def tasks_modify(task_id):
#    return render_template("tasks/modify.html", form = TaskForm())

@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_operation(task_id):

    form = OperationForm(request.form)
    
    if not form.validate():
        print("ERROR: OPERATIONFORM ERROR")
        print(form.data)
        print(form.errors)
        return redirect(url_for("tasks_index"))

    print(form.data)
    if form.data["operation"] == 'Muuta status':
        print("MUUTA STATUS")

    if form.data["operation"] == 'Poista':
        Task.delete_task(task_id)

    if form.data["operation"] == 'Muokkaa':
        print("MUOKKAA")
    
    return redirect(url_for("tasks_index"))

#Miten saa tasks_delete, tasks_set_done (tai statuksen jatkuva vaihto), tasks_modify toimimaan molemmat?

#@app.route("/tasks/<task_id>/", methods=["POST"])
#@login_required
#def tasks_boolean(task_id):
#
#    Task.boolean_task(task_id)
#  
#    return redirect(url_for("tasks_index"))

#@app.route("/tasks/<task_id>/", methods=["POST"])
#@login_required
#def tasks_set_done(task_id):
#muuta tasks_set_booleaniksi

#    t = Task.query.get(task_id)
#    t.done = True
#    db.session().commit()
#  
#    return redirect(url_for("tasks_index"))

"""@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_modify(task_id):

    Task.modify_task(task_id)
    
    return redirect(url_for("tasks_index"))"""

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