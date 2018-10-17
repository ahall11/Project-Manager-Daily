import psycopg2
import psycopg2.extras
import json
import xml.etree.ElementTree as ET
import os


def get_credentials(filename):
    """
    Notes:  Reads server config file and converts xml to dictionary
    Args:   @filename: string path leading to server.config file
    Return: containing the keys 'address', 'username', 'password'(optional)
    """
    credentials = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        credentials[child.tag] = child.text
    return credentials


def connect(filename):
    """
    Notes:  Opens connection to database using credentials passed to function
            and creates a cursor object to be used to execute db operations
    Args:   @filename: string path leading to server.config file
    Return: cursor psycopg2 object (Used to perform database operations)
    """
    cwd = os.getcwd()
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    credentials = get_credentials(filename)
    try:
        conn = psycopg2.connect(dbname=credentials['dbname'],
                                user=credentials['username'],
                                password=credentials['password'],
                                host=credentials['host'])
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('Successfully connected to:', credentials['host'])
        os.chdir(cwd)
        return conn, cur
    except:
        print('Couldn\'t connect to server: ', credentials['host'])
        exit()


def disconnect(connection, cursor):
    """
    Notes:  Closes connection and cursor instances to db
    Args:   None
    Return: Boolean on whether or not both cursor and connection were
            successfully closed
    """
    success = True
    if connection:
        connection.close()
        print("Closing connection.")
    else:
        success = False
        print("[Warning] Could not close connection. No connection to db found.")
    if cursor:
        cursor.close()
        print("Closing cursor.")
    else:
        success = False
        print("[Warning] Could not close cursor. No cursor found.\n")
    return success


def list_tables(cursor):
    cursor.execute('SELECT * FROM pg_tables WHERE pg_tables.schemaname = \'public\';')
    res = cursor.fetchall()
    i = 1
    print('schemaname\ttablename\ttableowner\ttablespace\thasindexes\thasrules\thastriggers\trowsecurity')
    for table in res:
        print(i, '. ', end='')
        for attr in table:
            print(attr, end='\t')
        i += 1
        print('')


def get_report_info(cursor, report_number):
    report = {}
    query = 'SELECT P.number, P.name, R.id, R.date, R.weather, U.first_name, U.last_name FROM dailies_report R, dailies_project P, auth_user U WHERE R.id = ' + str(report_number) + ' AND R.project_id = P.id AND P.user_id = U.id'

    cursor.execute(query)
    result = cursor.fetchone()
    report.update({'project_number':result['number']})
    report.update({'project_name':result['name']})
    report.update({'report_id':result['id']})
    report.update({'date':str(result['date'])})
    report.update({'weather':result['weather']})
    report.update({'project_manager':result['first_name']+' '+result['last_name']})

    return report


def get_all_employee_info_for_report(cursor, report, report_number):
    employee_report = {}
    employee_report['e_report'] = {}
    query = 'SELECT ER.task_name, ER.task_details, ER.task_hours, E.first_name, E.last_name, E.labor_class, \
     E.ctr_code_id FROM dailies_employee_report ER, dailies_employee E WHERE ER.report_id = ' + str(report_number) + \
            ' AND ER.employee_id = E.id'

    cursor.execute(query)
    results = cursor.fetchall()
    i = 1
    for result in results:
        dictname = str(i)
        employee_report['e_report'][dictname] = {}
        employee_report['e_report'][dictname]['first_name'] = result['first_name']
        employee_report['e_report'][dictname]['last_name'] = result['last_name']
        employee_report['e_report'][dictname]['labor_class'] = result['labor_class']
        employee_report['e_report'][dictname]['contractor'] = result['ctr_code_id']
        employee_report['e_report'][dictname]['task_name'] = result['task_name']
        employee_report['e_report'][dictname]['task_details'] = result['task_details']
        employee_report['e_report'][dictname]['task_hours'] = float(result['task_hours'])
        i += 1
    report.update(employee_report)

    return report


def get_all_equipment_info_for_report(cursor, report, report_number):
    equipment_report = {}
    equipment_report['eq_report'] = {}
    query = 'SELECT  EQR.hours_used, EQ.name, EQ.ctr_code_id FROM dailies_equipment_report EQR, dailies_equipment EQ \
     WHERE EQR.report_id = ' + str(report_number) + ' AND EQR.equipment_id = EQ.id'

    cursor.execute(query)
    results = cursor.fetchall()
    i = 1
    for result in results:
        dictname = str(i)
        equipment_report['eq_report'][dictname] = {}
        equipment_report['eq_report'][dictname]['eq_name'] = result['name']
        equipment_report['eq_report'][dictname]['contractor'] = result['ctr_code_id']
        equipment_report['eq_report'][dictname]['hours_used'] = float(result['hours_used'])
        i += 1
    report.update(equipment_report)

    return report


def get_daily_report_info(cursor, report_number):
    """
    Notes:  Obtain info from database as a dictionary for the PDF report
    Args:   cursor (from Connection()), report_number (the id of the report you want)
    Return: report dictionary with all necessary info
    """
    report = get_report_info(cursor, report_number)
    report = get_all_employee_info_for_report(cursor, report, report_number)
    report = get_all_equipment_info_for_report(cursor, report, report_number)
    report = json.dumps(report) #This get it into JSON type
    return report


# Testings the variables
(con, cur) = connect('server.config')
print(get_daily_report_info(cur, 1))

disconnect(con, cur)
