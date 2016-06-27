# -*- coding: utf-8 -*-
import pandas
from pprint import pprint

df = pandas.read_json("major_scores.json", orient='records')
df2 = df.sort_values(['university', 'year'], ascending=[0, 1]).drop_duplicates()[['university', 'year', 'score_line', 'avg_score', 'score_diff']]

university = df2[df2['year'] == 2015]['university'].tolist()
df3 = df2[df2['university'].isin(university)]
df3.to_csv("university_scores.csv", encoding="utf-8")
