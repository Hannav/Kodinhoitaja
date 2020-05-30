from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SelectField

class TaskForm(FlaskForm):
    name = StringField("Pakattava", [validators.Length(min=2)])
    done = BooleanField("Pakattu")
  
    class Meta:
        csrf = False

class TaskOperationForm(FlaskForm):
    operation = SelectField(u'Operation', choices=[('Muuta status', 'Muuta status'), ('Poista', 'Poista'), ('Muokkaa', 'Muokkaa')])
    name = StringField("Pakattava", [validators.Length(min=2)])

    class Meta:
        csrf = False

class TripForm(FlaskForm):
    name = StringField("Matkan nimi", [validators.Length(min=2)])

    class Meta:
        csrf = False

class TripOperationForm(FlaskForm):
    operation = SelectField(u'Operation', choices=[('Muokkaa osallistujia', 'Muokkaa osallistujia'), ('Poista', 'Poista'), ('Muokkaa nimeä', 'Muokkaa nimeä')])
    name = StringField("Matka", [validators.Length(min=2)])

    class Meta:
        csrf = False

class TripParticipantForm(FlaskForm):
    participant_id = StringField("Osallistuja")
  
    class Meta:
        csrf = False