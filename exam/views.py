from typing import Counter
from django.shortcuts import render
from exam.models import *
import json
import base64
import datetime
import math
from pytz import timezone 
from itertools import groupby
from backend.constants_variables import statusCodes, statusMessages
from backend.constants_functions import  functions, requestMethod,Checks

# Create your views here.
def login(request):
	if(requestMethod.POST_REQUEST(request)):
		data = json.loads(request.body)
		user = data['user']
		print()
		passw = data['pass'].split(' ')[1].strip()
		passw=base64.b64decode(passw).decode('utf-8')
		print(passw)
		stu_id = list(StudentDetails.objects.filter(username=user,password=passw).values('id','name','email','date_of_birth','mobile','username','course'))
		print(len(stu_id),user,passw)
		if len(stu_id)==0:
			return functions.RESPONSE(statusMessages.MESSAGE_LOGIN_UNAUTHORIZED,statusCodes.STATUS_UNAUTHORIZED)
		else:
			stu_id = stu_id[0]
			obj = list(ExamSession.objects.filter(student_id=stu_id['id']).exclude(form_id__status='DELETE').values('form_id','form_id__course','form_id__subject','form_id__start_time','form_id__end_time','form_id__exam_title','form_id__date_of_exam','student_id','form_status'))
			data = {'data' : obj,'student': stu_id}
			return functions.RESPONSE(data,statusCodes.STATUS_SUCCESS)
	elif(requestMethod.GET_REQUEST(request)):
		form_id = request.GET['form_id']
		stu_id = request.GET['stu_id']
		obj = list(ExamSession.objects.filter(student_id = stu_id,form_id = form_id).values('id','form_status','form_id__date_of_exam','form_id__start_time','form_id__end_time','form_id__course','form_id__subject','form_id__exam_title'))
		if(obj[0]['form_status'] == 1):
			data = {'msg':'your response has already been submitted'}
			return functions.RESPONSE(data,statusCodes.STATUS_CONFLICT_WITH_MESSAGE)
		start_time = datetime.datetime.strptime(obj[0]['form_id__start_time'], '%Y-%m-%d %H:%M:%S')
		end_time = datetime.datetime.strptime(obj[0]['form_id__end_time'], '%Y-%m-%d %H:%M:%S')
		now_time1  = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
		now_time = datetime.datetime.strptime(now_time1, '%Y-%m-%d %H:%M:%S')
		if(start_time<=now_time and now_time <= end_time):
			data = get_form(form_id)
			data['start_time'] = start_time
			data['end_time'] = end_time
			data['form_id'] = form_id
			data['student_id'] = stu_id
			data['form_status'] = obj[0]['form_status']
			data['course'] = obj[0]['form_id__course']
			data['subject'] = obj[0]['form_id__subject']
			data['exam_title'] = obj[0]['form_id__exam_title']
			return functions.RESPONSE(data,statusCodes.STATUS_SUCCESS)
		else:
			data = {'msg':'the test is no longer available please contact to admin'}
			return functions.RESPONSE(data,statusCodes.STATUS_CONFLICT_WITH_MESSAGE)
	else:
		data = statusMessages.MESSAGE_METHOD_NOT_ALLOWED
		status =  statusCodes.STATUS_METHOD_NOT_ALLOWED
	return functions.RESPONSE(data,status)

def get_form(form_id):
	qr2 = list(ExamAttribute.objects.filter(form_id=form_id).values('element_id','attribute','max_marks','form_id').order_by('form_id','element_id'))
	att_list = []
	for i,j in groupby(qr2,key=lambda y:y['element_id']): 
		l=list(j)
		if len(l)>0:
			att_list.append(l[0]['attribute'])
	
	data={'elements': att_list}
	return data

