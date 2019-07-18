#Author:xue yi yang
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length,DataRequired

class form_serch(FlaskForm):
    name = StringField(label="电影名",validators=[DataRequired(),Length(1,128)])