from email.policy import default
import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import Online_file_folder, Online_lesson, Online_attendance, Online_student, Online_file, Online_sub_file, Online_type, Online_sub
from apps.subject.models import Subject
from apps.student.models import Student
from apps.schoolyear.models import Schoolyear
from graphql_jwt.decorators import login_required, permission_required
from django.db.models import Q

class Online_file_folderType(DjangoObjectType):
    class Meta:
        model = Online_file_folder

class Online_lessonType(DjangoObjectType):
    class Meta:
        model = Online_lesson

class Online_studentType(DjangoObjectType):
    class Meta:
        model = Online_student

class Online_fileType(DjangoObjectType):
    class Meta:
        model = Online_file

class Online_typeType(DjangoObjectType):
    class Meta:
        model = Online_type

class Online_subType(DjangoObjectType):
    class Meta:
        model = Online_sub

class Online_attendanceType(DjangoObjectType):
    class Meta:
        model = Online_attendance

class Online_sub_fileType(DjangoObjectType):
    class Meta:
        model = Online_sub_file

class Query(object):
    all_online_lessons = graphene.List(Online_lessonType, offset=graphene.Int(required=False, default_value=0), limit=graphene.Int(required=False, default_value=50), filter=graphene.String(required=False, default_value=''))
    all_online_student_by_lesson = graphene.List(Online_studentType, online_lesson=graphene.Int(required=True))
    all_online_types = graphene.List(Online_typeType)
    online_lesson_by_id = graphene.Field(Online_lessonType, id=graphene.Int(required=True))
    all_online_sub_by_lesson = graphene.List(Online_subType, online_lesson=graphene.Int(required=True))
    online_sub_by_id = graphene.Field(Online_subType, id=graphene.Int(required=True))
    online_attendance_by_sub = graphene.List(Online_subType, online_sub=graphene.Int(required=True))
    all_folders = graphene.List(Online_file_folderType, folder=graphene.Int(required=False, default_value=0))
    all_online_files = graphene.List(Online_fileType, folder=graphene.Int(required=False, default_value=0))
    all_online_sub_files = graphene.List(Online_sub_fileType, online_sub=graphene.Int())

    @login_required
    @permission_required('online_lesson.view_online_sub_file')
    def resolve_all_online_sub_files(self, info, online_sub):
        online_sub_o = Online_sub.objects.get(pk=online_sub)
        return Online_sub_file.objects.filter(online_sub=online_sub_o)

    @login_required
    @permission_required('online_lesson.view_online_lesson')
    def resolve_all_online_lessons(self, info, offset, limit, filter):

        fields = Online_lesson.filter_fields()

        Qr = None
        for field in fields:
            q = Q(**{"%s__icontains" % field: filter })
            if Qr:
                Qr = Qr | q
            else:
                Qr = q


        if info.context.user.is_teacher==True:
            return Online_lesson.objects.filter(Q(create_userID=info.context.user), Qr)[offset:limit]
        if info.context.user.is_student==True:
            student = Student.objects.get(user=info.context.user)
            online_student = Online_student.objects.filter(student=student).values ('online_lesson')
            return Online_lesson.objects.filter(Q(pk__in=online_student), Qr)[offset:limit]
        else:
            return Online_lesson.objects.filter(Qr)[offset:limit]

    @login_required
    @permission_required('online_lesson.view_online_student')
    def resolve_all_online_student_by_lesson(self, info, online_lesson):
        return Online_student.objects.filter(online_lesson_id=online_lesson)

    @login_required
    @permission_required('online_lesson.view_online_type')
    def resolve_all_online_types(self, info, **kwargs):
        return Online_type.objects.all()
        
    @login_required
    @permission_required('online_lesson.view_online_file_folder')
    def resolve_all_folders(self, info, folder):
        if folder==0:
            return Online_file_folder.objects.filter(Q(create_userID=info.context.user), Q(sub_folder__isnull=True))
        else:
            return Online_file_folder.objects.filter(Q(create_userID=info.context.user), Q(sub_folder_id=folder))
        
    @login_required
    @permission_required('online_lesson.view_online_file')
    def resolve_all_online_files(self, info, folder):
        if folder==0:
            return Online_file.objects.filter(Q(create_userID=info.context.user), Q(folder__isnull=True))
        else:
            return Online_file.objects.filter(Q(create_userID=info.context.user), Q(folder_id=folder))

    @login_required
    @permission_required('online_lesson.view_online_lesson')
    def resolve_online_lesson_by_id(root, info, id):
        try:
            return Online_lesson.objects.get(pk=id)
        except Online_lesson.DoesNotExist:
            return None

    @login_required
    @permission_required('online_lesson.view_online_sub')
    def resolve_all_online_sub_by_lesson(root, info, online_lesson):
        try:
            if info.context.user.is_student==False:
                return Online_sub.objects.filter(online_lesson=online_lesson)
            else:
                return Online_sub.objects.filter(online_lesson=online_lesson, status='OPEN')
        except Online_sub.DoesNotExist:
            return None
            
    @login_required
    @permission_required('online_lesson.view_online_sub')
    def resolve_online_sub_by_id(root, info, id):
        try:
            if info.context.user.is_student==False:
                return Online_sub.objects.get(pk=id)
            else:
                online_sub_i = Online_sub.objects.get(pk=id, status='OPEN')
                student = Student.objects.get(user=info.context.user)

                online_attendance = Online_attendance(online_sub=online_sub_i, student=student)
                online_attendance.save()
                
                return online_sub_i
        except Online_sub.DoesNotExist:
            return None
      
    @login_required
    @permission_required('online_lesson.view_online_attendance')
    def resolve_online_attendance_by_sub(root, info, online_sub):
        try:
            online_sub_i = Online_sub.objects.get(pk=online_sub)
            if info.context.user.is_student==False:
                return Online_attendance.objects.filter(online_sub=online_sub_i)
            else:
                student = Student.objects.get(user=info.context.user)
                return Online_attendance.objects.filter(online_sub=online_sub_i,student=student)
        except Online_attendance.DoesNotExist:
            return None

