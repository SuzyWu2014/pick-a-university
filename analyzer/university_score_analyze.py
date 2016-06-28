# -*- coding: utf-8 -*-
import pandas
from pprint import pprint


def create_df_university_scores():
    '''
    convert json data into pandas dataframe, and sort the data by unversity-year
    '''
    df_university = pandas.read_json("university_scores_2011_2015.json", orient='records')
    df_university = df_university.sort_values(['university', 'year'], ascending=[0, 1]).drop_duplicates()[['university', 'year', 'score_line', 'avg_score', 'score_diff']]
    return df_university


def get_university_scores_with_2015(df_university):
    university = df_university[df_university['year'] == 2015]['university'].tolist()
    df_university = df_university[df_university['university'].isin(university)]
    return df_university


def export_to_csv(df_university, filename):
    df_university.to_csv(filename, encoding="utf-8", index=False)


def merge_ranking(df_university):
    df_ranking = pandas.read_csv('scores_ranking_2013_2015.csv')
    df_university = df_university.merge(df_ranking, how='left', left_on=['year', 'avg_score'], right_on=['year', 'grade']).drop('grade', axis=1).fillna(0)
    return df_university


if __name__ == '__main__':
    df_university = create_df_university_scores()
    df_university = merge_ranking(df_university)
    export_to_csv(df_university, 'all_university_scores_with_ranking.csv')
