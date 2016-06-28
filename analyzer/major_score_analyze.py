# -*- coding: utf-8 -*-
import pandas
import re
from pprint import pprint
import numpy


def group_major():
    df_major = pandas.read_json("data/major_scores_2011_2015.json", orient='records')
    df_major = df_major.sort_values(['university', 'major', 'year'], ascending=[0, 0, 1]).drop_duplicates()[['university', 'year', 'major', 'avg_score']]
    df_major.rename(columns={'avg_score': 'avg_major_score'}, inplace=True)
    df_major['year'] = df_major['year'].str.replace(pat=u'年', repl='').astype(numpy.int32)
    return df_major


def merge_ranking(df_major):
    print df_major.head()
    df_ranking = pandas.read_csv('data/scores_ranking_2013_2015.csv', encoding='utf-8')
    print df_ranking.head()
    # df_ranking['year'] = df_ranking['year'].astype(numpy.int32)
    df_major = df_major.merge(df_ranking, how='left', left_on=['year', 'avg_major_score'], right_on=['year', 'grade']).drop('grade', axis=1).fillna(0)
    return df_major


def merge_university(df_major):
    df_university = pandas.read_csv('report/university_scores.csv', encoding='utf-8')
    df_major = df_major.merge(df_university, how='left', left_on=['year', 'university'], right_on=['year', 'university'])
    return df_major


def filter_cs(df_major):
    majors = [u'计算', u'软件', u'网络', u'信息', u'自动化', u'电气', u'电子', u'通信']
    pat = '|'.join(map(re.escape, majors))
    df_major = df_major[df_major['major'].str.contains(pat)]
    return df_major


def filter_ranking(df_major, low, high):
    df_major = df_major[(df_major['stu_ranking'] > low) & (df_major['stu_ranking'] < high)]
    return df_major


def export_to_csv(filename, df_major):
    df_major.to_csv(filename, encoding="utf-8")


if __name__ == '__main__':
    df_major = group_major()
    df_major = merge_ranking(df_major)
    df_major = merge_university(df_major)
    df_major = df_major.sort_values(['university', 'year', 'major'], ascending=[0, 1, 0])
    # df_major = filter_cs(df_major).sort_values(['university', 'year'], ascending=[0, 1])
    # print df_major.head()
    # df_major = filter_ranking(df_major, 5000, 15000)
    export_to_csv('report/all_major.csv', df_major)
