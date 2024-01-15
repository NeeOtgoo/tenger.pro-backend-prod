import graphene
from graphene_django.types import DjangoObjectType
from django.db import connections
from json import dumps
from apps.student.models import Student
from apps.teacher.models import Teacher
from apps.parent.models import Parent
from apps.school.models import School
from apps.program.models import Program
from apps.schoolyear.models import Schoolyear
from apps.mark.models import Mark_rel, Mark_board, Mark, Mark_percentage
from apps.subject.models import Subject
from tenants.middlewares import get_current_db_name
from django.db.models import Sum

class StudentreportType(graphene.ObjectType):
    school = graphene.String()
    text_top = graphene.String()
    text_mid = graphene.String()
    text_bottom = graphene.String()
    student_photo = graphene.String()
    student_code = graphene.String()

class Student_markreportType(graphene.ObjectType):
    school = graphene.String()
    text_top = graphene.String()
    text_mid0 = graphene.String()
    text_mid1 = graphene.String()
    text_mid2 = graphene.String()
    text_mid3 = graphene.String()
    text_mid4 = graphene.String()
    text_mid5 = graphene.String()
    text_mid6 = graphene.String()
    text_mid7 = graphene.String()
    text_bottom = graphene.String()
    student_photo = graphene.String()
    student_code = graphene.String()

class Markcon_studentType(graphene.ObjectType):
    student_id = graphene.String()
    family_name = graphene.String()
    name = graphene.String()
    student_code = graphene.String()
    registerNo = graphene.String()

class Markcon_subjectType(graphene.ObjectType):
    subject_id = graphene.String()
    subject = graphene.String()
    subject_code = graphene.String()
    subject_credit = graphene.String()

class Mark_con_relType(graphene.ObjectType):
    mark_val = graphene.String()
    mark_setting = graphene.String()

class Mark_conType(graphene.ObjectType):
    percentage = graphene.String()
    mark_rel = graphene.List(Mark_con_relType)
    diam = graphene.String()

class Student_schoolyearType(DjangoObjectType):
    class Meta:
        model = Schoolyear

class Student_mark_relType(DjangoObjectType):
    class Meta:
        model = Mark_rel

class StudentMarkType(DjangoObjectType):
    class Meta:
        model = Mark

class Mark_percentagetypeType(DjangoObjectType):
    class Meta:
        model = Mark_percentage

class LoginCountType(graphene.ObjectType):
    login_date = graphene.Date()
    login_count = graphene.Int()

class DashboardType(graphene.ObjectType):
    student_count = graphene.Int()
    teacher_count = graphene.Int()
    parent_count = graphene.Int()
    subject_count = graphene.Int()
    logins = graphene.List(LoginCountType)

