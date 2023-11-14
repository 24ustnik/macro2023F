from flask import request, Response, render_template
from flask import Blueprint
from flask import jsonify
from flask import redirect

defaultapp = Blueprint( 'defaultroutes', __name__,
                      static_folder='static',
                      template_folder='templates')

@defaultapp.route('/', methods= ['GET', 'POST'])
def home_redirect():
  return redirect('/home')