# coding: utf-8
from sqlalchemy import Column, MetaData, String, Table

metadata = MetaData()


t_students = Table(
    'students', metadata,
    Column('stu_id', String(10), nullable=False),
    Column('stu_name', String(10), nullable=False)
)
