from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BlogSectionForm(FlaskForm):
    '''
    Form for admin to add, edit, delete department
    '''
    name = StringField('Blog Section', validators=[DataRequired()])
    submit = SubmitField('Submit')
