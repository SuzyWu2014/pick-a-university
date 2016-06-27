# -*- coding: utf-8 -*-
import pandas
from pprint import pprint

df_university = pandas.read_json("university_scores.json", orient='records')
df_university = df_university.sort_values(['university', 'year'], ascending=[0, 1]).drop_duplicates()[['university', 'year', 'score_line', 'avg_score', 'score_diff']]

university = df_university[df_university['year'] == 2015]['university'].tolist()
df_university = df_university[df_university['university'].isin(university)]

df_ranking = pandas.read_csv('score_ranking.csv')
df_university = df_university.merge(df_ranking, how='left', left_on=['year', 'avg_score'], right_on=['year', 'grade']).drop('grade', axis=1).fillna(0)
# print df_university.head()

df_university.to_csv("university_scores_with_ranking.csv", encoding="utf-8", index=False)
