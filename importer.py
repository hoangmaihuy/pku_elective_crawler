import os
from MySQLdb import _mysql
import simplejson as json

COURSE_DATA_DIR = "./courses_data"

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
ELECTIVE_DB = "elective_db"

COURSE_TYPE_MAP = {
    "english": "英语课",
    "gym": "体育课",
    "liberal_computer": "计算机基础课",
    "politics": "政治课",
    "pub_choice": "公选课",
    "speciality": "专业课",
    "trans_choice": "通选课",
}

CREATE_COURSE_TABLE_SQL = \
"CREATE TABLE course_tab ( \
    id INT NOT NULL AUTO_INCREMENT, \
    course_no VARCHAR(20) NOT NULL, \
    name VARCHAR(100) NOT NULL, \
    credit INT NOT NULL, \
    type VARCHAR(10) NOT NULL, \
    school_name VARCHAR(20) NOT NULL, \
    PRIMARY KEY (id) \
);"

INSERT_COURSE_SQL = \
"INSERT INTO course_tab (course_no, name, credit, type, school_name) \
    VALUES ('{course_no}', '{name}', {credit}, '{type}','{school_name}');"

def import_courses(course_type):
    # Read course data from json file
    with open(os.path.join(COURSE_DATA_DIR, course_type+".json"), "r", encoding="utf8") as f:
        courses = json.load(f)
    # Insert course into table
    chinese_course_type = COURSE_TYPE_MAP[course_type]
    for course in courses:
        try:
            db.query(INSERT_COURSE_SQL.format(
                course_no=course["id"],
                name=course["name"],
                credit=course["credit"],
                type=chinese_course_type,
                school_name=course["school"]
            ))
            print("Insert {} successfully!".format(course["name"]))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    # Connect to MySQL
    db = _mysql.connect(host="127.0.0.1", port=3306, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=ELECTIVE_DB)
    # Create course_tab table
    try:
        db.query(CREATE_COURSE_TABLE_SQL)
    except Exception as e:
        print(e)

    for course_type in COURSE_TYPE_MAP.keys():
        import_courses(course_type)