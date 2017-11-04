from . import db
from flask_user import UserMixin


# Define Role model


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)  # for @roles_accepted()
    # for display purposes
    label = db.Column(db.Unicode(255), server_default=u'')

# Define User model


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    # User Authentication info required for flask_user
    username = db.Column(db.String(256), nullable=True, unique=True)
    email = db.Column(db.String(255), unique=True, index=True)
    confirmed_at = db.Column(db.DateTime())
    user_pwd = db.Column(db.String(255))
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    status = db.Column(db.String(255))
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('You can read the password attribute')

    @password.setter
    def password(self, password):
        self.user_pwd = hash_password(password)


# Define UserRoles model


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))