class Query(graphene.ObjectType):
    dashboard = graphene.Field(DashboardType)
    student_report = graphene.Field(StudentreportType, student_code=graphene.String())
    student_report_section = graphene.List(StudentreportType, section=graphene.Int())
    student_mark_report = graphene.Field(Student_markreportType, student_code=graphene.String())
    student_mark_report_section = graphene.List(Student_markreportType, section=graphene.Int())
    student_schoolyear = graphene.List(Student_schoolyearType, student=graphene.Int(required=False, default_value=0))
    student_mark_rel = graphene.List(Student_mark_relType, student=graphene.Int(required=False, default_value=0), schoolyear=graphene.Int())
    student_mark = graphene.List(StudentMarkType, student=graphene.Int(required=False, default_value=0), schoolyear=graphene.Int(), part=graphene.String())
    mark_percentage = graphene.Field(Mark_percentagetypeType, percentage=graphene.Int())

    markcon_student = graphene.List(Markcon_studentType, section=graphene.Int(required=True))
    markcon_subject = graphene.List(Markcon_subjectType, section=graphene.Int(required=True), schoolyear=graphene.Int(required=True), part=graphene.String(required=True))
    mark_con = graphene.Field(Mark_conType, subject=graphene.Int(required=True), schoolyear=graphene.Int(required=True), student=graphene.Int(required=True))

    def resolve_dashboard(self, info):
        cursor = connections[get_current_db_name()].cursor()

        student_count = Student.objects.filter(classes__status="OPEN").count() 

        teacher_count = Teacher.objects.all().count()
        
        parent_count = Parent.objects.all().count()

        subject_count = Subject.objects.all().count()

        cursor.execute("SELECT DATE_TRUNC('day', ""expire_date"") AS ""day"", COUNT(""expire_date"") AS ""number_of_users"" FROM ""django_session"" GROUP BY DATE_TRUNC('day', ""expire_date"") ORDER BY day ASC LIMIT 6;")
        row5 = cursor.fetchall()
        # row5 = dumps(row5, indent=4, sort_keys=True, default=str)

        login_array = []

        for i in row5:
            login_array.append(LoginCountType(i[0], i[1]))

        sections = {
            'student_count': student_count,
            'teacher_count': teacher_count,
            'parent_count': parent_count,
            'subject_count': subject_count,
            'logins': login_array
        }
        return sections
    
    def resolve_student_report(self, info, student_code):

        if info.context.user.is_anonymous==True:
            student = Student.objects.get(student_code=student_code)
        else:
            if info.context.user.is_student==True:
                student = Student.objects.get(user=info.context.user)
            else:
                student = Student.objects.get(student_code=student_code)

        school = School.objects.get(pk=student.school_id)
        program = Program.objects.get(pk=student.program_id)

        return {"school":school.name,"text_top":school.report_text,"text_mid":"<b>"+student.family_name + "</b> овогтой <b>"+student.name+"</b> нь тус сургуулийн <b>"+program.program+"</b> хөтөлбөрөөр сурдаг нь үнэн болно<br>Суралцагчийн дугаар: <b>"+student.student_code+"</b> Регистрийн дугаар :<b>"+student.registerNo+"</b>","text_bottom":program.report_text,"student_photo":"/media/"+str(student.photo),"student_code":student.student_code}

    def resolve_student_report_section(self, info, section):
      
        reports = []

        for student in Student.objects.filter(section_id=section):
            school = School.objects.get(pk=student.school_id)
            program = Program.objects.get(pk=student.program_id)

            reports.append({"school":school.name,"text_top":school.report_text,"text_mid":"<b>"+student.family_name + "</b> овогтой <b>"+student.name+"</b> нь тус сургуулийн <b>"+program.program+"</b> хөтөлбөрөөр сурдаг нь үнэн болно<br>Суралцагчийн дугаар: <b>"+student.student_code+"</b> Регистрийн дугаар :<b>"+student.registerNo+"</b>","text_bottom":program.report_text,"student_photo":"/media/"+str(student.photo),"student_code":student.student_code}) 

        return reports

    def resolve_student_mark_report(self, info, student_code):
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
        else:
            student = Student.objects.get(student_code=student_code)

        school = School.objects.get(pk=student.school_id)
        program = Program.objects.get(pk=student.program_id)
        schoolyear = Schoolyear.objects.last()

        return {
            "school":school.name,
            "text_top":school.report_text,
            "text_mid0": student.pk,
            "text_mid1": student.family_name,
            "text_mid2": student.name,
            "text_mid3": student.registerNo,
            "text_mid4": schoolyear.schoolyear,
            "text_mid5": program.program_numeric,
            "text_mid6": program.program,
            "text_mid7": program.degree.name,
            "text_bottom":program.report_text,
            "student_photo":"/media/"+str(student.photo),
            "student_code":student.student_code
        }

    def resolve_student_mark_report_section(self, info, section):

        reports = []

        for student in Student.objects.filter(section_id=section):
            school = School.objects.get(pk=student.school_id)
            program = Program.objects.get(pk=student.program_id)
            schoolyear = Schoolyear.objects.last()

            reports.append({
                "school":school.name,
                "text_top":school.report_text,
                "text_mid0": student.pk,
                "text_mid1": student.family_name,
                "text_mid2": student.name,
                "text_mid3": student.registerNo,
                "text_mid4": schoolyear.schoolyear,
                "text_mid5": program.program_numeric,
                "text_mid6": program.program,
                "text_mid7": program.degree.name,
                "text_bottom":program.report_text,
                "student_photo":"/media/"+str(student.photo),
                "student_code":student.student_code
            }) 

        return reports

    def resolve_student_schoolyear(self, info, student):

        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user).id

        schoolyears = Mark_board.objects.filter(mark__student_id=student).values('schoolyear_id')
        return Schoolyear.objects.filter(pk__in=schoolyears)

    def resolve_student_mark_rel(self, info, student, schoolyear):
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user).id

        mark_boards = Mark_board.objects.filter(schoolyear_id=schoolyear).values('id')
        marks = Mark.objects.filter(mark_board_id__in=mark_boards, student_id=student).values('id')
        return Mark_rel.objects.filter(mark_id__in=marks)

    def resolve_student_mark(self, info, student, schoolyear, part):
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user).id

        mark_boards = Mark_board.objects.filter(schoolyear_id=schoolyear).values('id')
        return Mark.objects.filter(mark_board_id__in=mark_boards, student_id=student, mark_board__subject__part=part)

    def resolve_mark_percentage(self, info, percentage):
      return Mark_percentage.objects.get(percentage=percentage)

    def resolve_markcon_student(self, info, section):
      reports = []

      for student in Student.objects.filter(section_id=section):
        reports.append({
        "student_id":student.pk,
        "family_name":student.family_name,
        "name":student.name,
        "student_code": student.student_code,
        "registerNo": student.registerNo,}) 

      return reports

    def resolve_markcon_subject(self, info, section, schoolyear, part):
      reports = []

      students = Student.objects.filter(section_id=section).values('id')
      mark_boards = Mark.objects.filter(student__in=students).values('mark_board_id')

      if schoolyear == 0:
        subjects = Mark_board.objects.filter(pk__in=mark_boards).values('subject_id')
      else:
        subjects = Mark_board.objects.filter(pk__in=mark_boards, schoolyear_id=schoolyear, subject__part=part).values('subject_id')

      for subject in Subject.objects.filter(pk__in=subjects):
        reports.append({
        "subject_id":subject.pk,
        "subject":subject.subject,
        "subject_code":subject.subject_code,
        "subject_credit": subject.credit,}) 

      return reports

    def resolve_mark_con(self, info, subject, schoolyear, student):
      if schoolyear == 0:
        mark = Mark.objects.get(mark_board__subject_id=subject, student_id=student)
      else:
        try:
          mark = Mark.objects.get(mark_board__subject_id=subject, student_id=student, mark_board__schoolyear_id=schoolyear)
        except:
          return {"percentage":'',"mark_rel":[],"diam":'0'}

      mark_val = Mark_rel.objects.filter(mark__mark_board=mark.mark_board, mark__student_id=student).aggregate(Sum('mark_val')).get('mark_val__sum')

      if mark_val is not None:
        if mark_val > 100:
          mark_val = 100

        if mark_val < 0:
          mark_val = 0

        rels = []

        for rel in Mark_rel.objects.filter(mark__mark_board=mark.mark_board, mark__student_id=student):
            rels.append({
                "mark_val": rel.mark_val, 
                "mark_setting": rel.mark_setting.pass_val
            }) 

        return {"percentage":str(mark_val),"mark_rel":rels,"diam":"percentage_type.diam"}
      else:
         return {"percentage":"","mark_rel":[],"diam":"percentage_type.diam"}

    #   if mark_val > 100:
    #     mark_val = 100

    #   if mark_val < 0:
    #     mark_val = 0

    #   percentage_type = Mark_percentage.objects.get(percentage = mark_val)

    #   return {"percentage":str(mark_val),"type":"percentage_type.type","diam":"percentage_type.diam"}

schema = graphene.Schema(query=Query)