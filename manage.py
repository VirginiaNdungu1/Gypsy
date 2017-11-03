from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Role, User, UserRoles
app = create_app('development')

# app = create_app('test')

# app = create_app('production')

# Initialise flask class instances
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('server', Server)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    '''
    Run unit tests
    '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, UserRoles=UserRoles)


if __name__ == '__main__':
    manager.run()
