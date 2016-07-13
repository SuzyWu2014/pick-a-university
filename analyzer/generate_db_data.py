# -*- coding: utf-8 -*-
import pandas
import numpy


def export_to_csv(df, filename):
    df.to_csv(filename, encoding="utf-8", index=True)


def create_rankings():
    df_ranking = pandas.read_csv('data/scores_ranking_2013_2015.csv')
    # add student_pool_id column; value = 1
    df_ranking['STUDENT_POOL_ID'] = 1
    export_to_csv(df_ranking, "db_data/Ranking.csv")


def createUniversities():
    df_university = pandas.read_csv('report/all_univesity.csv')
    df_university = df_university[['university', 'is_985', 'is_211']]
    df_university = df_university.drop_duplicates()
    export_to_csv(df_university, "db_data/university.csv")


def createEnrollmentUniversity():
    # ID, StudentPool, year, UniversityID, score_avg, stu_count
    df_enroll_university = pandas.read_csv('report/all_univesity.csv')
    df_university = pandas.read_csv("db_data/university.csv")
    #  merge id
    df_enroll_university = df_enroll_university[['university', 'year', 'avg_score', 'admission_count']].drop_duplicates()
    df_enroll_university['student_pool_id'] = 1
    df_university = pandas.read_csv("db_data/university.csv")

    export_to_csv(df_enroll_university, "db_data/enroll_university.csv")


def createEnrollmentMajor():
    # ID, studentPool_id, universityID, year, major, score_avg
    pass


if __name__ == '__main__':
    createUniversities()
