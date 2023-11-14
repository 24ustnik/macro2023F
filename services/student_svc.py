from . import db
from sqlalchemy import text
from flask import current_app, request

def submit_application( app_student_pkid=int, app_credit_id=int,
                                 app_rationale=text, app_app_cycle_title=text,
                                 app_app_cycle_date=int, app_date_submitted=int,
                                 app_status='Unreviewed', app_top_course=text ):
    sql_string = """
        INSERT INTO applications ( student_pkid, credit_id, rationale, app_cycle_title, app_cycle_date, date_submitted, status, top_course )
        VALUES( :student, :credit, :rationale_link, :cycle_title, :cycle_date, :date_submitted, :status, :top_course );
    
    """

    sql = db.text( sql_string )
    sql_with_parms = sql.bindparams(
        student=app_student_pkid,
        credit=app_credit_id,
        rationale_link=app_rationale,
        status=app_status,
        cycle_title=app_app_cycle_title,
        cycle_date=app_app_cycle_date,
        date_submitted=app_date_submitted,
        top_course=app_top_course
    )

    inserted_id = -1
    with db.engine.connect() as conn:
        rs = conn.execute( sql_with_parms )
        inserted_id = rs.lastrowid
        conn.commit()
    return inserted_id


def credits_status(student_pkid) -> list:
    select_statement = f"""
SELECT credit_name, app_cycle_title,
    is_earned, app_cycle_date, panel_time, latest.pkid as credit_id
    FROM (SELECT c.pkid, max(a.pkid) as max_pkid FROM credits as c
    LEFT OUTER JOIN applications as a ON c.pkid = a.credit_id
    AND student_pkid = :student_pkid
    GROUP BY c.pkid) as latest
LEFT JOIN applications as a ON latest.max_pkid = a.pkid
INNER JOIN credits as c ON latest.pkid = c.pkid;
    """

    sql = text(select_statement)

    results = [ ]
    #execute connection
    with db.engine.connect() as conn:
        params_dict = {'student_pkid':student_pkid}
        rs = conn.execute(sql, params_dict)
        for row in rs.mappings():
                results.append(row)
                print(row)
    return results


def credit_history(student_pkid=int, credit_id=int) -> list:
    select_statement = f"""
    SELECT app_cycle_title, fname, lname, credit_name, feedback FROM applications as a
        INNER JOIN faculty_members as f on a.faculty_id = f.pkid
        INNER JOIN credits as c on a.credit_id = c.pkid
        WHERE student_pkid = :student_pkid AND credit_id = :credit_id;
    """

    sql = text(select_statement)

    my_applications = [ ]
    #execute connection
    with db.engine.connect() as conn:
        params_dict = {'student_pkid':student_pkid,
                       'credit_id':credit_id}
        rs = conn.execute(sql, params_dict)
        for row in rs.mappings():
                my_applications.append(row)
                print(row)
    return my_applications


def courses() -> list:
    select_statement = f"""
    SELECT * FROM courses;
    """

    sql = text(select_statement)
    sql_with_parms = sql.bindparams()

    courses_list = []
    

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            courses_list.append(row)
    return courses_list