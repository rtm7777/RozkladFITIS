# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from rozklad.models import Group, Teacher, Housing, AudienceType, Audience, SubjectsType, Subject, PairType, Pair, Day, Schedule
from django.utils import simplejson
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie


days_in_week = [u'1Понеділок', u'2Вівторок', u'3Середа', u'4Четвер', u"5П'ятниця"]
pair_in_day = ['I', 'II', 'III', 'IV', 'V', 'VI']

def main(request):
	return render_to_response('main.html')

@csrf_protect
def ajax_login(request):
	result = {}
	if request.method == 'POST':
		username = request.POST.get('login')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			result['sources'] = "1"
			json = simplejson.dumps(result)
			return HttpResponse(json, mimetype = 'application/json')
		else:
			result['sources'] = username
			json = simplejson.dumps(result)
			return HttpResponse(json, mimetype = 'application/json')

def rozklad(request):
	groups = Group.objects.order_by("group_name")
	groups_list = []
	for g in groups:
		groups_list.append(g.group_name)
	return render_to_response('rozklad_group.html', {'groups': groups_list})

def group_subjs(request):
	group = request.GET.get("group")
	jquery = request.GET.get("callback")
	schedules = Schedule.objects.filter(group__group_name = group)
	result = {}
	res = []
	period = ""
	for schedule in schedules:
		if schedule.pair.pair_period.period == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period ==4:
			period = "4,8,12,16"
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

def rozklad_content(request, group):
	groups = Group.objects.order_by("group_name")
	groups_list = []
	for g in groups:
		groups_list.append(g.group_name)
	days = days_in_week
	pairs = pair_in_day

	result = {}
	for d in days:
		result[d] = {}
		for p in pairs:
			result[d][p]={}
			result[d][p]['type'] = 0

	period = ""

	schedules = Schedule.objects.filter(group__group_name = group)
	for schedule in schedules:
		if schedule.pair.pair_period.period == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period ==4:
			period = "4,8,12,16"
		subject = schedule.subject.subject_name + ' - ' + schedule.subject.subject_type.type_of_subject
		audience = ' a.' + schedule.audience.number_of_audience + '-' + str(schedule.audience.housing.number_of_housing) + ' ' + period
		teacher = ' ' + schedule.teacher.teacher_last_name + ' ' + schedule.teacher.teacher_first_name[0] + '.' + schedule.teacher.teacher_middle_name[0] + '.'

		if schedule.pair.pair_type.type_of_pair == u'кожен':
			result[schedule.day.day][schedule.pair.pair_number]['1'] = subject + audience + teacher
			result[schedule.day.day][schedule.pair.pair_number]['type'] = 1
		elif schedule.pair.pair_type.type_of_pair == u'непарна':
			result[schedule.day.day][schedule.pair.pair_number]['2'] = subject + audience + teacher
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 2
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4
		elif schedule.pair.pair_type.type_of_pair == u'парна':
			result[schedule.day.day][schedule.pair.pair_number]['3'] = subject + audience + teacher
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 3
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4

	return render_to_response('rozklad_content.html', {'days': days, 'pairs': pairs, 'groups': groups_list, 'active_group': group, 'result': result, 'myurl': request.build_absolute_uri()})

def rozklad_teacher(request):
	teachers = Teacher.objects.order_by("teacher_last_name")
	teachers_list = {}
	for t in teachers:
		teachers_list[t.teacher_last_name + "_" + t.teacher_first_name + "_" + t.teacher_middle_name] = t.teacher_last_name + " " + t.teacher_first_name[0] + ". " + t.teacher_middle_name[0] + "."
	return render_to_response('rozklad_teacher.html', {'teachers': teachers_list})

