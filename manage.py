import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# Import from main/__init__.py
from main import create_app, db
# Import models from main/model/main_model.py
from main.model.main_model import VadrRun
from __init__ import blueprint

# Creates app using enviornment variable
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()