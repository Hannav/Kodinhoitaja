from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class TaskForm(FlaskForm):
    name = StringField("Tehtävän nimi", [validators.Length(min=2)])
    done = BooleanField("Tehty")
  
    class Meta:
        csrf = False