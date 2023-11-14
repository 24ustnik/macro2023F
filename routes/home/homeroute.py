from flask import request, Response, render_template
from flask import Blueprint
from flask import jsonify

homeapp = Blueprint( 'homeapp', __name__, 
                      static_folder='static',
                      template_folder='templates')

@homeapp.route('/', methods= ['GET', 'POST'])
def home_default_fn():
  return render_template("fake_log-in.html")