def create_form(request):   
	data=""
	status = 402
	if(requestMethod.POST_REQUEST(request)):
		print('samyak')
		data = json.loads(request.body)
		if 'id' in data:
			qwert = ExamDetail.objects.filter(id=data['id']).update(status='DELETE')
			obj5 = data['elements']
			data['elements'] = {}
			data['elements']['form']=[]
			data['elements']['form']=obj5
			# print(data['elements'])
		data['course'] = data['course'].upper().strip()
		data['subject'] = data['subject'].upper().strip()
		data['exam_title'] = data['exam_title'].upper().strip()
		exam_id = ExamDetail.objects.create(course = data['course'],subject=data['subject'],exam_title=data['exam_title'],date_of_exam=data['date_of_exam'],start_time=data['start_time'],end_time=data['end_time'])
		qr_object = (ExamAttribute(form_id=ExamDetail.objects.get(id=exam_id.id),max_marks=att['max_marks'],element_id=att['element_id'],attribute=att)for k,v in data['elements'].items() for att in v)
		qr_create = ExamAttribute.objects.bulk_create(qr_object)
		stu_obj = list(StudentDetails.objects.all())
		student_obj = (ExamSession(form_id = ExamDetail.objects.get(id=exam_id.id),student_id=v) for v in stu_obj)
		stu_create = ExamSession.objects.bulk_create(student_obj)
		data = statusMessages.MESSAGE_INSERT
		status = statusCodes.STATUS_SUCCESS
	elif(requestMethod.GET_REQUEST(request)):
		if(requestMethod.custom_request_type(request.GET, 'get_form')):
			exam = list(ExamDetail.objects.filter(status='INSERT').values('id','subject','course','start_time','end_time','exam_title'))
			now_time1  = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
			now_time = datetime.datetime.strptime(now_time1, '%Y-%m-%d %H:%M:%S')
			data = []
			for x in exam:
				start_time = datetime.datetime.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S')
				if(start_time>now_time):
					data.append(x)
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET,'get_data')):
			exam = list(ExamDetail.objects.filter(id = request.GET['form_id']).values('id','subject','course','start_time','end_time','exam_title'))
			data = get_form(request.GET['form_id'])
			data1 = {**data,**exam[0]}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data1,status)
		elif(requestMethod.custom_request_type(request.GET,'get_delete')):
			exam = ExamDetail.objects.filter(id=request.GET['form_id']).update(status='DELETE')
			data={'msg':'form deleted successfully'}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
	else:
		data = statusMessages.MESSAGE_METHOD_NOT_ALLOWED
		status =  statusCodes.STATUS_METHOD_NOT_ALLOWED
	return functions.RESPONSE(data,status)
	
