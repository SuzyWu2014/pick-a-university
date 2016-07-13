# -*- coding: utf-8 -*-
import pandas
from pprint import pprint
import numpy


def create_df_university_scores():
    '''
    convert json data into pandas dataframe,
    and sort the data by unversity-year
    '''
    df_university = pandas.read_json(
        "data/university_scores_2011_2015.json", orient='records')
    df_university = df_university.sort_values(
        ['university', 'year'],
        ascending=[0, 1]).drop_duplicates()[[
            'university', 'year', 'score_line', 'avg_score', 'score_diff']]
    return df_university


def get_university_scores_with_2015(df_university):
    university = df_university[
        df_university['year'] == 2015]['university'].tolist()
    df_university = df_university[df_university['university'].isin(university)]
    return df_university


def export_to_csv(df_university, filename):
    df_university.to_csv(filename, encoding="utf-8", index=False)


def merge_ranking(df_university):
    df_ranking = pandas.read_csv('data/scores_ranking_2013_2015.csv')
    df_university = df_university.merge(
        df_ranking, how='left',
        left_on=['year', 'avg_score'],
        right_on=['year', 'grade']).drop(
        'grade', axis=1).fillna(0)
    return df_university


def merge985_211(df_university):
    list_985 = pandas.read_csv(
        'data/university_985_list.csv', encoding="utf-8")
    list_211 = pandas.read_csv(
        'data/university_211_list.csv', encoding='utf-8')
    list_985 = list_985['985']
    list_211 = list_211['211']
    df_university['is_985'] = numpy.where(
        df_university['university'].isin(list_985), 1, 0)
    df_university['is_211'] = numpy.where(
        df_university['university'].isin(list_211), 1, 0)
    # df_university['is_985'] = numpy.where(
    #     df_university['university'].isin(list_985), '985', 'not_985')
    # df_university['is_211'] = numpy.where(
    #     df_university['university'].isin(list_211), '211', 'not_211')
    return df_university


def merge_admission(df_university):
    df_admission = pandas.read_json(
        'data/admission_2012_2013.json',
        orient='records')
    df_university = df_university.merge(
        df_admission,
        how='left',
        left_on=['year', 'university'],
        right_on=['year', 'university']).drop(
        ['stu_type', 'avg_score_y'],
        axis=1).fillna(0)
    return df_university


def count_admission(df_university):
    grouped = df_university.groupby(['is_985', 'is_211', 'year'], axis=0)
    # print grouped.count()
    admission_count = grouped['admission_count'].agg(
        {'admission_count': numpy.sum, 'university': numpy.count_nonzero})
    # print admission_count
    admission_count.to_csv(
        'report/admission_count_2012_2013.csv', encoding="utf-8", index=False)


def merge_all():
    df_university = create_df_university_scores()
    # df_university = merge_ranking(df_university)
    df_university = merge985_211(df_university)
    df_university = merge_admission(df_university)
    return df_university


if __name__ == '__main__':
    df_university = merge_all()
    df_university.to_csv("report/all_univesity.csv", encoding="utf-8", index=False)