def rt_content(request, teacher):
	tlfm = teacher.split("_")

	teachers = Teacher.objects.order_by("teacher_last_name")
	teachers_list = {}
	for t in teachers:
		teachers_list[t.teacher_last_name + "_" + t.teacher_first_name + "_" + t.teacher_middle_name] = t.teacher_last_name + " " + t.teacher_first_name[0] + ". " + t.teacher_middle_name[0] + "."
	days = days_in_week
	pairs = pair_in_day

	result = {}
	for d in days:
		result[d] = {}
		for p in pairs:
			result[d][p]={}
			result[d][p]['type'] = 0

	period = ""

	schedules = Schedule.objects.filter(teacher__teacher_last_name = tlfm[0], teacher__teacher_first_name = tlfm[1], teacher__teacher_middle_name = tlfm[2])
	for schedule in schedules:
		if schedule.pair.pair_period.period == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period ==4:
			period = "4,8,12,16"
		subject = schedule.subject.subject_name + ' - ' + schedule.subject.subject_type.type_of_subject
		audience = ' a.' + schedule.audience.number_of_audience + '-' + str(schedule.audience.housing.number_of_housing)
		group = ' ' + schedule.group.group_name + ' ' + period

		if schedule.pair.pair_type.type_of_pair == u'кожен':
			result[schedule.day.day][schedule.pair.pair_number]['1'] = subject + audience + group
			result[schedule.day.day][schedule.pair.pair_number]['type'] = 1
		elif schedule.pair.pair_type.type_of_pair == u'непарна':
			result[schedule.day.day][schedule.pair.pair_number]['2'] = subject + audience + group
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 2
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4
		elif schedule.pair.pair_type.type_of_pair == u'парна':
			result[schedule.day.day][schedule.pair.pair_number]['3'] = subject + audience + group
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 3
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4

	return render_to_response('rt_content.html', {'days': days, 'pairs': pairs, 'teachers': teachers_list, 'active_teacher': teacher, 'result': result, 'myurl': request.build_absolute_uri()})


def rozklad_admin(request):
	days = days_in_week
	pairs = pair_in_day
	groups = Group.objects.order_by("group_name")
	groups_list = []
	for g in groups:
		groups_list.append(g.group_name)
	return render_to_response('rozklad_admin.html', {'days': days, 'pairs': pairs, 'groups': groups_list})

def about(request):
	return render_to_response('about.html')

def predmet_autocomplite(request):
	subjects = Subject.objects.all()
	
	query = request.GET.get("predmet", "")
	jquery = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res = []
		for subject in subjects:
			subj = {}
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
				subj = {}
				subj['name'] = subject.subject_name
				subj['type'] = subject.subject_type.type_of_subject
				res.append(subj)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def teacher_autocomplite(request):
	teachers = Teacher.objects.all()
	
	query = request.GET.get("teacher", "")
	jquery = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res = []
		for teacher in teachers:
			teach = {}
			teach['firstname'] = teacher.teacher_first_name
			teach['lastname'] = teacher.teacher_last_name
			teach['middlename'] = teacher.teacher_middle_name
			res.append(teach)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	else:
		result = {}
		res = []
		for teacher in teachers:
			if teacher.teacher_last_name.lower().find(query.lower()) != -1:
				teach = {}
				teach['firstname'] = teacher.teacher_first_name
				teach['lastname'] = teacher.teacher_last_name
				teach['middlename'] = teacher.teacher_middle_name
				res.append(teach)
		result['sources'] = res
		json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

def audience_autocomplite(request):
	audiences = Audience.objects.all()
	
	query = request.GET.get("auditory", "")

	jquery = request.GET.get("callback")
	if len(query) == 0 or query[0] == " ":
		result = {}
		res = []
		for audience in audiences:
			aud = {}
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

