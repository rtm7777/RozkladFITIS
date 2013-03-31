# -*- coding: utf-8 -*-

from django.db import models

class Group(models.Model):
	group_name			= models.CharField(max_length=30, verbose_name=u'назва групи')
	number_of_students	= models.IntegerField(verbose_name=u'кількість студентів')
	year				= models.IntegerField(verbose_name=u"курс")

	def __unicode__(self):
		return u'%s' % self.group_name

	class Meta:
		verbose_name		= u'Групу'
		verbose_name_plural = u'Групи'

class Teacher(models.Model):
	teacher_first_name  = models.CharField(max_length=15, verbose_name=u'імя викладача')
	teacher_last_name   = models.CharField(max_length=20, verbose_name=u'прізвище викладача')
	teacher_middle_name = models.CharField(max_length=20, verbose_name=u'по батькові')

	def __unicode__(self):
		return u'%s %s' % (self.teacher_last_name, self.teacher_first_name)

	class Meta:
		verbose_name		= u'Викладача'
		verbose_name_plural = u'Викладачі'

class Housing(models.Model):
	number_of_housing = models.IntegerField(verbose_name=u'номер корпусу')

	def __unicode__(self):
		return u'%s корпус' % self.number_of_housing

	class Meta:
		verbose_name		= u'Корпус'
		verbose_name_plural = u'Корпуси'

class AudienceType(models.Model):
	type_of_audience = models.CharField(max_length=30, verbose_name=u'тип аудиторії')

	def __unicode__(self):
		return self.type_of_audience

	class Meta:
		verbose_name		= u'Тип аудиторії'
		verbose_name_plural = u'Типи аудиторій'

class Audience(models.Model):
	number_of_audience = models.CharField(max_length=10, verbose_name=u'номер аудиторії')
	audience_sets      = models.IntegerField(verbose_name=u'кількість міст')
	housing            = models.ForeignKey(Housing, verbose_name=u'корпус')
	audience_type      = models.ForeignKey(AudienceType, verbose_name=u'тип аудиторії')

	def __unicode__(self):
		return u'%s' % self.number_of_audience

	class Meta:
		verbose_name		= u'Аудиторію'
		verbose_name_plural = u'Аудиторії'

class SubjectsType(models.Model):
	type_of_subject = models.CharField(max_length=25, verbose_name=u'вид заняття')

	def __unicode__(self):
		return self.type_of_subject

	class Meta:
		verbose_name		= u'Тип предмета'
		verbose_name_plural = u'Типи предметів'

class Subject(models.Model):
	subject_name = models.CharField(max_length=70, verbose_name=u'назва предмету')
	subject_type = models.ForeignKey(SubjectsType, verbose_name=u'вид заняття')

	def __unicode__(self):
		return self.subject_name

	class Meta:
		verbose_name		= u'Предмет'
		verbose_name_plural = u'Предмети'

class PairType(models.Model):
	type_of_pair = models.CharField(max_length=15, verbose_name=u'тип пари')

	def __unicode__(self):
		return u'%s' % self.type_of_pair

	class Meta:
		verbose_name		= u'Тип пари'
		verbose_name_plural = u'Типи пар'

class PairPeriod(models.Model):
	period = models.IntegerField()

	def __unicode__(self):
		return u'%s' % self.period

	class Meta:
		verbose_name		= u"Період"
		verbose_name_plural = u"Періоди"

class Pair(models.Model):
	pair_number = models.CharField(max_length=5, verbose_name=u'номер пари')
	pair_type   = models.ForeignKey(PairType, verbose_name=u'тип пари')
	pair_period = models.ForeignKey(PairPeriod, verbose_name=u"період")

	def __unicode__(self):
		return u'%s %s' % (self.pair_number, self.pair_type.type_of_pair)

	class Meta:
		verbose_name		= u'Пару'
		verbose_name_plural = u'Пари'

class Day(models.Model):
	day = models.CharField(max_length=10, verbose_name=u'день')

	def __unicode__(self):
		return self.day

	class Meta:
		verbose_name		= u'День'
		verbose_name_plural = u'Дні'

class Department(models.Model):
	department_name 	 = models.CharField(max_length=15, verbose_name=u"ім'я")
	department_full_name = models.CharField(max_length=40, verbose_name=u"повне ім'я")

	def __unicode__(self):
		return self.department_name

	class Meta:
		verbose_name		= u"кафедра"
		verbose_name_plural = u"кафедри"

class Schedule(models.Model):
	group    = models.ForeignKey(Group, verbose_name=u'група')
	teacher  = models.ForeignKey(Teacher, verbose_name=u'викладач')
	audience = models.ForeignKey(Audience, verbose_name=u'аудиторія')
	subject  = models.ForeignKey(Subject, verbose_name=u'предмет')
	day      = models.ForeignKey(Day, verbose_name=u'день')
	pair     = models.ForeignKey(Pair, verbose_name=u'пара')
	

class TaskChair(models.Model):
	department = models.ForeignKey(Department, verbose_name=u'кафедра')
	subject    = models.ForeignKey(Subject, verbose_name=u'предмет')
	group      = models.ForeignKey(Group, verbose_name=u'група')
	teacher    = models.ForeignKey(Teacher, verbose_name=u'викладач')
	audience   = models.ForeignKey(Audience, blank=True, null=True, verbose_name=u'аудиторія')
	duration   = models.DecimalField(max_digits=3, decimal_places=1, verbose_name=u'час')