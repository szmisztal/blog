from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from blog import routes, models

def db_init():
    db.create_all()
    migrate.stamp()

@app.cli.command()
def db_migrate():
    migrate.init()
    migrate.migrate()
    migrate.upgrade()

@app.before_first_request
def before_first_request():
    db_init()
    db_migrate()

@app.shell_context_processor
def make_shell_context():
  return {
      "db": db,
      "Entry": models.Entry
  }
