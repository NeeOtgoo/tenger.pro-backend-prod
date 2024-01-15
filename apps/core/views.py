from asyncio.windows_events import NULL
from cmath import exp
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from apps.core.models import City, District, Khoroo, Classtime, Degree, Activity, Student_status, Student_status_extra
from apps.subject.models import Subject
from apps.school.models import School
from apps.sub_school.models import Sub_school
from apps.program.models import Program
from apps.classes.models import Classes
from apps.section.models import Section
from apps.teacher.models import Teacher
from apps.student.models import Student
from apps.routine.models import Routine, Routine_time, Routine_student
from apps.schoolyear.models import Schoolyear
from apps.online_lesson.models import Online_lesson, Online_student, Online_file, Online_sub
from apps.mark.models import Mark_board, Mark_rel, Mark_percentage, Mark
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import timedelta,datetime
from django.utils.dateparse import parse_date
import os

@login_required
def Import_subject(request):
    print('s')    

    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                
                if Subject.objects.filter(subject_code=dbframe.subject_code).exists():

                    subject = Subject.objects.get(subject_code=dbframe.subject_code)

                    if dbframe.credit.isnumeric() == False:
                        credit = 0
                    else:
                        credit = dbframe.credit

                    if(subject.subject == subject.subject_code) or (subject.credit == 0):

                        if dbframe.subject != dbframe.subject_code:
                            try:
                                subject.subject = dbframe.subject
                                subject.subject_mgl = dbframe.subject_mgl
                                subject.subject_eng = dbframe.subject_eng
                                subject.credit = credit
                                subject.save()
                            except Exception as e:
                                print("error:")
                                print(type(subject))
                                print(e)
                                print(dbframe.subject_code)

                    # subject = Subject(
                    #     id=dbframe.id,
                    #     school_id=dbframe.school_id,
                    #     sub_school_id=dbframe.sub_school_id,
                    #     subject=dbframe.subject,
                    #     subject_mgl=dbframe.subject_mgl,
                    #     subject_code=dbframe.subject_code,
                    #     credit=dbframe.credit,
                    #     create_userID=get_user_model().objects.get(pk=1))

                        try:
                            print("done:")
                            print(type(subject))
                            print(dbframe.subject_code)
                        except Exception:
                            print("error:")
                            print(type(subject))
                            print(dbframe.subject_code)
                    else:
                        print("fine:")
                        print(type(subject))
                        print(dbframe.subject_code)
                else:
                    print("not found:")
                    print(type(subject))
                    print(dbframe.subject_code)

 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'import.html',{})

