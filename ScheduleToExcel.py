#!/usr/bin/python
# -*- coding: utf-8 -*-

from xlwt import Workbook,easyxf

start_pos = 9   # НЕ ставити менше 3! Установка початкової комірки

day_style = easyxf(
	'font: bold on;'
	'align: vertical center, horizontal center, rotation 90;'
	'borders: left 2, right 2, top 2, bottom 2;'
	)

pair_style = easyxf(
	'font: bold on;'
	'align: vertical center, horizontal center;'
	'borders: left 2, right 2, top 2, bottom 2;'
	)

sybject_style1 = easyxf(
	'font: height 220;'
	'align: horizontal center;'
	'borders: left 1, right 1, top 1;'
	)

sybject_style2 = easyxf(
	'font: height 220;'
	'align: vertical top, horizontal center;'
	'borders: left 1, right 1, bottom 1;'
	)

groups_style = easyxf(
	'font: bold on;'
	'align: vertical center, horizontal center;'
	'borders: left 2, right 2, top 2, bottom 2;'	
	)

group_pair_style = easyxf(
	'font: height 160;'
	'borders: left 1, right 1, top 1, bottom 1;'
	)

def SetDays():					#Фунція установки розмітки днів і пар
	st_pos_days = start_pos
	st_pos_pairs = start_pos
	days = [u'Понеділок', u'Вівторок', u'Середа', u'Четвер', u'Пятниця']
	pairs = [u'I', u'II', u'III', u'IV', u'V', u'VI']
	ws.col(0).width = 0x470
	ws.col(1).width = 0x470
	for day in range(5):
		ws.write_merge(st_pos_days, st_pos_days+23, 0, 0, days[day], day_style)
		for pair in range(6):
			ws.write_merge(st_pos_pairs, st_pos_pairs+3, 1, 1, pairs[pair], pair_style)
			st_pos_pairs += 4
		st_pos_days += 24

def SetGroups(groups):			#Функція установки розмітки груп
	st_pos_row = start_pos
	st_pos_col = 2
	ws.write(st_pos_row-2, 1, u'групи', group_pair_style)
	ws.write(st_pos_row-1, 1, u'пари', group_pair_style)
	for group in range(len(groups)):
		ws.write_merge(st_pos_row-2, st_pos_row-1, st_pos_col, st_pos_col, unicode(groups[group]), groups_style)
		ws.col(st_pos_col).width = 0x1950
		st_pos_col += 1

def SetSubject(day, pair, group, pairtype, sybject, audience):		#Фуккція запису предмету в розклад
	st_pos = start_pos
	start_day_pos = st_pos + day*24
	start_pair_pos = pair*4
	start_subj_pos = 0

	start_subj_pos = 0 if pairtype == (1 or 3) else 2
	
	if pairtype == 1 or pairtype == 2:
		ws.write(start_day_pos+start_pair_pos+start_subj_pos, group, sybject, sybject_style1)
		ws.write(start_day_pos+start_pair_pos+start_subj_pos+1, group, audience, sybject_style2)
	elif pairtype == 3:
		ws.write_merge(start_day_pos+start_pair_pos, start_day_pos+start_pair_pos+1, group, group, sybject, sybject_style1)
		ws.write_merge(start_day_pos+start_pair_pos+2, start_day_pos+start_pair_pos+3, group, group, audience, sybject_style2)