#******************* 😎 Online_lesson-MUTATIONS 😎 *************************#
class CreateOnline_lesson(graphene.Mutation):
    online_lesson = graphene.Field(Online_lessonType)

    class Arguments:
        schoolyear = graphene.Int()
        subject = graphene.Int()
        description = graphene.String()
        content = graphene.String()
        status = graphene.String()

    @login_required
    @permission_required('online_lesson.add_online_lesson')
    def mutate(self, info, schoolyear, subject, description, content, status):
        
        schoolyear_i = Schoolyear.objects.get(pk=schoolyear)
        subject_i = Subject.objects.get(pk=subject)
        create_userID_i = info.context.user

        online_lesson = Online_lesson(schoolyear=schoolyear_i, subject=subject_i, description=description, content=content, status=status, create_userID=create_userID_i)
        online_lesson.save()
        return CreateOnline_lesson(online_lesson=online_lesson)

class UpdateOnline_lesson(graphene.Mutation):
    online_lesson = graphene.Field(Online_lessonType)

    class Arguments:
        schoolyear = graphene.Int()
        subject = graphene.Int()
        description = graphene.String()
        content = graphene.String()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.change_online_lesson')
    def mutate(self, info, schoolyear, subject, description, content, status, id):
        
        online_lesson = Online_lesson.objects.get(pk=id)
        schoolyear_i = Schoolyear.objects.get(pk=schoolyear)
        subject_i = Subject.objects.get(pk=subject)

        online_lesson.schoolyear = schoolyear_i
        online_lesson.subject = subject_i
        online_lesson.description = description
        online_lesson.content = content
        online_lesson.status = status
        online_lesson.save()
        return UpdateOnline_lesson(online_lesson=online_lesson)
        
