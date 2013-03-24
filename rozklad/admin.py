from django.contrib import admin
from rozklad.models import Group, Teacher, Housing, AudienceType, Audience, SubjectsType, Subject, PairType, PairPeriod, Pair, Day, Schedule, TaskChair, Department

class GroupAdmin(admin.ModelAdmin):
	list_display = ('group_name', 'number_of_students')
	search_fields = ('group_name',)

class TeacherAdmin(admin.ModelAdmin):
	list_display = ('teacher_last_name', 'teacher_first_name', 'teacher_middle_name')
	search_fields = ('teacher_last_name',)

class HousingAdmin(admin.ModelAdmin):
	list_display = ('number_of_housing',)

class AudienceAdmin(admin.ModelAdmin):
	list_display = ('number_of_audience', 'audience_sets', 'housing', 'audience_type')
	search_fields = ('number_of_audience', 'audience_sets')
	list_filter = ('housing', 'audience_type')
	ordering = ('housing',)

class SubjectAdmin(admin.ModelAdmin):
	list_display = ('subject_name', 'subject_type')
	search_fields = ('subject_name',)
	list_filter = ('subject_type',)

class PairAdmin(admin.ModelAdmin):
	list_display = ('pair_number', 'pair_type', 'pair_period')
	list_filter = ('pair_type',)

class DayAdmin(admin.ModelAdmin):
	list_display = ('day',)

class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('group', 'day', 'pair', 'subject', 'audience', 'teacher')
	search_fields = ('group', 'sybject', 'audience')

class TaskChairAdmin(admin.ModelAdmin):
	list_display = ('group', 'teacher', 'subject', 'duration', 'audience')

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('department_name', 'department_full_name')

admin.site.register(Group, GroupAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Housing, HousingAdmin)
admin.site.register(AudienceType)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(SubjectsType)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(PairType)
admin.site.register(PairPeriod)
admin.site.register(Pair, PairAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TaskChair, TaskChairAdmin)
admin.site.register(Department, DepartmentAdmin)