@login_required
def Import_sub_school(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                sub_school = Sub_school(
                    id=dbframe.id,
                    name=dbframe.name,
                    name_mgl=dbframe.name_mgl,
                    school_id=dbframe.school_id)

                try:
                    print("done:")
                    print(type(sub_school))
                    print(dbframe.name)
                    sub_school.save()
                except Exception as e:
                    print("error:")
                    print(type(sub_school))
                    print(dbframe.name)
                    print(e)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_program(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                sub_school = Sub_school.objects.filter(school_id=dbframe.school_id)[:1].get()

                program = Program(
                    id=dbframe.id,
                    program=dbframe.program,
                    program_mgl=dbframe.program_mgl,
                    program_numeric=dbframe.program_numeric,
                    degree_id=dbframe.degree_id,
                    max_student_num=dbframe.max_student_num,
                    school_id=dbframe.school_id,
                    sub_school=sub_school,
                    status=dbframe.status,
                    report_text=dbframe.report_text,
                    create_userID=get_user_model().objects.get(pk=1))

                try:
                    print("done:")
                    print(type(program))
                    print(dbframe.program)
                    program.save()
                except Exception:
                    print("error:")
                    print(type(program))
                    print(dbframe.program)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_classes(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                if dbframe.course==dbframe.end_course:
                    status = 'OPEN'
                else:
                    status = 'CLOSED'

                
                if(type(dbframe.program_id) == 'int'):        
                    try:
                        program = Program.objects.get(pk=dbframe.program_id)
                        sub_school_id = program.sub_school_id
                        school_id = program.school_id
                    except Program.DoesNotExist:
                        sub_school_id = 48
                        school_id = 1
                else:
                    sub_school_id = 48
                    school_id = 1

                if(type(dbframe.degree_id) == 'int'):
                    try:
                        degree = Degree.objects.get(pk=dbframe.degree_id)
                        degree_id = degree.pk
                    except Degree.DoesNotExist:
                        degree_id = 1
                else:
                    degree_id = 1

                    
                if(type(dbframe.activity_id) == 'int'):
                    try:
                        activity = Activity.objects.get(pk=dbframe.activity_id)
                        activity_id = activity.pk
                    except Activity.DoesNotExist:
                        activity_id = 1
                else:
                    activity_id = 1

                if(type(dbframe.program_id) == 'int'):
                    try:
                        program = Program.objects.get(pk=dbframe.program_id)
                        program_id = program.pk
                    except Program.DoesNotExist:
                        program_id = 1
                else:
                    program_id = 1
                

                classes_o = Classes(
                    id=dbframe.id,
                    classes=dbframe.classes,
                    classes_mgl=dbframe.classes_mgl,
                    classes_numeric=dbframe.classes_numeric,
                    degree_id=degree_id,
                    activity_id=activity_id,
                    max_student_num=1000,
                    teacher_id=1508,
                    program_id=program_id,
                    sub_school_id=sub_school_id,
                    school_id=school_id,
                    status=status,
                    course=dbframe.course,
                    end_course=dbframe.end_course,
                    create_userID=get_user_model().objects.get(pk=1))
                classes_o.save()

                section = Section(
                    section=str(dbframe.classes)+' 1',
                    classes=classes_o,
                    program_id=dbframe.program_id,
                    sub_school_id=sub_school_id,
                    school_id=school_id,
                    create_userID = get_user_model().objects.get(pk=1))

                try:
                    print("done:")
                    print(type(classes_o))
                    print(dbframe.classes)
                    section.save()
                except Exception:
                    print("error:")
                    print(type(classes_o))
                    print(dbframe.classes)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Update_classes(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                     
                try:
                    program = Program.objects.get(pk=dbframe.program_id)
                    sub_school_id = program.sub_school_id
                    school_id = program.school_id
                except Program.DoesNotExist:
                    sub_school_id = 48
                    school_id = 1

                try:
                    degree = Degree.objects.get(pk=dbframe.degree_id)
                    degree_id = degree.pk
                except Degree.DoesNotExist:
                    degree_id = 1

                
                try:
                    activity = Activity.objects.get(pk=dbframe.activity_id)
                    activity_id = activity.pk
                except Activity.DoesNotExist:
                    activity_id = 1

                try:
                    program = Program.objects.get(pk=dbframe.program_id)
                    program_id = program.pk
                except Program.DoesNotExist:
                    program_id = 1


                classes_o = Classes.objects.get(pk=dbframe.id)

                classes_o.sub_school_id = sub_school_id
                classes_o.school_id = school_id
                classes_o.degree_id = degree_id
                classes_o.activity_id = activity_id
                classes_o.program_id = program_id
                classes_o.save()

                if Section.objects.filter(classes_id=dbframe.id).exists():

                    section = Section.objects.filter(classes_id=dbframe.id)[:1].get()
                    section.sub_school_id = sub_school_id
                    section.school_id = school_id
                    section.program_id = program_id
                    section.save()
                else:
                    section = Section(
                    section=str(dbframe.classes)+' 1',
                    classes=classes_o,
                    program_id=program_id,
                    sub_school_id=sub_school_id,
                    school_id=school_id,
                    create_userID = get_user_model().objects.get(pk=1))
                    section.save()

                try:
                    print("done:")
                    print(type(classes_o))
                    print(dbframe.classes)
                    
                except Exception:
                    print("error:")
                    print(type(classes_o))
                    print(dbframe.classes)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_teacher(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                userob = get_user_model()(
                    username=dbframe.username,
                    email=dbframe.email,
                    first_name=dbframe.family_name,
                    last_name=dbframe.name,
                    is_student=False,
                    is_teacher=True,
                    is_parent=False,)
                userob.set_password(dbframe.password)
                
                userob.save()
                user_i = get_user_model().objects.get(pk=userob.pk)

                group = Group.objects.get(pk=1)
                group.user_set.add(user_i)

                if len(str(dbframe.join_date))==10:
                    join_date = dbframe.join_date
                else:
                    join_date = "2000-01-01"

                if len(str(dbframe.birthdate))==10:
                    birthdate = parse_date(dbframe.birthdate)
                else:
                    birthdate = "2000-01-01"

                registerNo = str(dbframe.registerNo)[:10] + (str(dbframe.registerNo)[10:] and '')
                phone = str(dbframe.phone)[:8] + (str(dbframe.phone)[8:] and '')
                phone2 = str(dbframe.phone2)[:8] + (str(dbframe.phone2)[8:] and '')

                try:
                    birth_city = City.objects.get(pk=dbframe.birth_city_id)
                    birth_city_id = birth_city.pk
                except City.DoesNotExist:
                    birth_city_id = 20
                try:
                    birth_district = District.objects.get(pk=dbframe.birth_district_id)
                    birth_district_id = birth_district.pk
                except District.DoesNotExist:
                    birth_district_id = 346

                teacher_o = Teacher(
                    user=user_i,
                    teacher_code=dbframe.username,
                    access='A_'+str(dbframe.access),
                    surname=dbframe.surname,
                    family_name=dbframe.family_name,
                    name=dbframe.name,
                    religion=dbframe.religion,
                    registerNo=registerNo,
                    phone=phone,
                    phone2=phone2,
                    address=dbframe.address,
                    address_live=dbframe.address_live,
                    citizen=dbframe.citizen,
                    degree_id=dbframe.degree_id,
                    join_date=join_date,
                    join_before=dbframe.join_before,
                    sex=dbframe.sex,
                    birthdate=birthdate,
                    birth_city_id=birth_city_id,
                    birth_district_id=birth_district_id,
                    status_id=dbframe.status_id,
                    school_id=dbframe.school_id,
                    sub_school_id=dbframe.sub_school_id,
                    create_userID = get_user_model().objects.get(pk=1)
                    )
                
                try:
                    print("done:")
                    print(type(teacher_o))
                    print(dbframe.teacher_code)
                    teacher_o.save()
                except Exception as e:
                    print("error:")
                    print(type(teacher_o))
                    print(dbframe.teacher_code)
                    print(e)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_student(request):
    print('s')
    # get_user_model().objects.filter(is_student=True).delete()        
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                registerNo = str(dbframe.registerNo)[:10] + (str(dbframe.registerNo)[10:] and '')

                userob = get_user_model()(
                    username=dbframe.student_code,
                    email='email@email.com',
                    first_name=dbframe.family_name,
                    last_name=dbframe.name,
                    is_student=True,
                    is_teacher=False,
                    is_parent=False,)
                userob.set_password(registerNo)
                userob.save()
                user_i = get_user_model().objects.get(pk=userob.pk)

                group = Group.objects.get(pk=2)
                group.user_set.add(user_i)

                if len(str(dbframe.join_date))==10:
                    join_date = dbframe.join_date
                else:
                    join_date = "1900-01-01"

                if len(str(dbframe.birthdate))==10:
                    birthdate = parse_date(dbframe.birthdate)
                else:
                    birthdate = "1900-01-01"

                phone = str(dbframe.phone)[:8] + (str(dbframe.phone)[8:] and '')
                phone2 = str(dbframe.phone2)[:8] + (str(dbframe.phone2)[8:] and '')

                if(type(dbframe.birth_city_id) == 'int'):
                    try:
                        birth_city = City.objects.get(pk=dbframe.birth_city_id)
                        birth_city_id = birth_city.pk
                    except City.DoesNotExist:
                        birth_city_id = 20
                else:
                    birth_city_id = 20

                if(type(dbframe.birth_district_id) == 'int'):
                    try:
                        birth_district = District.objects.get(pk=dbframe.birth_district_id)
                        birth_district_id = birth_district.pk
                    except District.DoesNotExist:
                        birth_district_id = 346
                else:
                    birth_district_id = 346

                if(type(dbframe.school_id) == 'int'):        
                    try:
                        school = School.objects.get(pk=dbframe.school_id)
                        school_id = school.pk
                    except School.DoesNotExist:
                        school_id = 1
                else:
                    school_id = 1

                if(type(dbframe.program_id) == 'int'):
                    try:
                        program = Program.objects.get(pk=dbframe.program_id)
                        program_id = program.pk
                    except Program.DoesNotExist:
                        program_id = 1
                else:
                    program_id = 1

                if(type(dbframe.classes_id) == 'int'):        
                    try:
                        classes = Classes.objects.get(pk=dbframe.classes_id)
                        classes_id = classes.pk
                    except Classes.DoesNotExist:
                        classes_id = 14
                else:
                    classes_id = 14

                if(type(dbframe.classes_id) == 'int'):        
                    try:
                        section = Section.objects.filter(classes_id=dbframe.classes_id)[:1].get()
                        section_id = section.pk
                    except Section.DoesNotExist:
                        section_id = 1
                else:
                    section_id = 1

                    # asdasd2 
                if(type(dbframe.join_schoolyear_id) == 'int'):        
                    try:
                        schoolyear = Schoolyear.objects.get(pk=dbframe.join_schoolyear_id)
                        join_schoolyear_id = schoolyear.pk
                    except Schoolyear.DoesNotExist:
                        join_schoolyear_id = 13
                else:
                    join_schoolyear_id = 13

                        
                if(type(dbframe.classtime_id) == 'int'):        
                    try:
                        classtime = Classtime.objects.get(pk=dbframe.classtime_id)
                        classtime_id = classtime.pk
                    except Classtime.DoesNotExist:
                        classtime_id = 1
                else:
                    classtime_id = 1

                        
                if(type(dbframe.status_id) == 'int'):        
                    try:
                        status = Student_status.objects.get(pk=dbframe.status_id)
                        status_id = status.pk
                    except Student_status.DoesNotExist:
                        status_id = 2
                else:
                    status_id = 2

                        
                if(type(dbframe.status_extra_id) == 'int'):        
                    try:
                        status_extra = Student_status_extra.objects.get(pk=dbframe.status_extra_id)
                        status_extra_id = status_extra.pk
                    except Student_status_extra.DoesNotExist:
                        status_extra_id = 1
                else:
                    status_extra_id = 1

                    
                if(type(dbframe.degree_id) == 'int'):
                    try:
                        degree = Degree.objects.get(pk=dbframe.degree_id)
                        degree_id = degree.pk
                    except Degree.DoesNotExist:
                        degree_id = 1
                else:
                    degree_id = 1

                    
                if(type(dbframe.activity_id) == 'int'):
                    try:
                        activity = Activity.objects.get(pk=dbframe.activity_id)
                        activity_id = activity.pk
                    except Activity.DoesNotExist:
                        activity_id = 1
                else:
                    activity_id = 1


                stu = Student(
                    user=user_i,
                    student_code=dbframe.student_code,
                    registerNo=registerNo,
                    religion=dbframe.religion,
                    surname=dbframe.surname,
                    family_name=dbframe.family_name,
                    family_name_mgl=dbframe.family_name_mgl,
                    name=dbframe.name,
                    name_mgl=dbframe.name_mgl,
                    nationality=dbframe.nationality,
                    citizen=dbframe.citizen,
                    state=dbframe.state,
                    phone=phone,
                    phone2=phone2,
                    address=dbframe.address,
                    address_live=dbframe.address_live,
                    join_date=join_date,
                    join_schoolyear_id=join_schoolyear_id,
                    join_before=dbframe.join_before,
                    sex=dbframe.sex,
                    classtime_id=classtime_id,
                    status_id=status_id,
                    status_extra_id=status_extra_id,
                    degree_id=degree_id,
                    activity_id=activity_id,
                    birthdate=birthdate,
                    birth_city_id=birth_city_id,
                    birth_district_id=birth_district_id,
                    school_id=school_id,
                    program_id=program_id,
                    classes_id=classes_id,
                    section_id=section_id,
                    create_userID=get_user_model().objects.get(pk=1))
                try:
                    print("done:")
                    print(type(stu))
                    print(dbframe.student_code)
                    stu.save()
                except Exception as e:
                    print("error:")
                    print(type(stu))
                    print(dbframe.student_code)
                    print(e)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

    
@login_required
def Update_student(request):
    print('s')
    # get_user_model().objects.filter(is_student=True).delete()        
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                try:
                    birth_city = City.objects.get(pk=dbframe.birth_city_id)
                    birth_city_id = birth_city.pk
                except City.DoesNotExist:
                    birth_city_id = 20

                try:
                    birth_district = District.objects.get(pk=dbframe.birth_district_id)
                    birth_district_id = birth_district.pk
                except District.DoesNotExist:
                    birth_district_id = 346
       
                try:
                    school = School.objects.get(pk=dbframe.school_id)
                    school_id = school.pk
                except School.DoesNotExist:
                    school_id = 1

                try:
                    program = Program.objects.get(pk=dbframe.program_id)
                    program_id = program.pk
                except Program.DoesNotExist:
                    program_id = 1
     
                try:
                    classes = Classes.objects.get(pk=dbframe.classes_id)
                    classes_id = classes.pk
                except Classes.DoesNotExist:
                    classes_id = 14

                try:
                    section = Section.objects.filter(classes_id=dbframe.classes_id)[:1].get()
                    section_id = section.pk
                except Section.DoesNotExist:
                    section_id = 1
                    # asdasd2       
                try:
                    schoolyear = Schoolyear.objects.get(pk=dbframe.join_schoolyear_id)
                    join_schoolyear_id = schoolyear.pk
                except Schoolyear.DoesNotExist:
                    join_schoolyear_id = 13
                
                try:
                    classtime = Classtime.objects.get(pk=dbframe.classtime_id)
                    classtime_id = classtime.pk
                except Classtime.DoesNotExist:
                    classtime_id = 1
 
                try:
                    status = Student_status.objects.get(pk=dbframe.status_id)
                    status_id = status.pk
                except Student_status.DoesNotExist:
                    status_id = 2
                                
                try:
                    status_extra = Student_status_extra.objects.get(pk=dbframe.status_extra_id)
                    status_extra_id = status_extra.pk
                except Student_status_extra.DoesNotExist:
                    status_extra_id = 1
                    
                try:
                    degree = Degree.objects.get(pk=dbframe.degree_id)
                    degree_id = degree.pk
                except Degree.DoesNotExist:
                    degree_id = 1
                    
                try:
                    activity = Activity.objects.get(pk=dbframe.activity_id)
                    activity_id = activity.pk
                except Activity.DoesNotExist:
                    activity_id = 1

                if Student.objects.filter(student_code=dbframe.student_code).exists():

                    student = Student.objects.filter(student_code=dbframe.student_code)[:1].get()

                    student.join_schoolyear_id = join_schoolyear_id
                    student.classtime_id = classtime_id
                    student.status_id = status_id
                    student.status_extra_id = status_extra_id
                    student.degree_id = degree_id
                    student.activity_id = activity_id
                    student.birth_city_id = birth_city_id
                    student.birth_district_id = birth_district_id
                    student.school_id = school_id
                    student.program_id = program_id
                    student.classes_id = classes_id
                    student.section_id = section_id

                    try:
                        print("done:")
                        print(type(student))
                        print(student)
                        student.save()
                    except Exception as e:
                        print("error:")
                        print(type(student))
                        print(dbframe.student_code)
                        print(e)
                else:
                    print("error: student not found")
                    print(dbframe.student_code)
                    print(e)

 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_schoolyear(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                schoolyear = Schoolyear(
                    id=dbframe.id,
                    schoolyear=dbframe.schoolyear,
                    season=dbframe.season,
                    semester_code=dbframe.semester_code,
                    start_date=dbframe.start_date,
                    end_date=dbframe.end_date,
                    is_current=dbframe.is_current,
                    create_userID=get_user_model().objects.get(pk=1))
                try:
                    print("done:")
                    print(type(schoolyear))
                    print(dbframe.schoolyear)
                    schoolyear.save()
                except Exception:
                    print("error:")
                    print(type(schoolyear))
                    print(dbframe.schoolyear)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})
    
@login_required
def Import_routine(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():


                if Teacher.objects.filter(teacher_code=dbframe.username).exists():
                    teacher_o = Teacher.objects.get(teacher_code=dbframe.username)

                    try:
                        subject_o = Subject.objects.get(subject_code=dbframe.subject_code_o)
                    except Subject.DoesNotExist:

                        subject_o = Subject(
                            school_id=1,
                            sub_school_id=48,
                            subject=dbframe.subject_code_o,
                            subject_mgl=dbframe.subject_code_o,
                            subject_code=dbframe.subject_code_o,
                            credit=0,
                            create_userID=get_user_model().objects.get(pk=1))
                        subject_o.save()


                    try:
                        program = Program.objects.get(pk=dbframe.program_id)
                        program_id = program.pk
                    except Program.DoesNotExist:
                        program_id = 1
 
                    try:
                        classes = Classes.objects.get(pk=dbframe.classes_id)
                        classes_id = classes.pk
                    except Classes.DoesNotExist:
                        classes_id = 14
      
                    try:
                        section = Section.objects.filter(classes_id=dbframe.classes_id)[:1].get()
                        section_id = section.pk
                    except Section.DoesNotExist:
                        section_id = 1

                    routine_o = Routine(
                        schoolyear_id=dbframe.schoolyear_id,
                        program_id=program_id,
                        classes_id=classes_id,
                        section_id=section_id,
                        subject=subject_o,
                        teacher=teacher_o,
                        create_userID=get_user_model().objects.get(pk=1))
                    routine_o.save()

                    routine_inserted = Routine.objects.latest('id')

                    delta = timedelta(days=7)
    
                    d = datetime(2022, 2, 1)
                    offset = int(dbframe.day)-d.weekday() #weekday = 1 means tuesday
                    if offset < 0:
                        offset+=7
                    print( d+timedelta(offset))

                    start_date = d+timedelta(offset)
                    start_date = start_date.date()
                    end_date = parse_date('2022-06-01')

                    while start_date <= end_date:

                        routine_time_o = Routine_time(
                            routine=routine_inserted,
                            type=dbframe.type,
                            time=int(dbframe.time),
                            date=start_date,
                            room=dbframe.room)
                        routine_time_o.save()

                        start_date += delta

                    for student in Student.objects.filter(program_id=program_id,classes_id=classes_id,section_id=section_id):

                        routine_student_o = Routine_student(routine=routine_inserted, student=student)
                        routine_student_o.save()

                    print("done:")
                    print(type(routine_o))
                    print(dbframe.username)
                else:
                    print("error: teacher not found")
                    print(dbframe.username)

 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_online_lesson(request):
    print('s')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            i = 0
            for dbframe in dbframe.itertuples():
                i += 1 
                # '''SELECT `syllabus`.*, `teacher`.`username`, `subject`.`subject_code`
                # FROM `syllabus`
                # INNER JOIN `teacher` ON `teacher`.teacherID = `syllabus`.userID
                # INNER JOIN `routine` ON `routine`.routineID = `syllabus`.routineID
                # INNER JOIN `subject` ON `subject`.subjectID = `routine`.subjectID
                # WHERE `syllabus`.`usertypeID` = 2'''

                title_o = str(dbframe.title)[:110]
                description_o = dbframe.description
                originalfile = dbframe.originalfile
                file_o = dbframe.file
                subject_code_o = dbframe.subject_code
                creator_username = dbframe.creator_username
                schoolyearID = dbframe.schoolyearID
                
                try:
                    program = Program.objects.get(pk=dbframe.program_id)
                    program_id = program.pk
                except Program.DoesNotExist:
                    program_id = 1
 
                try:
                    classes = Classes.objects.get(pk=dbframe.classes_id)
                    classes_id = classes.pk
                except Classes.DoesNotExist:
                    classes_id = 14
      
                try:
                    section = Section.objects.filter(classes_id=dbframe.classes_id)[:1].get()
                    section_id = section.pk
                except Section.DoesNotExist:
                    section_id = 1

                if (os.path.isfile('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(file_o))==True) or (os.path.isfile('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(originalfile))==True) or (os.path.isfile('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/['+str(i)+']'+str(originalfile))==True):

                    if os.path.isfile('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(file_o))==True:

                        if os.path.isfile('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(originalfile))==True:

                            try:

                                os.rename('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(file_o), 'C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/['+str(i)+']'+str(originalfile))

                                originalfile = '['+str(i)+']'+originalfile
                            except:
                                originalfile = file_o
                            
                        else:
                            try:
                                os.rename('C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(file_o), 'C:/Emind/school/media/static/uploads/default/online_lessons/2022/03/27/'+str(originalfile))

                                originalfile = originalfile
                            except:
                                originalfile = file_o

                    creator = get_user_model().objects.get(username=creator_username)

                    try:
                        online_file_o = Online_file.objects.get(file='static/uploads/default/online_lessons/2022/03/27/'+str(originalfile),create_userID=creator)
                    except Online_file.DoesNotExist:
                        online_file_o = Online_file(file='static/uploads/default/online_lessons/2022/03/27/'+str(originalfile), create_userID=creator)
                        online_file_o.save()

                    try:
                        subject_o = Subject.objects.get(subject_code=subject_code_o)
                    except Subject.DoesNotExist:

                        subject_o = Subject(
                            school_id=1,
                            sub_school_id=48,
                            subject=subject_code_o,
                            subject_mgl=subject_code_o,
                            subject_code=subject_code_o,
                            credit=0,
                            create_userID=get_user_model().objects.get(pk=1))
                        subject_o.save()

                    try:
                        online_lesson_o = Online_lesson.objects.get(subject=subject_o)
                    except Online_lesson.DoesNotExist:
                        online_lesson_o = Online_lesson(
                            schoolyear_id=schoolyearID,
                            subject=subject_o,
                            description=description_o,
                            content=description_o,
                            status='OPEN',
                            create_userID=creator)
                        online_lesson_o.save()

                        for student in Student.objects.filter(program_id=program_id,classes_id=classes_id,section_id=section_id):

                            online_student_o = Online_student(online_lesson=online_lesson_o, student=student)
                            online_student_o.save()

                    online_sub = Online_sub(
                        title=title_o,
                        description=description_o,
                        content=description_o,
                        status='OPEN',
                        online_lesson=online_lesson_o,
                        online_file=online_file_o,
                        online_type_id = 1,
                        create_userID=creator)
                    online_sub.save()

                
                    print("done:")
                    print(type(online_sub))
                    print(title_o)
                else:
                    print("error file not found:")
                    print(file_o)

             
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

    
@login_required
def Import_mark(request):
    print('s')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                
                # '''SELECT `mark`.*, `student`.`username`, `subject`.`subject_code`, `markrelation`.`mark`, `markrelation`.`mark2`
                # FROM `mark`
                # INNER JOIN `student` ON `student`.studentID = `mark`.studentID
                # INNER JOIN `subject` ON `mark`.subjectID = `subject`.subjectID
                # INNER JOIN `markrelation` ON `mark`.markID = `markrelation`.markID
                # WHERE `markrelation`.mark IS NOT NULL AND `markrelation`.mark2 IS NOT NULL
                # GROUP BY `mark`.markID'''

                subject_code_o = dbframe.subject_code
                student_username = dbframe.student_username
                schoolyearID = dbframe.schoolyearID
                year = parse_date(str(dbframe.year)+'-01-01')
                mark1 = dbframe.mark1
                mark2 = dbframe.mark2

                

                if Student.objects.filter(student_code=student_username).exists():

                    student_o = Student.objects.get(student_code=student_username)

                    try:
                        subject_o = Subject.objects.get(subject_code=subject_code_o)
                    except Subject.DoesNotExist:

                        sub_school = Sub_school.objects.filter(school=student_o.school).first()
                        subject_o = Subject(
                            school=student_o.school,
                            sub_school=sub_school,
                            subject=subject_code_o,
                            subject_mgl=subject_code_o,
                            subject_code=subject_code_o,
                            credit=0,
                            create_userID=get_user_model().objects.get(pk=1))
                        subject_o.save()

                    try:
                        mark_board_o = Mark_board.objects.get(
                            schoolyear_id=schoolyearID,
                            subject=subject_o,
                        )
                    except Mark_board.DoesNotExist:
                        mark_board_o = Mark_board(
                            schoolyear_id=schoolyearID,
                            subject=subject_o,
                            teacher_id=377,
                            start_at=year,
                            end_at=year,
                            status='CLOSED',
                            create_userID=get_user_model().objects.get(pk=1))
                        mark_board_o.save()

                    student_o = Student.objects.get(student_code=student_username)

                    mark = Mark(
                        mark_board=mark_board_o,
                        student=student_o,
                        create_userID=get_user_model().objects.get(pk=1))
                    mark.save()

                    mark_board_o1 = Mark_rel(
                        mark=mark,
                        mark_setting_id=1,
                        mark_val=mark1)
                    mark_board_o1.save()

                    mark_board_o2 = Mark_rel(
                        mark=mark,
                        mark_setting_id=2,
                        mark_val=mark2)
                    mark_board_o2.save()

                
                    print("done:")
                    print(type(mark_board_o1))
                    print(type(mark_board_o2))
                    print(dbframe.subject_code)
                else:
                    print("error: student not found" + str(student_username))
                    print(type(mark_board_o1))
                    print(type(mark_board_o2))
                    print(dbframe.subject_code)


 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})

@login_required
def Import_percentage(request):
    print('s')
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                mark_percentage = Mark_percentage(
                    type=dbframe.type,
                    percentage=dbframe.percentage,
                    diam=dbframe.diam,
                    create_userID=get_user_model().objects.get(pk=1))
                mark_percentage.save()
                
                print("done:")
                print(type(mark_percentage))
                print(dbframe.percentage)
 
            return render(request, 'import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)

    return render(request, 'import.html',{})