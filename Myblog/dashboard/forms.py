from flask_wtf import FlaskForm
from wtforms import StringField ,BooleanField, SubmitField ,TextAreaField
from Myblog.validators import DataRequired ,InputRequired ,Regexp, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from Myblog.models import Post , Catogary
from Myblog import db

def catogaries_choices():      
    return db.session.query(Catogary)


class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    slug = StringField('Slug',validators=[DataRequired(),Regexp('[a-z](-?[a-z])',flags=0)])
    content = TextAreaField('Content')
    catogary = QuerySelectField('Catogary',query_factory=catogaries_choices)
    save_post = SubmitField('Save Post')

    def Validate_slug(self,username):
        post = Post.query.filter_by(slug=slug).first() 
        if user:
            raise ValidationError('The slug already exists.')

