# -*- coding: utf-8 -*-
import pandas
import re
from pprint import pprint
import numpy

df_major = pandas.read_json("major_scores.json", orient='records')
df_major = df_major.sort_values(['university', 'major', 'year'], ascending=[0, 0, 1]).drop_duplicates()[['university', 'year', 'major', 'avg_score']]
df_major.rename(columns={'avg_score': 'avg_major_score'}, inplace=True)

majors = [u'计算', u'软件', u'网络', u'信息', u'自动化', u'电气', u'电子', u'通信']
pat = '|'.join(map(re.escape, majors))
df_major = df_major[df_major['major'].str.contains(pat)]
df_major['year'] = df_major['year'].str.replace(pat=u'年', repl='').astype(numpy.int32)
# df_major.to_csv("cs_major.csv", encoding="utf-8")

df_ranking = pandas.read_csv('score_ranking.csv')
# print df_ranking.head()

df_major = df_major.merge(df_ranking, how='left', left_on=['year', 'avg_major_score'], right_on=['year', 'grade']).drop('grade', axis=1).fillna(0)

df_university = pandas.read_csv('university_scores.csv', encoding='utf-8')
# print df_university.head()
df_major = df_major.merge(df_university, how='left', left_on=['year', 'university'], right_on=['year', 'university'])
df_major = df_major[(df_major['stu_ranking'] > 5000) & (df_major['stu_ranking'] < 15000)]
df_major.to_csv("major_info_5000_15000.csv", encoding="utf-8")
# print df_major.head()
