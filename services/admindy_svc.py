from . import db
from sqlalchemy import text
from flask import current_app

def applications():
    sql_string = """
SELECT a.is_earned, c.shortname, c.credit_name, c.title, s.lname, s.fname, s.email, s.graduation_year FROM applications AS a
    INNER JOIN students AS s ON a.student_pkid = s.pkid
    INNER JOIN credits AS c ON a.credit_id = c.pkid
    WHERE a.app_cycle_title = 'fall2023'
    ORDER BY s.lname ASC;
    """
    sql = text(sql_string)
    sql_with_parms = sql.bindparams()
    my_results = []

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            my_results.append(row)
    return my_results


def readers():
    sql_string = """
    SELECT fname, lname, pkid FROM faculty_members;
    """
    sql = text(sql_string)
    sql_with_parms = sql.bindparams()
    readers_list = []

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            readers_list.append(row)
    return readers_list

def credit_assigns():
    sql_string = """
    SELECT * FROM credit_years as c
        INNER JOIN credits as e on c.credit_id = e.pkid
        LEFT OUTER JOIN faculty_members as f on c.faculty_id = f.pkid;
    """
    sql = text(sql_string)
    sql_with_parms = sql.bindparams()
    credits_list = []

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            credits_list.append(row)
    return credits_list

def add_credit_assigns( assigns_list ):


    for assign in assigns_list:
   
        sql_string = """
            UPDATE credit_years SET faculty_id = :faculty_id WHERE credit_id = :credit_id
            AND student_graduation_year = :student_graduation_year
            AND reader_number = :reader_number;
        """


        sql = db.text( sql_string )
        sql_with_parms = sql.bindparams(
            faculty_id=assign[2],
            credit_id=assign[0],
            student_graduation_year=assign[1],
            reader_number=assign[3]
    )
        inserted_id = -1
        with db.engine.connect() as conn:
            rs = conn.execute( sql_with_parms )
            inserted_id = rs.lastrowid
            conn.commit()

    return inserted_id


def add_reader_assigns():

    sql_string = """
        UPDATE applications INNER JOIN students ON applications.student_pkid = students.pkid
        SET applications.faculty_id=(SELECT credit_years.faculty_id FROM credit_years
        WHERE credit_years.student_graduation_year = students.graduation_year
        AND credit_years.credit_id = applications.credit_id AND credit_years.reader_number = 1)

        WHERE app_cycle_title = 'fall2023';
    """

    sql = text(sql_string)
    sql_with_parms = sql.bindparams()

    inserted_id = -1

    with db.engine.connect() as conn:
        rs = conn.execute( sql_with_parms )
        inserted_id = rs.lastrowid
        conn.commit()

    return inserted_id


def detailed_applications():

    sql_string = """
    SELECT s.fname as student_fname, s.lname as student_lname,
        credit_name, f.fname as reader_fname, f.lname as reader_lname,
        panel_time, a.pkid as pkid, faculty_id FROM applications as a
        LEFT JOIN students as s ON a.student_pkid = s.pkid
        lEFT JOIN faculty_members as f on a.faculty_id = f.pkid
        LEFT JOIN credits as c ON a.credit_id = c.pkid
        WHERE app_cycle_title = 'fall2023';
    """

    sql = text(sql_string)
    sql_with_parms = sql.bindparams()

    applications_list = []
    

    with db.engine.connect() as conn:
        rs = conn.execute(sql_with_parms)

        for row in rs.mappings():
            applications_list.append(row)
    return applications_list


def add_final_assigns( assigns_list ):


    for assign in assigns_list:
   
        sql_string = """
            UPDATE applications SET faculty_id = :faculty_id, panel_time = :panel_time WHERE pkid = :pkid;
        """

        sql = db.text( sql_string )
        sql_with_parms = sql.bindparams(
            pkid=assign[0],
            faculty_id=assign[1],
            panel_time=assign[2]
    )

        with db.engine.connect() as conn:
            rs = conn.execute( sql_with_parms )

            conn.commit()

    return


def previous_apps( credit_id:int, graduation_year:int):
    
    if credit_id == None or graduation_year == None:
    
        select_statement = f"""
        SELECT * FROM applications as a
        INNER JOIN credits as c on a.credit_id = c.pkid
        INNER JOIN students as s on a.student_pkid = s.pkid
        WHERE app_cycle_title = 'fall2023';
        """
    else:
        select_statement = f"""
        SELECT * FROM applications as a
        INNER JOIN credits as c on a.credit_id = c.pkid
        INNER JOIN students as s on a.student_pkid = s.pkid
        WHERE app_cycle_title = 'fall2023'
        AND credit_id = :credit_id
        AND graduation_year = :graduation_year;
        """

    sql = text(select_statement)
    sql_with_parms = sql.bindparams()

    previous_applications_list = []
    

    with db.engine.connect() as conn:
        params_dict = {'graduation_year':graduation_year,
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
