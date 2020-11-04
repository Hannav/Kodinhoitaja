from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SelectField
from wtforms.validators import ValidationError
from application.auth.models import User

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

    def validate_participant_id(form, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError("Käyttäjää ei löydy!")
