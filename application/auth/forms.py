from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False

class CreateForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.Length(min=2)])
    password = PasswordField("Salasana", [validators.Length(min=2)])
  
    class Meta:
        csrf = False