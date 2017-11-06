from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Blogsection, Post


class BlogSectionForm(FlaskForm):
    '''
    Form for admin to add, edit, delete blog section
    '''
    name = StringField('Blog Section', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BlogPostForm(FlaskForm):
    '''
    Form for admin to add, edit, delete blogposts
    '''

    title = StringField('Post Title', validators=[DataRequired()])
    description = StringField('Write Post Here', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BlogpostAssignForm(FlaskForm):
    '''
    Form for admin to assign ablog section to a post
    '''
    blogsection = QuerySelectField(
        query_factory=lambda: Blogsection.query.all(),
        get_label="name")
    submit = SubmitField('Assign')


class CommentForm(FlaskForm):
    '''
    Form for admin to add, edit, delete blog section
    '''
    description = StringField('Leave a comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