def submit_answer(request):
	print("samyak")
	if(requestMethod.POST_REQUEST(request)):
		print("in submit")
		data = json.loads(request.body)
		obj = list(ExamSession.objects.filter(student_id = data['student_id'],form_id = data['form_id']).values('id','form_status','form_id__date_of_exam','form_id__start_time','form_id__end_time','form_id__course','form_id__subject','form_id__exam_title'))
		start_time = datetime.datetime.strptime(obj[0]['form_id__start_time'], '%Y-%m-%d %H:%M:%S')
		end_time = datetime.datetime.strptime(obj[0]['form_id__end_time'], '%Y-%m-%d %H:%M:%S')
		now_time1  = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
		now_time = datetime.datetime.strptime(now_time1, '%Y-%m-%d %H:%M:%S')
		if(obj[0]['form_status'] == 1):
			data = {'msg':'your response has already been submitted'}
			return functions.RESPONSE(data,statusCodes.STATUS_CONFLICT_WITH_MESSAGE)
		elif(start_time<=now_time and now_time <= end_time):
			for z in data['elements']:
				if((z['answer']==None and z['answer'] == "") and z['mand']==True):
					data = {'msg':'Mandatory Answer Should not be Empty'}
					status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
					return functions.RESPONSE(data,status)
				if(z['answer']!=None and z['answer']!=""):					
					if(z['category']=='text' and (z['len_check']!=None and z['len_check']!="")):
						if(not(Checks.length_check(z['len_check'],len(z['answer'])))):
							data = {'msg':'Text filled length Should match to the length define'}
							status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
							return functions.RESPONSE(data,status)
					if(z['category']=='number'):
						# if(z['len_check']!=None and z['len_check']!=""):
						# 	if(not(Checks.length_check(z['len_check'],len(str(z['answer']))))):
						# 		data = {'msg':'length of the number filled must match with the length define'}
						# 		status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
						# 		return functions.RESPONSE(data,status)
						if(z['min']!=None or z['max']!=None):
							maxvalue = z['max'] 
							if(z['min']==None or z['min']==""):
								z['min']=0
							if(z['max']==None or z['max']==""):
								maxvalue= math.inf
							if(not(Checks.min_max_value_check(z['min'],maxvalue,z['answer']))):
								data = {'msg':'number filled must be in range of minimum and maximum define value'}
								status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
								return functions.RESPONSE(data,status)
					elif(z['category']=='slider'):
						# if(z['po_id']!=None):
						# 	if(len(z['po_id'])>0 and (z['max']==None or z['max']=="")):
						# 		data = {'msg':'slider value connected with po must have maximum value defined'}
						# 		status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
						# 		return functions.RESPONSE(data,status)
						if(z['min']!=None or z['max']!=None):
							maxvalue = z['max']
							if(z['min']==None or z['min']==""):
								z['min']=0
							elif(z['max']==None or z['max']==""):
								maxvalue=math.inf
							if(not(Checks.min_max_value_check(z['min'],maxvalue,z['answer']))):
								data = {'msg':'slider value filled must be in range of minimum and maximum value'}
								status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
								return functions.RESPONSE(data,status)
					elif(z['category']=='textarea' and z['max_words']!=None and z['max_words']!=""):
						if(not(Checks.min_words_in_paragraph(z['max_words'],z['answer']))):
							data = {'msg':'the no of words in paragraph Should match with the the length defined'}
							status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
							return functions.RESPONSE(data,status)
					elif(z['category']=='email'):
						if(not(Checks.email_check(z['answer']))):
							data = {'msg':'invalid email'}
							status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
							return functions.RESPONSE(data,status)
					elif(z['category']=='date' and z['start']!=None and z['end']!=None):
						if(not(Checks.min_max_date(z['start'],z['end'],z['answer']))):
							data = {'msg':'the date range mismatch with the start and end date defined'}
							status = statusCodes.STATUS_CONFLICT_WITH_MESSAGE
							return functions.RESPONSE(data,status)
				qry_id = ExamAttribute.objects.filter(form_id=data['form_id'],element_id = z['element_id']).exclude(form_id__status='DELETE').values_list('id',flat=True)
				z['ques_id'] = qry_id[0]
			qry_obj = (ExamAnswer(ans_id=ExamSession.objects.get(student_id=data['student_id'],form_id=data['form_id']),ans_attribute=z,ques_id=ExamAttribute.objects.get(id=z['ques_id']))for z in data['elements'])
			qr_create = ExamAnswer.objects.bulk_create(qry_obj)
			qry_hash = ExamSession.objects.filter(student_id=data['student_id'],form_id=data['form_id']).update(form_status=1)
			data = statusMessages.MESSAGE_FILLED
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)			
		else:
			data = {'msg':'the test is no longer available please contact to admin'}
			status=statusCodes.STATUS_CONFLICT_WITH_MESSAGE
			return functions.RESPONSE(data,status)
	elif(requestMethod.GET_REQUEST(request)):
		stu_id = request.GET['student_id']
		obj = list(ExamSession.objects.filter(student_id=stu_id).exclude(form_id__status='DELETE').values('form_id','form_id__course','form_id__subject','form_id__start_time','form_id__end_time','form_id__exam_title','form_id__date_of_exam','student_id','form_status'))
		now_time1  = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
		now_time = datetime.datetime.strptime(now_time1, '%Y-%m-%d %H:%M:%S')
		print(now_time)
		data={}
		data['live'] = []
		data['upcoming'] = []
		data['previous'] = []
		for x in obj:
			start_time = datetime.datetime.strptime(x['form_id__start_time'], '%Y-%m-%d %H:%M:%S')
			end_time = datetime.datetime.strptime(x['form_id__end_time'], '%Y-%m-%d %H:%M:%S')
			if(now_time>=start_time and now_time<=end_time):
				data['live'].append(x)
			elif(now_time>end_time):
				data['previous'].append(x)
			else:
				data['upcoming'].append(x)
		data = {'data' : data,'student': stu_id}
		return functions.RESPONSE(data,statusCodes.STATUS_SUCCESS)
	else:
		data = statusMessages.MESSAGE_FORBIDDEN
		status = statusCodes.STATUS_FORBIDDEN
	return functions.RESPONSE(data,status)

