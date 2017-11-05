from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    '''
    Define Role model
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                            lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class User(db.Model, UserMixin):
    '''
    Define User model
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    user_pwd = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # Define Relationships
    blogsections = db.relationship(
        'Blogsection', backref='user', lazy='dynamic')
    posts = db.relationship(
        'Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        '''
        prevent password from being accessed
        '''
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        '''
        Set password to a hashed password
        '''
        self.user_pwd = generate_password_hash(password)

    def verify_password(self, password):
        '''
        check if hashed pwd matches actual pwd
        '''
        return check_password_hash(self.user_pwd, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Reader: {}>'.format(self.username)

    # set up user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Blogsection(db.Model):
    '''
    create blog section table
    '''
    __tablename__ = 'blogsections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    user_id = db.Column(db.ForeignKey('users.id'))

    # Define Relationships
    posts = db.relationship('Post', backref='blogsection', lazy='dynamic')

    def save_blogsection(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogsections(cls):
        all_blogsections = Blogsection.query.all()
        return all_blogsections

    def __repr__(self):
        return '<Blog Section: {}>'.format(self.name)


class Post(db.Model):
    '''
    create blog posts table
    '''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.String())
    user_id = db.Column(db.ForeignKey('users.id'))
    section_id = db.Column(db.ForeignKey('blogsections.id'))

    # Define Relationships
    comments = db.relationship('Comment', backref='post',
                               lazy='dynamic')

    def __repr__(self):
        return '<Post: {}'.format(self.title)


class Comment(db.Model):
    '''
    create comments table
    '''
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String())
    user_id = db.Column(db.ForeignKey('users.id'))
    post_id = db.Column(db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Comment: {}'.format(self.description)
