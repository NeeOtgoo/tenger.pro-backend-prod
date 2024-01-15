import os
import pandas as pd
from .models import Student
import datetime as dt
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from apps.core.models import City, District, Student_status, Student_status_extra, Activity, Degree, Classtime
from apps.school.models import School
from apps.program.models import Program
from apps.classes.models import Classes
from apps.section.models import Section
from apps.schoolyear.models import Schoolyear
from apps.teacher.models import Teacher
from apps.sub_school.models import Sub_school
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
 
@login_required
def Import_csv(request):
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
                 
                # fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                
                join_schoolyear_i = Schoolyear.objects.get(pk=dbframe.join_schoolyear)
                classtime_i = Classtime.objects.get(pk=dbframe.classtime)
                status_i = Student_status.objects.get(pk=dbframe.status)
                status_extra_i = Student_status_extra.objects.get(pk=dbframe.status_extra)
                degree_i = Degree.objects.get(pk=dbframe.degree)
                birth_city_i = City.objects.get(pk=dbframe.birth_city)
                birth_district_i = District.objects.get(pk=dbframe.birth_district)
                school_i = School.objects.get(pk=dbframe.school)
                program_i = Program.objects.get(pk=dbframe.program)
                classes_i = Classes.objects.get(pk=dbframe.classes)
                activity_i = Activity.objects.get(pk=classes_i.activity.pk)
                create_userID_i = get_user_model().objects.get(pk=1)

                userob = get_user_model()(username=dbframe.username,email=dbframe.email,first_name=dbframe.family_name,last_name=dbframe.name,is_student=True,is_teacher=False,)
                userob.set_password(str(dbframe.password))
                userob.save()
                user_i = get_user_model().objects.get(pk=userob.pk)

                group = Group.objects.get(pk=2)
                group.user_set.add(user_i)

                if len(str(dbframe.phone))>=8:
                    phoner1 = str(dbframe.phone)[:8] + (str(dbframe.phone)[8:] and '')
                else:
                    phoner1 = 0

                if len(str(dbframe.phone2))>=8:
                    phoner2 = str(dbframe.phone2)[:8] + (str(dbframe.phone2)[8:] and '')
                else:
                    phoner2 = 0

             
                section_num = Section.objects.filter(classes=classes_i).count()
                if section_num >= 1:
                    section_i = Section.objects.filter(classes=classes_i).first()
                else:

                    teacher_i = Teacher.objects.latest('id')
                    sub_school_i = Sub_school.objects.latest('id')

                    section = Section(section=str(classes_i.classes)+' - 1', classes=classes_i, program=program_i, sub_school=sub_school_i, school=school_i, create_userID = create_userID_i)
                    section.save()
                    section_i = Section.objects.get(pk=section.pk)

                
                registerNo = str(dbframe.registerNo)[:10] + (str(dbframe.registerNo)[10:] and '')

                stu = Student(user=user_i, student_code=dbframe.student_code, registerNo=registerNo, religion=dbframe.religion, surname=dbframe.surname, family_name=dbframe.family_name, family_name_mgl=dbframe.family_name_mgl, name=dbframe.name, name_mgl=dbframe.name_mgl,nationality=dbframe.nationality, citizen=dbframe.citizen, state=dbframe.state, phone=phoner1, phone2=phoner2, address=dbframe.address, join_date=dbframe.join_date, join_schoolyear=join_schoolyear_i,join_before=dbframe.join_before, sex=dbframe.sex, classtime=classtime_i, status=status_i, status_extra=status_extra_i, degree=degree_i, activity=activity_i,  birthdate="2000-01-01", birth_city=birth_city_i, birth_district=birth_district_i, school=school_i, program=program_i, classes=classes_i, section=section_i, create_userID=create_userID_i)
          
                try:
                    print("done:")
                    print(type(stu))
                    print(dbframe.student_code)
                    stu.save()
                except Exception:
                    print("error:")
                    print(type(stu))
                    print(dbframe.student_code)
 
            return render(request, 'student_import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'student_import.html',{})