def check_status(request):
	if(requestMethod.POST_REQUEST(request)):
		data = {'msg':'ok'}
		status = statusCodes.STATUS_SUCCESS
		return functions.RESPONSE(data,status) 
	elif(requestMethod.GET_REQUEST(request)):
		if(requestMethod.custom_request_type(request.GET, 'get_drop')):
			qry = list(ExamDetail.objects.filter(status = 'INSERT').values('id','course','subject','exam_title','start_time','end_time'))
			data = []
			for x in qry:
				start_time = datetime.datetime.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S')
				end_time = datetime.datetime.strptime(x['end_time'], '%Y-%m-%d %H:%M:%S')
				now_time1  = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
				now_time = datetime.datetime.strptime(now_time1, '%Y-%m-%d %H:%M:%S')
				if(end_time<now_time):
					data.append(x)
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'get_form_data')):
			form_id = request.GET['form_id']
			qry = list(ExamSession.objects.filter(form_id = form_id).values('form_id','student_id','student_id__name','student_id__username','student_id__mobile','form_status','student_id__date_of_birth'))
			status = statusCodes.STATUS_SUCCESS
			data = {'data':qry}
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'get_student')):
			form_id = request.GET['form_id']
			student_id = request.GET['student_id']
			data = form_answer(form_id,student_id)
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		else:
			data = statusMessages.MESSAGE_FORBIDDEN
			status = statusCodes.STATUS_FORBIDDEN
			return functions.RESPONSE(data,status)
	else:
		data = statusMessages.MESSAGE_FORBIDDEN
		status = statusCodes.STATUS_FORBIDDEN
	return functions.RESPONSE(data,status)

def form_answer(get_id,student_id):
	qr2 = list(ExamAnswer.objects.filter(ans_id__form_id=get_id,ans_id__student_id=student_id).values('ques_id__element_id','ans_attribute','ques_id__max_marks','ques_id__form_id').order_by('ques_id__form_id','ques_id__element_id'))
	att_list = []
	if len(qr2)>0:
		for i,j in groupby(qr2,key=lambda y:y['ques_id__element_id']): 
			l=list(j)
			if len(l)>0:
				att_list.append(l[0]['ans_attribute'])
	data={'elements': att_list}
	return data


def test(request):
	if(requestMethod.GET_REQUEST(request)):
		if(requestMethod.custom_request_type(request.GET, 'insert_student')):
			name = request.GET['name']
			course = request.GET['course']
			date_of_birth = request.GET['date']
			email = request.GET['email']
			mobile = request.GET['mobile']
			username = request.GET['username']
			password = request.GET['password']
			qry = StudentDetails.objects.create(name= name,course=course,date_of_birth = date_of_birth,email=email,mobile=mobile,username=username,password=password)
			data = {'msge':'student inserted'}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'update')):
			# qry = StudentDetails.objects.filter(id=1).update(id=1001)
			# qry = StudentDetails.objects.filter(id=2).update(id=1002)
			qry = StudentDetails.objects.filter(id=3).update(id=1003)
			data = {'data':'qry'}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'get_student')):
			qry = list(StudentDetails.objects.filter().values('id','course','username','name','password'))
			data = {'data':qry}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'clear_all_data')):
			qry = ExamAnswer.objects.all().delete()
			qry2 = ExamSession.objects.all().delete()
			qry3 = ExamAttribute.objects.all().delete()
			qry4 = ExamDetail.objects.all().delete()
			data = {'data':'success cleared all data'}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		elif(requestMethod.custom_request_type(request.GET, 'get_all_form')):
			qry = list(ExamDetail.objects.filter().values('id','course','subject','status','start_time','end_time','exam_title'))
			data = {'data':qry}
			status = statusCodes.STATUS_SUCCESS
			return functions.RESPONSE(data,status)
		else:
			data = statusMessages.MESSAGE_FORBIDDEN
			status = statusCodes.STATUS_FORBIDDEN
			return functions.RESPONSE(data,status)
	else:
		data = statusMessages.MESSAGE_FORBIDDEN
		status = statusCodes.STATUS_FORBIDDEN
		return functions.RESPONSE(data,status)








