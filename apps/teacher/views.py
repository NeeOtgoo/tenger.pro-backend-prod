import os
import pandas as pd
from .models import Teacher
import datetime as dt
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import DateTimeField, DateField, Model, TextField, CharField, ForeignKey, ImageField, EmailField, OneToOneField, CASCADE
from apps.core.models import City, District, Teacher_status, Degree
from django.conf import settings
from apps.school.models import School
from apps.sub_school.models import Sub_school
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

@login_required
def Import_csv(request):
    print('s')


    for teacher in Teacher.objects.all():
        txt = str(teacher.access)

        if "_['" in txt:
            x = txt.replace("['", "")
            x = x.replace("']", "")
            teacher.access = str(x)
            teacher.save()

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
                
                degree_i = Degree.objects.get(pk=dbframe.degree)
                birth_city_i = City.objects.get(pk=dbframe.birth_city)
                birth_district_i = District.objects.get(pk=dbframe.birth_district)
                status_i = Teacher_status.objects.get(pk=dbframe.status)
                sub_school_i = Sub_school.objects.get(pk=dbframe.sub_school)
                school_i = School.objects.get(pk=sub_school_i.school_id)
                create_userID_i = get_user_model().objects.get(pk=1)

                userob = get_user_model()(username=dbframe.username,email=dbframe.email,first_name=dbframe.family_name,last_name=dbframe.name,is_student=False,is_teacher=True,)
                userob.set_password(str(dbframe.password))
                userob.save()
                user_i = get_user_model().objects.get(pk=userob.pk)

                group = Group.objects.get(pk=1)
                group.user_set.add(user_i)

                if len(str(dbframe.join_date))==10:
                    join_date = parse_date(dbframe.join_date)
                else:
                    join_date = "2000-01-01"

                if len(str(dbframe.birthdate))==10:
                    birthdate = parse_date(dbframe.birthdate)
                else:
                    birthdate = "2000-01-01"


                registerNo = str(dbframe.registerNo)[:10] + (str(dbframe.registerNo)[10:] and '')
                phone = str(dbframe.phone)[:8] + (str(dbframe.phone)[8:] and '')
                phone2 = str(dbframe.phone2)[:8] + (str(dbframe.phone2)[8:] and '')

                teacher = Teacher(user=user_i, teacher_code=dbframe.teacher_code, surname=dbframe.surname, family_name=dbframe.family_name, name=dbframe.name, religion=dbframe.religion, registerNo=registerNo, phone=phone, phone2=phone2, address=dbframe.address, address_live=dbframe.address_live, citizen=dbframe.citizen, degree=degree_i, join_date=join_date, join_before=dbframe.join_before, sex=dbframe.sex, birthdate=birthdate, birth_city=birth_city_i, birth_district=birth_district_i, status=status_i, school=school_i, sub_school=sub_school_i, create_userID = create_userID_i)

                try:
                    print("done:")
                    print(type(teacher))
                    print(dbframe.teacher_code)
                    teacher.save()
                except Exception as identifier:
                    print("error:")
                    print(type(teacher))
                    print(dbframe.teacher_code)            
                    print(identifier)
 
            return render(request, 'teacher_import.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'teacher_import.html',{})