# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from diplom.views import rozklad_admin, predmet_autocomplite, teacher_autocomplite, audience_autocomplite, pair_add, about, main, rozklad, rozklad_content, group_subjs, getsubjsingle, getsubjsmodal, experimental, login_ajax, logout_ajax, forum

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'ac$', predmet_autocomplite), #обробка автозаповнення предмету
	(r'tch$', teacher_autocomplite), #обробка автозаповнення викладача
	(r'au$', audience_autocomplite), #обробка автозаповнення аудиторiї
	(r'sendsubj$', pair_add), #відправка запросу на додавання пари
	(r'getsubjs$', group_subjs), #повертає всі пари для групи
	(r'getsubjsingle$', getsubjsingle), #повертає предмети для певного дня і пари
	(r'getsubjsmodal$', getsubjsmodal), #повертає предмети пари і вводить їх в модальне вікно
	(r'login_ajax$', login_ajax),
	(r'logout_ajax$', logout_ajax),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^social/', include('social_auth.urls')),

	(r'^about/$', about),
	(r'^rozklad/$', rozklad),
	(r'^rozklad/(.+)/$', rozklad_content),
	(r'^forum/$', forum),
	(r'^experimental/$', experimental),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^rozklad_admin/$', rozklad_admin),
	('^$', main),
)
