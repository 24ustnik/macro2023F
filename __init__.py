from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ, path

db = SQLAlchemy()

def create_app():
  app=Flask( __name__, 
            template_folder='templates', 
            static_folder='static', 
            static_url_path='' )

  from .routes.default.defaultroute import defaultapp as default_blueprint
  from .routes.home.homeroute import homeapp as home_blueprint
  from .routes.admindy.admindyroute import admindyapp as admindy_blueprint
  from .routes.reader.readerroute import readerapp as reader_blueprint
  from .routes.student.studentroute import studentapp as student_blueprint
  
  app.register_blueprint( default_blueprint, url_prefix = '/' )
  app.register_blueprint( home_blueprint, url_prefix = '/home' )
  app.register_blueprint( admindy_blueprint, url_prefix='/admindy')
  app.register_blueprint( reader_blueprint, url_prefix='/reader')
  app.register_blueprint( student_blueprint, url_prefix='/student')

  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dappled:12345@10.18.161.6:3400/data_barely_knowa'

  db.init_app(app)

  return app