# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from sce.models import (
    EducativeProgram, GradeLevel, Cohort, SubjectCategory, Subject)
import csv
from slugify import slugify
from students.models import Institute, Student, Teacher


def load_institutes(apps, schema_editor):
    print('\nLoading data for students module')
    print('\n-Loading Institutes')
    institute = Institute(
        name='Colegio Natkan',
    )
    institute.save()
    print('--added Institute: ' + institute.__str__())


def load_educative_programs(apps, schema_editor):
    print("\n-Loading educative programs")
    institute = Institute.objects.get(pk=1)
    with open('students/initial_data/educative_programs.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            else:
                educative_program = EducativeProgram(
                    name=row[0],
                    slug=slugify(row[0], to_lower=True),
                    order=row[2],
                    marking_periods=row[3],
                    num_of_levels=row[4],
                    institute=institute
                )
                educative_program.save()
                print('--added EducativeProgram: ' + educative_program.__str__())


def load_grade_levels(apps, schema_editor):
    print('\n-Loading Grade Levels')
    educative_programs = EducativeProgram.objects.all()
    order = 1
    for educative_program in educative_programs:
        for i in range(1, educative_program.num_of_levels +1):
            grade_level = GradeLevel(
                number=i,
                educative_program=educative_program,
                name=str(i) + '° ' + educative_program.name,
                order=order,
                slug=slugify(str(i) + educative_program.name)
            )
            order += 1
            grade_level.save()
            print('--added GradeLevel: ' + grade_level.__str__())


def load_students(apps, schema_editor):
    print('\n-Load sample students')
    grade_levels = GradeLevel.objects.all()
    with open('students/initial_data/institute_students.csv',  'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            else:
                if row[3] == 'kinder':
                    row[3] = 'preescolar'
                student = Student(
                    institute_id=1,
                    first_name=row[0],
                    last_name=row[1] + ' ' + row[2],
                    grade_level=grade_levels.get(educative_program__slug=row[3], number=row[5].replace('NULL', '')),
                    is_active=row[4]
                )
                student.save()
                print('--added Student: ' + student.__str__())

    print('\n-Load sample teachers')
    teacher1 = Teacher(first_name='José Enrique', last_name='Alvarez Estrada', is_active=True)
    teacher2 = Teacher(first_name='María Montserrat', last_name='Ramírez', is_active=True)
    teacher1.save()
    teacher2.save()
    print('\n--added Teacher:' + teacher1.__str__())
    print('\n--added Teacher:' + teacher2.__str__())


class Migration(migrations.Migration):
    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_institutes),
        migrations.RunPython(load_educative_programs),
        migrations.RunPython(load_grade_levels),
        migrations.RunPython(load_students),
    ]