class DeleteOnline_lesson(graphene.Mutation):
    online_lesson = graphene.Field(Online_lessonType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_lesson')
    def mutate(self, info, **kwargs):
        online_lesson = Online_lesson.objects.get(pk=kwargs["id"])
        if online_lesson is not None:
            online_lesson.delete()
        return DeleteOnline_lesson(online_lesson=online_lesson)

#******************* 😎 Online_sub-MUTATIONS 😎 *************************#
class CreateOnline_sub(graphene.Mutation):
    online_sub = graphene.Field(Online_subType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        content = graphene.String()
        online_lesson = graphene.Int()
        online_type = graphene.Int()
        status = graphene.String()

    @login_required
    @permission_required('online_lesson.add_online_sub')
    def mutate(self, info, title, description, content, online_lesson, online_type, status):
        
        online_lesson_i = Online_lesson.objects.get(pk=online_lesson)
        online_type_i = Online_type.objects.get(pk=online_type)
        create_userID_i = info.context.user

        online_sub = Online_sub(title=title, description=description, content=content, status=status, online_lesson=online_lesson_i, online_type = online_type_i,create_userID=create_userID_i)
        online_sub.save()
        return CreateOnline_sub(online_sub=online_sub)

class UpdateOnline_sub(graphene.Mutation):
    online_sub = graphene.Field(Online_subType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        content = graphene.String()
        online_lesson = graphene.Int()
        online_type = graphene.Int()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.change_online_sub')
    def mutate(self, info, title, description, content, online_lesson, online_type, status, id):
        
        online_sub = Online_sub.objects.get(pk=id)
        online_lesson_i = Online_lesson.objects.get(pk=online_lesson)
        online_type_i = Online_type.objects.get(pk=online_type)

        online_sub.title = title
        online_sub.description = description
        online_sub.content = content
        online_sub.status = status
        online_sub.online_lesson = online_lesson_i
        online_sub.online_type = online_type_i
        online_sub.save()
        return UpdateOnline_sub(online_sub=online_sub)
        
class DeleteOnline_sub(graphene.Mutation):
    online_sub = graphene.Field(Online_subType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_sub')
    def mutate(self, info, id):
        online_sub_o = Online_sub.objects.get(pk=id)
        online_sub_o.delete()
        return DeleteOnline_lesson(online_sub_o)

#******************* 😎 Online_student-MUTATIONS 😎 *************************#
class CreateOnline_student(graphene.Mutation):
    online_student = graphene.Field(Online_studentType)

    class Arguments:
        online_lesson = graphene.Int()
        student_code = graphene.String()
        section = graphene.Int()

    @login_required
    @permission_required('online_lesson.add_online_student')
    def mutate(self, info, online_lesson, student_code, section):

        if(student_code==''):
            for student in Student.objects.filter(section_id=section):
                online_student_o = Online_student(student=student, online_lesson_id=online_lesson)
                online_student_o.save()
        else:
            student_i = Student.objects.get(student_code=student_code)
            online_student_o = Online_student(online_lesson_id=online_lesson, student=student_i)
            online_student_o.save()
        
        return CreateOnline_student(online_student=online_student_o)
        
class DeleteOnline_student(graphene.Mutation):
    online_student = graphene.Field(Online_studentType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_student')
    def mutate(self, info, **kwargs):
        online_student = Online_student.objects.get(pk=kwargs["id"])
        if online_student is not None:
            online_student.delete()
        return DeleteOnline_student(online_student=online_student)

#******************* 😎 Online_file-MUTATIONS 😎 *************************#
class CreateOnline_file(graphene.Mutation):
    online_file = graphene.Field(Online_fileType)

    class Arguments:
        file = Upload(required=True)
        folder = graphene.Int()

    # @login_required
    # @permission_required('online_lesson.add_online_file')
    def mutate(self, info, file, folder):
        
        create_userID_i = info.context.user
        
        if folder == 0:
            online_file = Online_file(file=file, create_userID=create_userID_i)
        else:
            folder_o = Online_file_folder.objects.get(pk=folder)
            online_file = Online_file(file=file, folder=folder_o, create_userID=create_userID_i)
        online_file.save()
        return CreateOnline_file(online_file=online_file)
        
class DeleteOnline_file(graphene.Mutation):
    online_file = graphene.Field(Online_fileType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_file')
    def mutate(self, info, **kwargs):
        online_file = Online_file.objects.get(pk=kwargs["id"])
        if online_file is not None:
            online_file.delete()
        return DeleteOnline_file(online_file=online_file)

#******************* 😎 Online_type-MUTATIONS 😎 *************************#
class CreateOnline_type(graphene.Mutation):
    online_type = graphene.Field(Online_typeType)

    class Arguments:
        name = graphene.String(required=True)

    @login_required
    @permission_required('online_lesson.add_online_type')
    def mutate(self, info, name):
        
        online_type = Online_type(name=name)
        online_type.save()
        return CreateOnline_type(online_type=online_type)

class UpdateOnline_type(graphene.Mutation):
    online_type = graphene.Field(Online_typeType)

    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.change_online_type')
    def mutate(self, info, name, id):
        
        online_type_o = Online_type.objects.get(pk=id)

        online_type_o.tinametle = name
        online_type_o.save()
        return UpdateOnline_type(online_type=online_type_o)
        
class DeleteOnline_type(graphene.Mutation):
    online_type = graphene.Field(Online_typeType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_type')
    def mutate(self, info, **kwargs):
        online_type = Online_type.objects.get(pk=kwargs["id"])
        if online_type is not None:
            online_type.delete()
        return DeleteOnline_type(online_type=online_type)

#******************* 😎 Online_attendance-MUTATIONS 😎 *************************#
class DeleteOnline_attendance(graphene.Mutation):
    online_attendance = graphene.Field(Online_attendanceType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_lesson.delete_online_attendance')
    def mutate(self, info, **kwargs):
        online_attendance = Online_attendance.objects.get(pk=kwargs["id"])
        if online_attendance is not None:
            online_attendance.delete()
        return DeleteOnline_attendance(online_attendance=online_attendance)

class CreateOnline_file_folder(graphene.Mutation):
    online_file_folder = graphene.Field(Online_file_folderType)
    class Arguments:
        name = graphene.String()
        sub_folder = graphene.Int(default_value=0)
    
    @login_required
    @permission_required('online_lesson.add_online_file_folder')
    def mutate(self, info, name, sub_folder):
        create_userID_i = info.context.user
        if sub_folder == 0:
            online_file_folder = Online_file_folder(name=name, create_userID=create_userID_i)
        else:
            sub_folder = Online_file_folder.objects.get(pk=sub_folder)
            online_file_folder = Online_file_folder(name=name, sub_folder=sub_folder, create_userID=create_userID_i)
        online_file_folder.save()
        return CreateOnline_file_folder(online_file_folder=online_file_folder)

class DeleteOnline_file_folder(graphene.Mutation):
    online_file_folder = graphene.Field(Online_file_folderType)
    class Arguments:
        id = graphene.Int()

    @login_required
    @permission_required('online_lesson.delete_online_file_folder')
    def mutate(self, info, id):
        online_file_folder = Online_file_folder.objects.get(pk=id)
        online_file_folder.delete()
        return DeleteOnline_file_folder(online_file_folder=online_file_folder)

class CreateOnline_sub_file(graphene.Mutation):
    online_sub_file = graphene.Field(Online_sub_fileType)
    class Arguments:
        online_sub = graphene.Int()
        online_file = graphene.Int()

    @login_required
    @permission_required('online_lesson.view_online_sub_file')
    def mutate(self, info, online_sub, online_file):
        online_sub_o = Online_sub.objects.get(pk=online_sub)
        online_file_o = Online_file.objects.get(pk=online_file)

        online_sub_file = Online_sub_file(online_sub=online_sub_o, online_file=online_file_o)
        online_sub_file.save()
        return CreateOnline_sub_file(online_sub_file=online_sub_file)

class DeleteOnline_sub_file(graphene.Mutation):
    online_sub_file = graphene.Field(Online_sub_fileType)
    class Arguments:
        id = graphene.Int()

    @login_required
    @permission_required('online_lesson.delete_online_sub_file')
    def mutate(self, info, id):
        online_sub_file = Online_sub_file.objects.get(pk=id)
        if online_sub_file is not None:
            online_sub_file.delete()
        return DeleteOnline_sub_file(online_sub_file=online_sub_file)

class Mutation(graphene.ObjectType):
    create_online_lesson = CreateOnline_lesson.Field()
    update_online_lesson = UpdateOnline_lesson.Field()
    delete_online_lesson = DeleteOnline_lesson.Field()
    create_online_sub = CreateOnline_sub.Field()
    update_online_sub = UpdateOnline_sub.Field()
    delete_online_sub = DeleteOnline_sub.Field()
    create_online_student = CreateOnline_student.Field()
    delete_online_student = DeleteOnline_student.Field()
    create_online_file = CreateOnline_file.Field()
    delete_online_file = DeleteOnline_file.Field()
    create_online_type = CreateOnline_type.Field()
    update_online_type = UpdateOnline_type.Field()
    delete_online_type = DeleteOnline_type.Field()
    delete_online_attendance = DeleteOnline_attendance.Field()
    create_online_file_folder = CreateOnline_file_folder.Field()
    delete_online_file_folder = DeleteOnline_file_folder.Field()
    create_online_sub_file = CreateOnline_sub_file.Field()
    delete_online_sub_file = DeleteOnline_sub_file.Field()