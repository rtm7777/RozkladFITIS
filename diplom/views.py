# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from rozklad.models import Group, Teacher, Housing, AudienceType, Audience, SubjectsType, Subject, PairType, Pair, Day, Schedule, PairPeriod
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
	groups 		= Group.objects.order_by("group_name")
	groups_list = []
	for g in groups:
		groups_list.append(g.group_name)
	return render_to_response('rozklad_group.html', {'groups': groups_list})

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
			result[d][p]['1'] = ""
			result[d][p]['2'] = ""
			result[d][p]['3'] = ""

	period = ""

	schedules = Schedule.objects.filter(teacher__teacher_last_name = tlfm[0], teacher__teacher_first_name = tlfm[1], teacher__teacher_middle_name = tlfm[2])
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
		group = ' ' + schedule.group.group_name + ' ' + period

		if schedule.pair.pair_type.type_of_pair == u'кожен':
			result[schedule.day.day][schedule.pair.pair_number]['1'] = subject + audience + group + '<br>'
			result[schedule.day.day][schedule.pair.pair_number]['type'] = 1
		elif schedule.pair.pair_type.type_of_pair == u'непарна':
			
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0 or result[schedule.day.day][schedule.pair.pair_number]['type'] == 2:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 2
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4
			result[schedule.day.day][schedule.pair.pair_number]['2'] += subject + audience + group + '<br>'
		elif schedule.pair.pair_type.type_of_pair == u'парна':
			
			if result[schedule.day.day][schedule.pair.pair_number]['type'] == 0 or result[schedule.day.day][schedule.pair.pair_number]['type'] == 3:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 3
			else:
				result[schedule.day.day][schedule.pair.pair_number]['type'] = 4
			result[schedule.day.day][schedule.pair.pair_number]['3'] += subject + audience + group + '<br>'

	return render_to_response('rt_content.html', {'days': days, 'pairs': pairs, 'teachers': teachers_list, 'active_teacher': teacher, 'result': result, 'myurl': request.build_absolute_uri()})

def about(request):
	return render_to_response('about.html')

def gmaps(request):
	return render_to_response('gmaps.html')

@ensure_csrf_cookie
@csrf_protect
def experimental(request):
	if not request.user.is_authenticated():
		return render_to_response('login.html')
	else:
		return render_to_response('experimental.html')

def forum(request):
	return render_to_response('forum.html')


def initializebase(request):
	pair_types = ["непарна", "парна", "кожен"]

	for pty in pair_types:
		p1 = PairType(type_of_pair = pty)
		p1.save()

	pair_periods = [1, 2, 3, 4, 5]

	for pper in pair_periods:
		p1 = PairPeriod(period = pper)
		p1.save()

	pair_type = PairType.objects.all()
	pair_period = PairPeriod.objects.all()

	pair_numbers = ["I", "II", "III", "IV", "V", "VI"]

	for pt in pair_type:
		for pn in pair_numbers:
			for pp in pair_period:
				p1 = Pair(pair_type = pt,
					pair_number = pn,
					pair_period = pp)
				p1.save()

	subjectstypes = ["Практика", "Лабораторна", "Лекція", "Загальна"]

	for st in subjectstypes:
		p1 = SubjectsType(type_of_subject = st)
		p1.save()

	houses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	for h in houses:
		p1 = Housing(number_of_housing = h)
		p1.save()

	audiencestypes = ["Лабораторна", "Лекційна", "Загальна"]

	for at in audiencestypes:
		p1 = AudienceType(type_of_audience = at)
		p1.save()

	days = [u'1Понеділок', u'2Вівторок', u'3Середа', u'4Четвер', u"5П'ятниця"]

	for d in days:
		p1 = Day(day = d)
		p1.save()

	teachers = [u'Данилюк Андрій Андрійович', u'Сєркова Любов Едуардівна', u'Триус Юрій Васильович', u"Стеценко Інна В'ячеславівна", u'Саух Валерій Михайлович', u'Тимченко Анатолій Анастасійович']

	for t in teachers:
		t_s = t.split(" ")
		p1 = Teacher(teacher_last_name = t_s[0], teacher_first_name = t_s[1], teacher_middle_name = t_s[2])
		p1.save()