import requests
import time
import os
import random


course_types = ['speciality']

get_courses_url = 'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/getCurriculmByForm.do'
query_courses_url = 'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/queryCurriculum.jsp'
# Your cookie here
cookie = "" 


s = requests.Session()
s.headers.update({
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,zh-CN;q=0.7,zh;q=0.6',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'DNT': '1',
	'Referer': 'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/CourseQueryController.jpf',
	'Cookie': cookie,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
})

def get_courses(course_type, page_nums):
	form_data = {
		'wlw-radio_button_group_key:{actionForm.courseSettingType}': course_type,
		'{actionForm.courseID}': '',
		'{actionForm.courseName}': '',
		'wlw-select_key:{actionForm.deptID}OldValue': 'true',
		'wlw-select_key:{actionForm.deptID}': 'ALL',
		'wlw-select_key:{actionForm.courseDay}OldValue': 'true', 
		'wlw-select_key:{actionForm.courseDay}': '',
		'wlw-select_key:{actionForm.courseTime}OldValue': 'true',
		'wlw-select_key:{actionForm.courseTime}': '',
		'wlw-checkbox_key:{actionForm.queryDateFlag}OldValue': 'false',
		'deptIdHide': 'ALL',
		}

	for page_num in range(1, page_nums+1):
		if page_num == 1:
			r = s.post(get_courses_url, data=form_data)
		else:
			r = s.post(query_courses_url, data={
				'netui_row':'syllabusListGrid;{}'.format((page_num-1)*100),
			})
		if r.status_code != 200:
			print("get_courses_error|status_code={},course_type={},page={}".format(r.status_code, course_type, page_num))
			return
		dir_name = os.path.join('courses', course_type)
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		with open(os.path.join(dir_name, "{}.html".format(page_num)), "w", encoding="utf8") as f:
			f.write(r.text)
		print("get_courses_success|course_type={},page={}".format(course_type, page_num))
		time.sleep(5)

if __name__ == '__main__':
	get_courses('speciality', 20)
	get_courses('politics', 1)
	get_courses('english', 2)
	get_courses('gym', 2)
	get_courses('trans_choice', 2)
	get_courses('pub_choice', 2)
	get_courses('liberal_computer', 1)