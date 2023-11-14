from flask import request, Response, render_template
from flask import Blueprint
from flask import jsonify
from flask import Flask,redirect
from mainapp.services import reader_svc

readerapp = Blueprint( 'readerroutes', __name__,
                      static_folder='static',
                      template_folder='templates')

@readerapp.route('/home', methods= ['GET', 'POST'])
def credits_reading():

  faculty_id = 2

  my_reading_list = reader_svc.retrieve_applications_reading(faculty_id_number=faculty_id)

  return render_template( 'readerhome.html', my_reading_list=my_reading_list)


@readerapp.route('/submit_feedback', methods= ['GET', 'POST'])
def submit_feedback():

  is_get = request.method == 'GET'

  pkid = request.args.get( 'pkid' ) if is_get else request.form.get( 'pkid' )

  return render_template('submit_feedback.html', pkid=pkid)

@readerapp.route('/provide_feedback', methods= ['GET', 'POST'])
def root_provide_feedback():

  is_get = request.method == 'GET'

  pkid = request.args.get( 'pkid' ) if is_get else request.form.get( 'pkid' )
  feedback = request.args.get( 'feedback' ) if is_get else request.form.get( 'feedback' )
  is_earned = request.args.get( 'is_earned' ) if is_get else request.form.get( 'is_earned' )

  reader_svc.update_credit_app( app_pkid=pkid, app_is_earned=is_earned, app_feedback=feedback )
  
  
  return redirect('/reader/home')

@readerapp.route('/previous', methods= ['GET', 'POST'])
def see_previous_feedback():

  is_get = request.method == 'GET'

  decision = request.args.get( 'decision' ) if is_get else request.form.get( 'decision' )
  credit = request.args.get( 'credit_id' ) if is_get else request.form.get( 'credit_id' )

  previous_applications_list = reader_svc.previous_apps(credit_id=credit, decision=decision)
  credits_list = reader_svc.credits_list()
  
  
  return render_template('previous_feedback.html', decision=decision, previous_applications_list=previous_applications_list, credits_list=credits_list)