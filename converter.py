import os
from bs4 import BeautifulSoup
import simplejson as json

courses_dir = 'courses'

def parse_course(course_type, cols):
    course = {}
    if course_type in ['speciality', 'gym', 'liberal_computer', 'politics', 'pub_choice']:
        course = {
            'id':  cols[0].span.text,
            'name': cols[1].span.text,
            'credit' : int(float(cols[3].span.text)),
            'teachers': cols[4].span.text.split(','),
            'school': cols[6].span.text,
            'profession': cols[7].span.text,
        }
    elif course_type == 'english':
        course = {
            'id':  cols[0].span.text,
            'name': cols[1].span.text,
            'level': cols[2].span.text,
            'credits' : int(float(cols[4].span.text)),
            'teachers': cols[5].span.text.split(','),
            'school': cols[7].span.text,
            'profession': cols[8].span.text,
        }
    elif course_type == 'trans_choice':
        course = {
            'id':  cols[0].span.text,
            'name': cols[1].span.text,
            'type': cols[2].span.text,
            'credits' : int(float(cols[4].span.text)),
            'teachers': cols[5].span.text.split(','),
            'school': cols[7].span.text,
            'profession': cols[8].span.text,
        }

    return course

def convert_courses(course_type):
    course_data = dict()
    dir_name = os.path.join(courses_dir, course_type)
    if not os.path.exists(dir_name):
        return
    for page in os.listdir(dir_name):
        with open(os.path.join(dir_name, page), "r", encoding='utf8') as f:
            text = f.read()
        soup = BeautifulSoup(text, 'lxml')
        rows = soup.find_all('tr', ['datagrid-odd', 'datagrid-even'])
        for row in rows:
            cols = row.find_all('td')
            course = parse_course(course_type, cols)
            course_id = course['id']
            school = course['school']
            _course = course_data.get((course_id, school))
            if _course is None:
                course_data[(course_id, school)] = course
            else:
                _course['teachers'] += course['teachers']
                _course['teachers'] = list(set(_course['teachers']))

    course_file = os.path.join('courses_data', course_type+'.json')
    with open(course_file, "w+", encoding='utf-8') as f:
        json.dump(list(course_data.values()), f, encoding='utf-8', ensure_ascii=False)

if __name__ == '__main__':
    convert_courses('speciality')
    convert_courses('english')
    convert_courses('gym')
    convert_courses('liberal_computer')
    convert_courses('politics')
    convert_courses('pub_choice')
    convert_courses('trans_choice')