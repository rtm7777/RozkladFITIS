# -*- coding: utf-8 -*-

from chromelogger import chromelogger as console

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from rozklad.models import Group, Teacher, Housing, AudienceType, Audience, SubjectsType, Subject, PairType, Pair, Day, Schedule, Department, TaskChair
from django.utils import simplejson
from django.contrib import auth
from django.db.models import Q

days_in_week = [u'1Понеділок', u'2Вівторок', u'3Середа', u'4Четвер', u"5П'ятниця"]
pair_in_day = ['I', 'II', 'III', 'IV', 'V', 'VI']

def group_subjs(request):
	group     = request.GET.get("group")
	jquery    = request.GET.get("callback")
	schedules = Schedule.objects.filter(group__group_name = group)
	result    = {}
	res       = []
	period    = ""
	for schedule in schedules:
		if schedule.pair.pair_period.period   == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period == 4:
			period = "4,8,12,16"
		elif schedule.pair.pair_period.period == 5:
			period = "5,9,13,17"
		subject = schedule.subject.subject_name + ' - ' + schedule.subject.subject_type.type_of_subject
		audience = ' a.' + schedule.audience.number_of_audience + '-' + str(schedule.audience.housing.number_of_housing)
		teacher = ' ' + schedule.teacher.teacher_last_name + ' ' + schedule.teacher.teacher_first_name[0] + '.' + schedule.teacher.teacher_middle_name[0] + '.' + " " + period
		sub = {}
		sub["daypair"] = schedule.day.day[0] + '_' + schedule.pair.pair_number
		sub["subject"] =  subject + audience + teacher
		sub["tupe"] = schedule.pair.pair_type.type_of_pair
		res.append(sub)
	result['sources'] = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def rozklad_admin(request):
	days 		= days_in_week
	pairs 		= pair_in_day
	groups 		= Group.objects.order_by("group_name")
	houses 		= Housing.objects.all()
	departments = Department.objects.all()
	groups_list = []
	houses_list = []
	dep_list 	= []
	for g in groups:
		groups_list.append(g.group_name)
	for h in houses:
		houses_list.append(str(h.number_of_housing))
	for d in departments:
		dep_list.append(d.department_name)
	return render_to_response('rozklad_admin.html', {'days': days, 'pairs': pairs, 'groups': groups_list, 'houses': houses_list, 'departments': dep_list})

