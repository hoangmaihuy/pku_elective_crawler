import MySQLdb

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
ELECTIVE_DB = "elective_db"

def get_total_course(c):
    SQL = "SELECT COUNT(*) FROM course_tab;"
    try:
        c.execute(SQL)
        r = c.fetchone()
        return r[0]
    except Exception as e:
        print(e)
        return 0

def get_max_credit_course(c):
    SQL = "SELECT name, credit, school_name FROM course_tab ORDER BY credit DESC LIMIT 1;"
    try:
        c.execute(SQL)
        r = c.fetchone()
        return {
            "name": r[0],
            "credit": r[1],
            "school": r[2]
        }
    except Exception as e:
        print(e)
        return None

def get_courses_number_by_school(c):
    try:
        # Get number of courses openned by each school
        c.execute("SELECT school_name, COUNT(*) FROM course_tab GROUP BY school_name;")
        rs = c.fetchall()
        return [{"school": r[0], "course_count": r[1]} for r in rs]
    except Exception as e:
        print(e)
        return []

if __name__ == "__main__":
    db = MySQLdb.connect(host="127.0.0.1", port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=ELECTIVE_DB)
    c = db.cursor()
    print("Number of crawled courses:", get_total_course(c))
    print("Course having highest credit:", get_max_credit_course(c))
    print("Number of courses by school:")
    stats = get_courses_number_by_school(c)
    for s in stats:
        print("{school}  {count:<2}".format(school=s["school"], count=s["course_count"]))
