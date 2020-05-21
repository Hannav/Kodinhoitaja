from flask import render_template
from application import app
from application.auth.models import User
from flask_login import login_required, current_user

@app.route('/')
@login_required
def index():
    return render_template("index.html", needs_tasks=User.find_users_with_no_tasks())