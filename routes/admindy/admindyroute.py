from flask import request, Response, render_template
from flask import Blueprint
from flask import jsonify
from mainapp.services import admindy_svc
from flask import redirect

admindyapp = Blueprint( 'admindyroutes', __name__,
                      static_folder='static',
                      template_folder='templates')

@admindyapp.route('/', methods= ['GET', 'POST'])
def admindy_test():
  return 'This is the admindy route'

@admindyapp.route('/submissions', methods= ['GET', 'POST'])
def see_previous_feedback():

  is_get = request.method == 'GET'

  graduation_year = request.args.get( 'graduation_year' ) if is_get else request.form.get( 'graduation_year' )
  credit_id = request.args.get( 'credit_id' ) if is_get else request.form.get( 'credit_id' )

  previous_applications_list = admindy_svc.previous_apps(credit_id=credit_id, graduation_year=graduation_year)
  credits_list = admindy_svc.credits_list()

  print(previous_applications_list)
  
  return render_template('admin_home.html', credits_list=credits_list, my_applications=previous_applications_list)

@admindyapp.route('/asign_reader', methods= ['GET', 'POST'])
def admindy_asign_reader():

  credits_list = admindy_svc.credit_assigns()
  readers_list = admindy_svc.readers()
  
  return render_template("admin_assign_reader.html", credits_list=credits_list, readers_list=readers_list)

@admindyapp.route('/asign_time', methods= ['GET', 'POST'])
def admindy_asign_time():

  applications_list = admindy_svc.detailed_applications()
  readers_list = admindy_svc.readers()

  return render_template("admin_assign_panel_time.html", applications_list=applications_list, readers_list=readers_list)


@admindyapp.route('/submit_assigns', methods= ['GET', 'POST'])
def submit_assigns():

  credits_list = admindy_svc.credit_assigns()

  is_get = request.method == 'GET'

  assign_list = []

  for credit in credits_list:
    assign = (request.args.get( f'{credit.credit_id}_{credit.student_graduation_year}_{credit.reader_number}' ) if is_get else request.form.get( f'{credit.credit_id}_{credit.student_graduation_year}_{credit.reader_number}') )
    if assign != 'None':
      assign_list.append([credit.credit_id, credit.student_graduation_year, assign, credit.reader_number])

  admindy_svc.add_credit_assigns(assign_list)
  admindy_svc.add_reader_assigns()
  return redirect('/admindy/submissions')

@admindyapp.route('/override', methods= ['GET', 'POST'])
def confirm_assigns():

  is_get = request.method == 'GET'

  applications_list = admindy_svc.detailed_applications()

  assign_list_final = []

  for application in applications_list:
    assign_reader = ( request.args.get( f'{application.pkid}_reader' ) if is_get else request.form.get( f'{application.pkid}_reader') )
    assign_time = ( request.args.get( f'{application.pkid}_time' ) if is_get else request.form.get( f'{application.pkid}_time') )

    if assign_reader != '' and assign_time != '':
      assign_time_int = ''
      for char in assign_time:
        if char.isdigit():
          assign_time_int += char

      assign_time_int += '00'

      assign_list_final.append([application.pkid, assign_reader, assign_time_int])

  admindy_svc.add_final_assigns(assign_list_final)
  return redirect('/admindy/submissions')