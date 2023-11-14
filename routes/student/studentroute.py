from flask import request, Response, render_template
from flask import Blueprint
from flask import jsonify
from mainapp.services import student_svc
from flask import redirect

student_pkid = 4

studentapp = Blueprint( 'studentroutes', __name__,
                      static_folder='static',
                      template_folder='templates')

@studentapp.route('/', methods= ['GET', 'POST'])
def student_test():
  return redirect('student/home')

@studentapp.route('/home', methods= ['GET', 'POST'])
def student_submit():
  results = student_svc.credits_status(4)
  print(results)
  return render_template('submit.html', results=results)

@studentapp.route('/submit_application', methods= ['GET', 'POST'])
def submit_application():
    
  is_get = request.method == 'GET'

  credit_id = request.args.get( 'credit_id' ) if is_get else request.form.get( 'credit_id' )
  credit_name = request.args.get( 'credit_name' ) if is_get else request.form.get( 'credit_name' )

  courses_list = student_svc.courses()

  return render_template('submit_application.html', credit_id=credit_id, credit_name=credit_name, courses_list=courses_list)

@studentapp.route('/send_application', methods= ['GET', 'POST'])
def send_application():

  is_get = request.method == 'GET'

  rationale = request.args.get( 'rationale' ) if is_get else request.form.get( 'rationale' )
  top_course = request.args.get( 'top_course' ) if is_get else request.form.get( 'top_course' )
  credit_id = request.args.get( 'credit_id' ) if is_get else request.form.get( 'credit_id' )

  app_cycle_title = 'fall2023'
  app_cycle_date = '20231018'
  date_submitted = '20231016'
  

  student_svc.submit_application( app_student_pkid=student_pkid, app_credit_id=credit_id,
                                 app_rationale=rationale, app_app_cycle_title=app_cycle_title,
                                 app_app_cycle_date=app_cycle_date, app_date_submitted=date_submitted,
                                 app_status='Unreviewed', app_top_course=top_course)
  return redirect('/student/home')


@studentapp.route('/previous_submission', methods= ['GET', 'POST'])
def submission_history():
    
  is_get = request.method == 'GET'

  credit_id = request.args.get( 'credit_id' ) if is_get else request.form.get( 'credit_id' )
  credit_name = request.args.get( 'credit_name' ) if is_get else request.form.get( 'credit_name' )
  
  my_applications = student_svc.credit_history(credit_id=credit_id, student_pkid=student_pkid)


  return render_template('view_history.html', my_applications=my_applications, credit_name=credit_name)