def predmet_autocomplite(request):
	subjects = Subject.objects.all()
	query    = request.GET.get("str")
	jquery   = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result 	= {}
		res 	= []
		for subject in subjects:
			subj 		 = {}
			subj['name'] = subject.subject_name
			subj['type'] = subject.subject_type.type_of_subject
			res.append(subj)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	else:
		result = {}
		res = []
		for subject in subjects:
			if subject.subject_name.lower().find(query.lower()) != -1:
				subj 		 = {}
				subj['name'] = subject.subject_name
				subj['type'] = subject.subject_type.type_of_subject
				res.append(subj)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def teacher_autocomplite(request):
	teachers = Teacher.objects.all()
	query    = request.GET.get("str")
	jquery   = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res    = []
		for teacher in teachers:
			teach = {}
			teach['firstname']  = teacher.teacher_first_name
			teach['lastname']   = teacher.teacher_last_name
			teach['middlename'] = teacher.teacher_middle_name
			res.append(teach)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	else:
		result = {}
		res    = []
		for teacher in teachers:
			if teacher.teacher_last_name.lower().find(query.lower()) != -1:
				teach = {}
				teach['firstname']  = teacher.teacher_first_name
				teach['lastname']   = teacher.teacher_last_name
				teach['middlename'] = teacher.teacher_middle_name
				res.append(teach)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def audience_autocomplite(request):
	audiences = Audience.objects.all()
	query     = request.GET.get("str")
	jquery    = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res    = []
		for audience in audiences:
			aud 		  = {}
			aud['number'] = audience.number_of_audience + " - " + str(audience.housing.number_of_housing)
			res.append(aud)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	else:
		result = {}
		res = []
		for audience in audiences:
			if str(audience.number_of_audience).lower().find(query.lower()) != -1:
				aud = {}
				aud['number'] = audience.number_of_audience + " - " + str(audience.housing.number_of_housing)
				res.append(aud)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def group_autocomplite(request):
	groups = Group.objects.all()
	
	query = request.GET.get("str")

	jquery = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res    = []
		for group in groups:
			gr = {}
			gr['name'] = group.group_name
			res.append(gr)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	else:
		result = {}
		res = []
		for group in groups:
			if group.group_name.lower().find(query.lower()) != -1:
				gr = {}
				gr['name'] = group.group_name
				res.append(gr)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def pair_add(request):
	group_val 	 = request.GET.get("group")
	day_pair 	 = request.GET.get("para").split(" ")
	jquery 		 = request.GET.get("callback")
	day 		 = day_pair[0]
	pair 		 = day_pair[1]
	evenodd      = request.GET.get("evenodd")
	lining_check = request.GET.get("lining")

	schedules 	  = Schedule.objects.all()
	pairs_objects = Pair.objects.filter(pair_number = pair)

	pair_add.errors 		= ""
	pair_add.error_inputs   = []
	pair_add.lining 		= ""
	pair_add.lin_count_t 	= 0
	pair_add.lin_count_a 	= 0

	def delete_objects(objects):
		for schedule in schedules:
			for p in objects:
				if schedule.day == s_day and schedule.pair == p and schedule.group == s_group:
					p1 = schedule
					p1.delete()

	def save_schedule(day, group, teacher, audience, subject, pair):
		p1 = Schedule(day    = day,
					group    = group,
					teacher  = teacher,
					audience = audience,
					subject  = subject,
					pair     = pair)
		p1.save()

	def full_save_schedule():
		delete_objects(pairs_objects)
		if evenodd == "true":
			if subject1:
				s_pair = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "кожен", pair_period__period=period1)
				save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair)

		elif evenodd == "false":
			if subject1 and subject2:
				s_pair1 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "непарна", pair_period__period= period1)				
				s_pair2 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "парна", pair_period__period =  period2)
				save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair1)
				save_schedule(s_day, s_group, pair_add.s_teacher2, pair_add.s_audience2, pair_add.s_subject2, s_pair2)

			elif not subject2 and subject1:
				s_pair1 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "непарна", pair_period__period = period1)
				save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair1)

			elif not subject1 and subject2:
				s_pair2 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "парна", pair_period__period =  period2)
				save_schedule(s_day, s_group, pair_add.s_teacher2, pair_add.s_audience2, pair_add.s_subject2, s_pair2)

	def error_check1():
		try:
			pair_add.s_subject = Subject.objects.get(subject_name = subject1_split[0], subject_type__type_of_subject = subject1_split[1])
		except:
			pair_add.error_inputs.append("msub1")
			pair_add.errors = "true"
		try:
			pair_add.s_teacher = Teacher.objects.get(teacher_last_name = teacher1[0], teacher_first_name = teacher1[1], teacher_middle_name = teacher1[2])
		except:
			pair_add.error_inputs.append("mteach1")
			pair_add.errors = "true"
		try:
			pair_add.s_audience = Audience.objects.get(number_of_audience = audience1_split[0], housing__number_of_housing = audience1_split[1])
		except:
			pair_add.error_inputs.append("maud1")
			pair_add.errors = "true"

	def error_check2():
		try:
			pair_add.s_subject2 = Subject.objects.get(subject_name = subject2_split[0], subject_type__type_of_subject = subject2_split[1])
		except:
			pair_add.error_inputs.append("msub2")
			pair_add.errors = "true"
		try:
			pair_add.s_teacher2 = Teacher.objects.get(teacher_last_name = teacher2[0], teacher_first_name = teacher2[1], teacher_middle_name = teacher2[2])
		except:
			pair_add.error_inputs.append("mteach2")
			pair_add.errors = "true"
		try:
			pair_add.s_audience2 = Audience.objects.get(number_of_audience = audience2_split[0], housing__number_of_housing = audience2_split[1])
		except:
			pair_add.error_inputs.append("maud2")
			pair_add.errors = "true"

	def check_lining_teacher(teacher, period, eo="кожен"):
		lessons = Schedule.objects.filter(day__day = day, pair__pair_number = pair, teacher__teacher_last_name =  teacher[0], teacher__teacher_first_name = teacher[1], teacher__teacher_middle_name = teacher[2]).exclude(day__day = day, pair__pair_number = pair, group__group_name = group_val)
		pair_add.lin_count_t = lessons.count()

		if pair_add.lin_count_t != 0:
			for lesson in lessons:
				if lesson.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
					if lesson.pair.pair_period.period == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
					elif int(period) == lesson.pair.pair_period.period or int(period) == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
				elif eo == lesson.pair.pair_type.type_of_pair.encode("utf-8") or eo == "кожен":
					if lesson.pair.pair_period.period == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
					elif int(period) == lesson.pair.pair_period.period or int(period) == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"


	def check_lining_audience(audience, period, eo="кожен"):
		lessons = Schedule.objects.filter(day__day = day, pair__pair_number = pair, audience__number_of_audience = audience[0], audience__housing__number_of_housing = audience[1]).exclude(day__day = day, pair__pair_number = pair, group__group_name = group_val)
		pair_add.lin_count_a = lessons.count()

		if pair_add.lin_count_a != 0:
			for lesson in lessons:
				if lesson.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
					if lesson.pair.pair_period.period == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
					elif int(period) == lesson.pair.pair_period.period or int(period) == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
				elif eo == lesson.pair.pair_type.type_of_pair.encode("utf-8") or eo == "кожен":
					if lesson.pair.pair_period.period == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"
					elif int(period) == lesson.pair.pair_period.period or int(period) == 1:
						pair_add.errors = "true"
						pair_add.lining = "true"


	subject1 			= request.GET.get("subject1")
	if subject1:
		subject1_split  = subject1.split(" - ")
	teacher1			= request.GET.get("teacher1").split(" ")
	audience1 			= request.GET.get("audience1")
	audience1_split 	= audience1.split(" - ")
	period1 			= request.GET.get("period1")

	subject2 			= request.GET.get("subject2")
	if subject2:
		subject2_split  = subject2.split(" - ")
	teacher2 			= request.GET.get("teacher2").split(" ")
	audience2 			= request.GET.get("audience2")
	audience2_split 	= audience2.split(" - ")
	period2 			= request.GET.get("period2")

	s_day = Day.objects.get(day=day)
	s_group = Group.objects.get(group_name=group_val)

	if evenodd == "true":
		if subject1 == "":
			full_save_schedule()
		else:
			error_check1()
			if pair_add.errors != "true":
				if lining_check == "true":
					check_lining_teacher(teacher1, period1)
					check_lining_audience(audience1_split, period1)
					if pair_add.lining != "true":
						full_save_schedule()
				else:
					full_save_schedule()

	elif evenodd == "false":
		if subject1 == "" and subject2 =="":
			full_save_schedule()
		elif subject2 == "":
			error_check1()
			if pair_add.errors != "true":
				if lining_check == "true":
					check_lining_teacher(teacher1, period1, "непарна")
					check_lining_audience(audience1_split, period1, "непарна")
					if pair_add.lining != "true":
						full_save_schedule()
				else:
					full_save_schedule()
		elif subject1 == "":
			error_check2()
			if pair_add.errors != "true":
				if lining_check == "true":
					check_lining_teacher(teacher2, period2, "парна")
					check_lining_audience(audience2_split, period2, "парна")
					if pair_add.lining != "true":
						full_save_schedule()
				else:
					full_save_schedule()
		else:
			error_check1()
			error_check2()
			if pair_add.errors != "true":
				if lining_check == "true":
					check_lining_teacher(teacher1, period1, "непарна")
					check_lining_audience(audience1_split, period1, "непарна")
					check_lining_teacher(teacher2, period2, "парна")
					check_lining_audience(audience2_split, period2, "парна")
					if pair_add.lining != "true":
						full_save_schedule()
				else:
					full_save_schedule()
		

	result 					 = {}
	result['errors'] 		 = pair_add.errors
	result['error_inputs']   = pair_add.error_inputs
	result['lining'] 		 = pair_add.lining
	result['count'] 		 = str(pair_add.lin_count_t) + " __ " + str(pair_add.lin_count_a)
	json 					 = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def pair_stream_add(request):
	groups = request.GET.get("groups")[:-1].split(",")
	day = request.GET.get("day")
	pair = request.GET.get("pair")
	jquery = request.GET.get("callback")
	evenodd = request.GET.get("evenodd")

	schedules = Schedule.objects.all()

	pair_add.errors = ""
	pair_add.errors_message = "Некорректно введено:"

	def save_schedule(day, group, teacher, audience, subject, pair):
		p1 = Schedule(day    = day,
					group    = group,
					teacher  = teacher,
					audience = audience,
					subject  = subject,
					pair     = pair)
		p1.save()

	def full_save_schedule():
		pair_count = 0
		for g in groups:
			pair_count += Schedule.objects.filter(group__group_name = g, day__day = day, pair__pair_number = pair).count()
		if not pair_count:
			for g in groups:
				s_group = Group.objects.get(group_name=g)
				if evenodd == "true":
					s_pair = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "кожен", pair_period__period=period1)
					save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair)
				elif evenodd == "false":
					if subject1 and subject2:
						s_pair1 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "непарна", pair_period__period= period1)
						s_pair2 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "парна", pair_period__period =  period2)
						save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair1)
						save_schedule(s_day, s_group, pair_add.s_teacher2, pair_add.s_audience2, pair_add.s_subject2, s_pair2)
					elif not subject2 and subject1:
						s_pair1 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "непарна", pair_period__period = period1)
						save_schedule(s_day, s_group, pair_add.s_teacher, pair_add.s_audience, pair_add.s_subject, s_pair1)
					elif not subject1 and subject2:
						s_pair2 = Pair.objects.get(pair_number = pair, pair_type__type_of_pair = "парна", pair_period__period =  period2)
						save_schedule(s_day, s_group, pair_add.s_teacher2, pair_add.s_audience2, pair_add.s_subject2, s_pair2)
		else:
			pair_add.errors = "true"
			pair_add.errors_message = "Заняття уже є у групах:"
			busy_groups_set = set()
			busy_groups = Schedule.objects.filter(day__day = day, pair__pair_number = pair)
			for g in busy_groups:
				if g.group.group_name in groups:
					busy_groups_set.add(g.group.group_name)
			for g in busy_groups_set:
				pair_add.errors_message += " " + g.encode("utf-8") + ","

	def error_check1():
		try:
			pair_add.s_subject = Subject.objects.get(subject_name = subject1_split[0], subject_type__type_of_subject = subject1_split[1])
		except:
			pair_add.errors_message += " предмет1,"
			pair_add.errors = "true"
		try:
			pair_add.s_teacher = Teacher.objects.get(teacher_last_name = teacher1[0], teacher_first_name = teacher1[1], teacher_middle_name = teacher1[2])
		except:
			pair_add.errors_message += " викладач1,"
			pair_add.errors = "true"
		try:
			pair_add.s_audience = Audience.objects.get(number_of_audience = audience1_split[0], housing__number_of_housing = audience1_split[1])
		except:
			pair_add.errors_message += " аудиторія1,"
			pair_add.errors = "true"

	def error_check2():
		try:
			pair_add.s_subject2 = Subject.objects.get(subject_name = subject2_split[0], subject_type__type_of_subject = subject2_split[1])
		except:
			pair_add.errors_message += " предмет2,"
			pair_add.errors = "true"
		try:
			pair_add.s_teacher2 = Teacher.objects.get(teacher_last_name = teacher2[0], teacher_first_name = teacher2[1], teacher_middle_name = teacher2[2])
		except:
			pair_add.errors_message += " викладач2,"
			pair_add.errors = "true"
		try:
			pair_add.s_audience2 = Audience.objects.get(number_of_audience = audience2_split[0], housing__number_of_housing = audience2_split[1])
		except:
			pair_add.errors_message += " аудиторія2,"
			pair_add.errors = "true"

	subject1 = request.GET.get("subject1")
	if subject1:
		subject1_split = subject1.split(" - ")
	teacher1 = request.GET.get("teacher1").split(" ")
	audience1 = request.GET.get("audience1")
	audience1_split = audience1.split(" - ")
	period1 = request.GET.get("period1")

	subject2 = request.GET.get("subject2")
	if subject2:
		subject2_split = subject2.split(" - ")
	teacher2 = request.GET.get("teacher2").split(" ")
	audience2 = request.GET.get("audience2")
	audience2_split = audience2.split(" - ")
	period2 = request.GET.get("period2")

	s_day = Day.objects.get(day=day)

	if evenodd == "true":
		if subject1 != "":
			error_check1()
			if pair_add.errors != "true":
				full_save_schedule()

	elif evenodd == "false":
		if subject1 != "" and subject2 != "":
			error_check1()
			error_check2()
			if pair_add.errors != "true":
				full_save_schedule()
		elif subject2 == "":
			error_check1()
			if pair_add.errors != "true":
				full_save_schedule()
		elif subject1 == "":
			error_check2()
			if pair_add.errors != "true":
				full_save_schedule()
	
	result = {}
	result['errors'] = pair_add.errors
	result['errors_message'] = pair_add.errors_message[:-1]
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getsubjsingle(request):
	group_val = request.GET.get("group")
	day_pair = request.GET.get("para").split(" ")
	jquery = request.GET.get("callback")
	day = day_pair[0]
	pair = day_pair[1]
	schedules = Schedule.objects.filter(group__group_name = group_val, day__day = day, pair__pair_number = pair)
	result = {}
	res = []
	period = ""
	for schedule in schedules:
		if schedule.pair.pair_period.period   == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period == 4:
			period = "4,8,12,16"
		elif schedule.pair.pair_period.period == 5:
			period = "5,9,13,17"
		subject = schedule.subject.subject_name + ' - ' + schedule.subject.subject_type.type_of_subject
		audience = ' a.' + schedule.audience.number_of_audience + '-' + str(schedule.audience.housing.number_of_housing)
		teacher = ' ' + schedule.teacher.teacher_last_name + ' ' + schedule.teacher.teacher_first_name[0] + '.' + schedule.teacher.teacher_middle_name[0] + '.' + ' ' + period
		sub = {}
		sub["daypair"] = schedule.day.day[0] + '_' + schedule.pair.pair_number
		sub["subject"] =  subject + audience + teacher
		sub["tupe"] = schedule.pair.pair_type.type_of_pair
		res.append(sub)
	result['sources'] = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getsubjsmodal(request):
	group_val = request.GET.get("group")
	day_pair  = request.GET.get("para").split(" ")
	jquery    = request.GET.get("callback")
	day       = day_pair[0]
	pair      = day_pair[1]
	result    = {}
	res       = []
	
	schedules = Schedule.objects.filter(group__group_name = group_val, day__day = day, pair__pair_number = pair)
	for schedule in schedules:
		sub = {}
		sub["subject"]   = schedule.subject.subject_name + " - " + schedule.subject.subject_type.type_of_subject
		sub["teacher"]   = schedule.teacher.teacher_last_name + " " + schedule.teacher.teacher_first_name + " " + schedule.teacher.teacher_middle_name
		sub["audience"]  = str(schedule.audience.number_of_audience) + " - " + str(schedule.audience.housing.number_of_housing)
		sub["period"]    = schedule.pair.pair_period.period
		sub["pair_type"] = schedule.pair.pair_type.type_of_pair
		sub["amount"]    = "false"
		res.append(sub)
	result['sources']    = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def dnd(request):
	group     = request.GET.get("group")
	start_les = request.GET.get("from").split("_")
	end_les   = request.GET.get("to").split("_")
	action    = request.GET.get("action")
	jquery    = request.GET.get("callback")

	les_start = Schedule.objects.filter(group__group_name = group, day__day__contains = start_les[0], pair__pair_number = start_les[1])
	les_end = Schedule.objects.filter(group__group_name = group, day__day__contains = end_les[0], pair__pair_number = end_les[1])


	linings_start = False
	linings_end   = False

	def lin_check(lessons, les):
		lining = False
		for lesson in lessons:
			if lesson.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
				if lesson.pair.pair_period.period == 1:
					lining = True
				elif int(les.pair.pair_period.period) == lesson.pair.pair_period.period or int(les.pair.pair_period.period) == 1:
					lining = True
			elif les.pair.pair_type.type_of_pair.encode("utf-8") == lesson.pair.pair_type.type_of_pair.encode("utf-8") or les.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
				if lesson.pair.pair_period.period == 1:
					lining = True
				elif int(les.pair.pair_period.period) == lesson.pair.pair_period.period or int(les.pair.pair_period.period) == 1:
					lining = True
		return lining

	def get_lining_count(les, se_les, exclude_les):
		lining = False
		lessons_t = Schedule.objects.filter(day__day__contains=se_les[0], pair__pair_number = se_les[1], teacher__teacher_last_name = les.teacher.teacher_last_name, teacher__teacher_first_name = les.teacher.teacher_first_name, teacher__teacher_middle_name = les.teacher.teacher_middle_name)
		for l in exclude_les:
			lessons_t = lessons_t.exclude(group__group_name = group)
		lin_count_t = lessons_t.count()

		if lin_count_t != 0:
			lining = lin_check(lessons_t, les)

		lessons_a = Schedule.objects.filter(day__day__contains=se_les[0], pair__pair_number = se_les[1], audience__number_of_audience = les.audience.number_of_audience, audience__housing__number_of_housing = les.audience.housing.number_of_housing)
		for l in exclude_les:
			lessons_a = lessons_a.exclude(group__group_name = group)
		lin_count_a = lessons_a.count()

		if lin_count_a != 0:
			if not lining:
				lining = lin_check(lessons_a, les)

		return lining


	for les in les_start:
		if not linings_start:
			linings_start = get_lining_count(les, end_les, les_end)
		
	for les in les_end:
		if not linings_end:
			linings_end   = get_lining_count(les, start_les, les_start)

	if action == "swap":
		if not linings_start and not linings_end:
			for les in les_start:
				les.delete()
				les = Schedule(day = Day.objects.get(day__contains=end_les[0]),
					pair     = Pair.objects.get(pair_number = end_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
					group    = les.group,
					teacher  = les.teacher,
					audience = les.audience, 
					subject  = les.subject)
				les.save()
			for les in les_end:
				les.delete()
				les = Schedule(day = Day.objects.get(day__contains=start_les[0]),
					pair     = Pair.objects.get(pair_number = start_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
					group    = les.group,
					teacher  = les.teacher,
					audience = les.audience, 
					subject  = les.subject)
				les.save()
	elif action == "replace":
		if not linings_start:
			for les in les_end:
				les.delete()
			for les in les_start:
				les.delete()
				les = Schedule(day = Day.objects.get(day__contains=end_les[0]),
					pair     = Pair.objects.get(pair_number = end_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
					group    = les.group,
					teacher  = les.teacher,
					audience = les.audience, 
					subject  = les.subject)
				les.save()
	elif action == "copy":
		if not linings_start:
			for les in les_end:
				les.delete()
			for les in les_start:
				les = Schedule(day = Day.objects.get(day__contains=end_les[0]),
					pair     = Pair.objects.get(pair_number = end_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
					group    = les.group,
					teacher  = les.teacher,
					audience = les.audience, 
					subject  = les.subject)
				les.save()
	result = {}
	result['status'] = str(linings_start) + str(linings_end)
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getaudemp(request):
	house = request.GET.get("house")
	day = request.GET.get("day")
	jquery = request.GET.get("callback")

	audiences = Audience.objects.filter(housing__number_of_housing = house)
	schedules = Schedule.objects.filter(day__day = day, audience__housing__number_of_housing = house)

	result = {}
	res = []

	for audience in audiences:
		aud = {}
		pairs = []
		aud['number'] = audience.number_of_audience
		for schedule in schedules:
			if audience == schedule.audience:
				items           = {}
				items["num"]    = schedule.pair.pair_number
				items["type"]   = schedule.pair.pair_type.type_of_pair
				items["period"] = str(schedule.pair.pair_period.period)
				pairs.append(items)
		aud["pairs"] = pairs
		res.append(aud)
	result['audiences'] = res

	result['status'] = "ok"
	json = jquery+'('+simplejson.dumps(result)+')'
	console.log('Hello console!')
	return HttpResponse(json, mimetype = 'application/json')

def getteachemp(request):
	house = request.GET.get("house")
	day = request.GET.get("day")
	jquery = request.GET.get("callback")

	teachers = Teacher.objects.all()
	schedules = Schedule.objects.filter(day__day = day)

	result = {}
	res = []

	for teacher in teachers:
		teach = {}
		pairs = []
		teach['name'] = teacher.teacher_last_name + "_" + teacher.teacher_first_name + "_" + teacher.teacher_middle_name
		for schedule in schedules:
			if teacher == schedule.teacher:
				items = {}
				items["num"]    = schedule.pair.pair_number
				items["type"]   = schedule.pair.pair_type.type_of_pair
				items["period"] = str(schedule.pair.pair_period.period)
				pairs.append(items)
		teach["pairs"] = pairs
		res.append(teach)
	result['teachers'] = res

	result['status'] = "ok"
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getdeptasks(request):
	dep = request.GET.get("dep")
	jquery = request.GET.get("callback")

	tasks = TaskChair.objects.filter(department__department_name=dep)

	result = {}
	res = []

	for task in tasks:
		items ={}
		items["subject"] = task.subject.subject_name + " - " + task.subject.subject_type.type_of_subject
		items["group"]   = task.group.group_name
		items["time"]    = str(task.duration)
		items["teacher"] = task.teacher.teacher_last_name + " " + task.teacher.teacher_first_name + " " + task.teacher.teacher_middle_name
		items["id"]      = task.id
		try:
			items["audience"] = task.audience.number_of_audience
		except:
			items["audience"] = "-"
		res.append(items)
	result["tasks"] = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def adddeptask(request):
	department = request.GET.get("department")
	subject    = request.GET.get("subject")
	if subject:
		subject_split = subject.split(" - ")
	group      = request.GET.get("group")
	teacher    = request.GET.get("teacher").split(" ")
	audience   = request.GET.get("audience")
	audience_split = audience.split(" - ")
	duration   = request.GET.get("duration")
	jquery     = request.GET.get("callback")

	result = {}
	e = False

	def check_errors():
		e = False
		items = {}
		try:
			items["subject"] = Subject.objects.get(subject_name = subject_split[0], subject_type__type_of_subject = subject_split[1])
		except:
			e = True
		try:
			items["teacher"] = Teacher.objects.get(teacher_last_name = teacher[0], teacher_first_name = teacher[1], teacher_middle_name = teacher[2])
		except:
			e = True
		if audience != "":
			try:
				items["audience"] = Audience.objects.get(number_of_audience = audience_split[0], housing__number_of_housing = audience_split[1])	
			except:
				e = True
		else:
			items["audience"] = None
		try:
			items["department"] = Department.objects.get(department_name = department)
		except:
			e = True
		try:
			items["group"] = Group.objects.get(group_name = group)
		except:
			e = True

		return e, items

	def save_task(dep, sub, gr, teach, aud, dur):
		t = TaskChair(department = dep,
					subject      = sub,
					group        = gr,
					teacher      = teach,
					audience     = aud,
					duration     = dur)
		t.save()
	if department != "":
		e, items = check_errors()
		if not e:
			save_task(items['department'], items['subject'], items['group'], items['teacher'], items['audience'], duration)

	result['errors'] = e
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getconformity(request):
	group = request.GET.get("group")
	jquery = request.GET.get("callback")

	result = {}
	res = []

	tasks = TaskChair.objects.filter(group__group_name = group)


	def getvalue(sub_name, sub_type, duration):
		time = 0.0
		lessons = Schedule.objects.filter(group__group_name = group, subject__subject_name = sub_name, subject__subject_type__type_of_subject = sub_type)
		for lesson in lessons:
			if lesson.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
				if lesson.pair.pair_period.period == 1:
					time += 2
				else:
					time += 0.5
			else:
				if lesson.pair.pair_period.period == 1:
					time += 1
				else:
					time += 0.5
		value = (100.0*time)/float(duration)

		return value, time

	for task in tasks:
		items = {}
		value, time = getvalue(task.subject.subject_name, task.subject.subject_type.type_of_subject, task.duration)
		items["subject"] = task.subject.subject_name + " - " + task.subject.subject_type.type_of_subject + ": [" + str(time) + "/" + str(task.duration) + "]"
		items["value"] = value
		if value < 100:
			items["type"] = ""
		elif value == 100:
			items["type"] = "progress-success"
		elif value > 100:
			items["type"] = "progress-danger"
		res.append(items)
	result['sources'] = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def delsub(request):
	jquery 		 = request.GET.get("callback")
	del_type     = request.GET.get("type")
	group_val 	 = request.GET.get("group")
	del_id	 = request.GET.get("id")

	if del_type == "1":
		day_pair = del_id.split("_")
		subjects 	 = Schedule.objects.filter(group__group_name = group_val, day__day__contains = day_pair[0], pair__pair_number = day_pair[1])
		for s in subjects:
			s.delete()
	elif del_type == "2":
		task = TaskChair.objects.get(id = del_id)
		task.delete()
	result = {}
	result['status'] = "ok"
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def simulate(request):
	jquery 		 = request.GET.get("callback")
	
	groups 		 = Group.objects.order_by("group_name")
	groups_list  = {}
	for g in groups:
		groups_list[g.group_name] = False

	weeks = 1  #кількість тижнів

	log   = ""

	period  = 1
	period2 = [2, 6, 10, 14]
	period3 = [3, 7, 11, 15]
	period4 = [4, 8, 12, 16]
	period5 = [5, 9, 13, 17]

	simulate_result = {}
	simulate_result_log = ""

	for w in range(1, weeks+1):
		simulate_result[w] = {}
		for d in days_in_week:
			simulate_result[w][d] = {}
			for p in pair_in_day:
				simulate_result[w][d][p] = {'success': [], 'unsuccess': []}
				

	def gen(week, period, wType, result):
		log = ""
		for d in days_in_week:
			for p in pair_in_day:
				for g in groups:
					groups_list[g.group_name] = False
				Schedules = Schedule.objects.filter(day__day = d, pair__pair_number = p).filter(Q(pair__pair_period__period = period) | Q(pair__pair_period__period = 1)).exclude(pair__pair_type__type_of_pair = wType)
				for s in Schedules:
					if not groups_list[s.group.group_name]:
						result[week][d][s.pair.pair_number]['success'].append(s.group.group_name)
						groups_list[s.group.group_name] = True
					else:
						result[week][d][s.pair.pair_number]['unsuccess'].append(s.group.group_name)
		return log

	for w in range(1, weeks+1):
		if w in period2: 
			period = 2
		elif w in period3:
			period = 3
		elif w in period4:
			period = 4
		elif w in period5:
			period = 5

		if w%2 != 0:
			log += gen(w, period, "парна", simulate_result)
		else:
			log += gen(w, period, "непарна", simulate_result)

	for key in sorted(simulate_result):
		for key2 in sorted(simulate_result[key]):
			for key3 in sorted(simulate_result[key][key2]):
				simulate_result_log += str(key).encode("utf-8") + " тиждень " + key2.encode("utf-8")[1:] + " " + key3.encode("utf-8") + " пара: успішно - "
				for i in simulate_result[key][key2][key3]['success']:
					simulate_result_log += i.encode("utf-8") + ", "
				simulate_result_log += " невдало -"
				for i in simulate_result[key][key2][key3]['unsuccess']:
					simulate_result_log += i.encode("utf-8") + ", "
				simulate_result_log += "\n"


	result = {}
	result['status'] = log
	result['dat'] = simulate_result_log
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getgroups(request):
	jquery 		 = request.GET.get("callback")
	
	year	 	 = request.GET.get("year")
	groups 		 = Group.objects.filter(year = year).order_by("group_name")
	groups_list  = []
	for g in groups:
		groups_list.append(g.group_name)

	result = {}
	result['data'] = groups_list
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def getgrouploading(request):
	jquery 	= request.GET.get("callback")
	group	= request.GET.get("group")
	data 	= [0, 0, 0, 0, 0]
	i = 0
	for d in days_in_week:
		schedules = Schedule.objects.filter(group__group_name = group, day__day = d)
		for s in schedules:
			if s.pair.pair_type.type_of_pair.encode("utf-8") == "кожен":
				data[i] += 2
			else:
				if s.pair.pair_period.period == 1:
					data[i] +=1
				else:
					data[i] += 0.5
		i += 1
	result = {}
	result['data'] = data
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')