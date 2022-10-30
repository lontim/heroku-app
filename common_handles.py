from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_moment import Moment


# Create "central" handles for database and migration, but don't instantiate yet

db = SQLAlchemy()
migrate = Migrate()
# moment = Moment()

