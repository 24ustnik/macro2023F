from . import db
from sqlalchemy import text
from flask import current_app

def update_credit_app( app_feedback:str, app_is_earned:int, app_pkid:int ):
    sql_string = """
        UPDATE applications SET feedback = :feedback, is_earned = :is_earned, status ='Reviewed'
        WHERE pkid = :pkid;
    """

    sql = db.text( sql_string )
    sql_with_parms = sql.bindparams(
        feedback=app_feedback,
        is_earned=app_is_earned,
        pkid=app_pkid,
    )

    inserted_id = -1
    with db.engine.connect() as conn:
        rs = conn.execute( sql_with_parms )
        inserted_id = rs.lastrowid
        conn.commit()
    return inserted_id

def retrieve_applications_reading(faculty_id_number: int) -> list:
    sql_string = """
    SELECT a.pkid, fname, lname, credit_name, rationale, status FROM applications as a
    INNER JOIN students as s ON a.student_pkid = s.pkid
    INNER JOIN credits as c ON a.credit_id = c.pkid
    WHERE (faculty_id = :id_number) AND app_cycle_title = 'fall2023';
"""
    sql = text(sql_string)
    sql_with_parms = sql.bindparams(id_number=faculty_id_number)
    my_results = []

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            my_results.append(row)
            print(row)
    return my_results

def stud_submission_and_result(credit_id_number: int) -> list:
    sql_string = """
    SELECT s.fname, s.lname, c.credit_name, c.pkid, a.date_submitted, a.feedback, f.email
FROM applications AS a
INNER JOIN students AS s ON a.student_pkid = s.pkid
INNER JOIN credits AS c ON a.credit_id = c.pkid
INNER JOIN faculty_members as f ON a.faculty_id = f.pkid
WHERE (credit_id = :id_number);
"""

    sql = text(sql_string)
    sql_with_parms = sql.bindparams(id_number=credit_id_number)
    my_results = []

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            my_results.append(row)
    return my_results


def previous_apps( credit_id:int, decision:int):
    
    if credit_id == None or decision == None:
    
        select_statement = f"""
        SELECT * FROM applications as a
        INNER JOIN credits as c on a.credit_id = c.pkid
        INNER JOIN students as s on a.student_pkid = s.pkid
        WHERE app_cycle_title != 'fall2023';
        """
    else:
        select_statement = f"""
        SELECT * FROM applications as a
        INNER JOIN credits as c on a.credit_id = c.pkid
        INNER JOIN students as s on a.student_pkid = s.pkid
        WHERE app_cycle_title != 'fall2023'
        AND credit_id = :credit_id
        AND is_earned = :decision;
        """

    sql = text(select_statement)
    sql_with_parms = sql.bindparams()

    previous_applications_list = []
    

    with db.engine.connect() as conn:
        params_dict = {'decision':decision,
                       'credit_id':credit_id}
        rs = conn.execute(sql, params_dict)
        for row in rs.mappings():
                previous_applications_list.append(row)
                print(row)
    return previous_applications_list


def credits_list() -> list:
    select_statement = f"""
    SELECT * FROM credits;
    """

    sql = text(select_statement)
    sql_with_parms = sql.bindparams()

    credits_list = []
    

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            credits_list.append(row)
    return credits_list