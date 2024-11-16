from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class UserProfileForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                       Length(min=3, max=20), 
                                       Regexp('^[A-Za-z0-9]*$', message='Only alphanumeric characters are allowed.')])
    profile_picture = FileField('Profile Picture', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    text = TextAreaField('Text', validators=[DataRequired(), Length(min=10)])
    image = FileField('Post Image')
    submit = SubmitField('Submit Post')