def pair_add(request):
	group_val = request.GET.get("group")
	day_pair = request.GET.get("para").split(" ")
	jquery = request.GET.get("callback")
	day = day_pair[0]
	pair = day_pair[1]
	evenodd = request.GET.get("evenodd")

	schedules = Schedule.objects.all()
	pairs_objects = Pair.objects.filter(pair_number = pair)

	pair_add.errors = ""
	pair_add.errors_message = "Некорректно введено:"

	def delete_objects(objects):
		for schedule in schedules:
			for p in objects:
				if schedule.day == s_day and schedule.pair == p and schedule.group == s_group:
					p1 = schedule
					p1.delete()

	def save_schedule(day, group, teacher, audience, subject, pair):
		p1 = Schedule(day = day,
					group = group,
					teacher = teacher,
					audience = audience,
					subject = subject,
					pair = pair)
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
	s_group = Group.objects.get(group_name=group_val)

	if evenodd == "true":
		if subject1 == "":
			full_save_schedule()
		else:
			error_check1()
			if pair_add.errors != "true":
				full_save_schedule()

	elif evenodd == "false":
		if subject1 == "" and subject2 =="":
			full_save_schedule()
		elif subject2 == "":
			error_check1()
			if pair_add.errors != "true":
				full_save_schedule()
		elif subject1 == "":
			error_check2()
			if pair_add.errors != "true":
				full_save_schedule()
		else:
			error_check1()
			error_check2()
			if pair_add.errors != "true":
				full_save_schedule()
		
		

	result = {}
	result['errors'] = pair_add.errors
	result['errors_message'] = pair_add.errors_message[:-1]
	json = jquery+'('+simplejson.dumps(result)+')'
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
		p1 = Schedule(day = day,
					group = group,
					teacher = teacher,
					audience = audience,
					subject = subject,
					pair = pair)
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
		if schedule.pair.pair_period.period == 1:
			period = ""
		elif schedule.pair.pair_period.period == 2:
			period = "2,6,10,14"
		elif schedule.pair.pair_period.period == 3:
			period = "3,7,11,15"
		elif schedule.pair.pair_period.period == 4:
			period = "4,8,12,16"
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
	day_pair = request.GET.get("para").split(" ")
	jquery = request.GET.get("callback")
	day = day_pair[0]
	pair = day_pair[1]
	result = {}
	res = []
	
	schedules = Schedule.objects.filter(group__group_name = group_val, day__day = day, pair__pair_number = pair)
	for schedule in schedules:
		sub = {}
		sub["subject"] = schedule.subject.subject_name + " - " + schedule.subject.subject_type.type_of_subject
		sub["teacher"] = schedule.teacher.teacher_last_name + " " + schedule.teacher.teacher_first_name + " " + schedule.teacher.teacher_middle_name
		sub["audience"] = str(schedule.audience.number_of_audience) + " - " + str(schedule.audience.housing.number_of_housing)
		sub["period"] = schedule.pair.pair_period.period
		sub["pair_type"] = schedule.pair.pair_type.type_of_pair
		sub["amount"] = "false"
		res.append(sub)
	result['sources'] = res
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')

@ensure_csrf_cookie
@csrf_protect
def experimental(request):
	if not request.user.is_authenticated():
		return render_to_response('login.html')
	else:
		return render_to_response('experimental.html')

def forum(request):
	return render_to_response('forum.html')

def dnd(request):
	group = request.GET.get("group")
	start_les = request.GET.get("from").split("_")
	end_les = request.GET.get("to").split("_")
	action = request.GET.get("action")
	jquery = request.GET.get("callback")

	les_start = Schedule.objects.filter(group__group_name = group, day__day__contains = start_les[0], pair__pair_number = start_les[1])
	les_end = Schedule.objects.filter(group__group_name = group, day__day__contains = end_les[0], pair__pair_number = end_les[1])

	for les in les_start:
		les.delete()

	for les in les_end:
		les.delete()

	if action == "swap":
		for les in les_start:
			les = Schedule(day = Day.objects.get(day__contains=end_les[0]),
				pair = Pair.objects.get(pair_number = end_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
				group = les.group,
				teacher = les.teacher,
				audience = les.audience, 
				subject = les.subject)
			les.save()
		for les in les_end:
			les = Schedule(day = Day.objects.get(day__contains=start_les[0]),
				pair = Pair.objects.get(pair_number = start_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
				group = les.group,
				teacher = les.teacher,
				audience = les.audience, 
				subject = les.subject)
			les.save()
	elif action == "replace":
		for les in les_start:
			les = Schedule(day = Day.objects.get(day__contains=end_les[0]),
				pair = Pair.objects.get(pair_number = end_les[1], pair_type__type_of_pair = les.pair.pair_type.type_of_pair, pair_period__period = les.pair.pair_period.period ),
				group = les.group,
				teacher = les.teacher,
				audience = les.audience, 
				subject = les.subject)
			les.save()

	result = {}
	result['status'] = "ok"
	json = jquery+'('+simplejson.dumps(result)+')'
	return HttpResponse(json, mimetype = 'application/json')