from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SelectField

class TaskForm(FlaskForm):
    name = StringField("Pakattava", [validators.Length(min=2)])
    done = BooleanField("Pakattu")
  
    class Meta:
        csrf = False

class OperationForm(FlaskForm):
    operation = SelectField(u'Operation', choices=[('Muuta status', 'Muuta status'), ('Poista', 'Poista'), ('Muokkaa', 'Muokkaa')])

    class Meta:
        csrf = False