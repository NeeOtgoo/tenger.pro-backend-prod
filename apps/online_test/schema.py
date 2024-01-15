import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from apps.subject.models import Subject
from apps.student.models import Student
from apps.teacher.models import Teacher
from .models import Online_test, Question_level, Question, Question_choice, Take_test, Take_level, Participant, Answer
from graphql_jwt.decorators import login_required, permission_required
from datetime import datetime
from django.db.models import Sum
from graphql import GraphQLError

class Online_testType(DjangoObjectType):
    class Meta:
        model = Online_test
        
class Question_levelType(DjangoObjectType):
    class Meta:
        model = Question_level
        
class QuestionType(DjangoObjectType):
    class Meta:
        model = Question   

class Question_choiceType(DjangoObjectType):
    class Meta:
        model = Question_choice

class Take_testType(DjangoObjectType):
    class Meta:
        model = Take_test

class Take_levelType(DjangoObjectType):
    class Meta:
        model = Take_level

class ParticipantType(DjangoObjectType):
    class Meta:
        model = Participant

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer

class Test_timeType(graphene.ObjectType):
    started = graphene.String()
    duration = graphene.String()
    end_at = graphene.String()

class FinishType(graphene.ObjectType):
    score = graphene.String()

class Query(object):
    all_online_tests = graphene.List(Online_testType)
    all_question_levels = graphene.List(Question_levelType)
    all_questions_by_test = graphene.List(QuestionType, id=graphene.Int(required=True))
    all_choices_by_question = graphene.List(Question_choiceType, id=graphene.Int(required=True))
    all_take_tests = graphene.List(Take_testType)
    single_take_test = graphene.Field(Take_testType, take_test=graphene.Int(required=True))
    start_test = graphene.List(AnswerType, take_test=graphene.Int(required=True))
    finish_test = graphene.Field(FinishType, take_test=graphene.Int(required=True))
    test_time = graphene.Field(Test_timeType, take_test=graphene.Int(required=True))
    all_take_level_by_test = graphene.List(Take_levelType, take_test=graphene.Int(required=True))
    all_participant_by_test = graphene.List(ParticipantType, take_test=graphene.Int(required=True))

    @login_required
    @permission_required('online_test.view_online_test')
    def resolve_all_online_tests(self, info, **kwargs):
        if info.context.user.is_superuser==True:
            return Online_test.objects.all()
            
        if info.context.user.is_student==True:
            return None
        else:
            return Online_test.objects.filter(create_userID=info.context.user)

    @login_required
    @permission_required('online_test.view_question')
    def resolve_all_questions_by_test(self, info, id):
        if info.context.user.is_student==True:
            return None
        else:
            online_test_i = Online_test.objects.get(pk=id)
            return Question.objects.filter(online_test=online_test_i).order_by('pk')

    @login_required
    @permission_required('online_test.view_question_level')
    def resolve_all_question_levels(self, info, **kwargs):
        if info.context.user.is_student==True:
            return None
        else:
            return Question_level.objects.all()

    @login_required
    @permission_required('online_test.view_question_choice')
    def resolve_all_choices_by_question(self, info, id):
        if info.context.user.is_student==True:
            return None
        else:
            question_i = Question.objects.get(pk=id)
            return Question_choice.objects.filter(question=question_i)

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_all_take_tests(self, info, **kwargs):
        if info.context.user.is_superuser==True:
            return Take_test.objects.all()
            
        if info.context.user.is_student==True:
            student=Student.objects.get(user=info.context.user)
            participant=Participant.objects.filter(student=student).values('take_test_id')
            return Take_test.objects.filter(pk__in=participant,status='OPEN')
        else:
            return Take_test.objects.filter(create_userID=info.context.user)

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_single_take_test(self, info, take_test):
        if info.context.user.is_student==True:
            return None
        else:
            return Take_test.objects.get(pk=take_test)

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_start_test(self, info, take_test):
        if info.context.user.is_student==True:
            student=Student.objects.get(user=info.context.user)
                
            if Participant.objects.filter(student=student,take_test=take_test,started__isnull=False,completed__isnull=False).exists():
                return None

            if Participant.objects.filter(student=student,take_test=take_test,started__isnull=True).exists():

                participant = Participant.objects.get(student=student,take_test=take_test)
                participant.started = datetime.now()
                participant.save()

                for take in Take_level.objects.filter(take_test=take_test):

                    for question in Question.objects.order_by('?').filter(online_test=take.online_test, question_level=take.question_level)[:take.take_number]:

                        choices=""
                        for choice in Question_choice.objects.filter(question=question):
                            choices += str(choice.pk)+":|"+choice.answer+",|"
                        answer = Answer(participant=participant, question=question, question_text=question.question, choices=choices,answer_type=question.answer_type)
                        answer.save()

            return Answer.objects.filter(participant__take_test=take_test).order_by("pk")
        else:
            return None

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_finish_test(self, info, take_test):
        if info.context.user.is_student==True:
            student=Student.objects.get(user=info.context.user)
                
            if Participant.objects.filter(student=student,take_test=take_test,started__isnull=False,completed__isnull=False).exists():
                
                participant = Participant.objects.get(student=student,take_test=take_test)
                answer_score = Answer.objects.filter(participant=participant).aggregate(sum=Sum('score'))['sum']
            
                return {"score":answer_score}

            if Participant.objects.filter(student=student,take_test=take_test,started__isnull=False,completed__isnull=True).exists():

                participant = Participant.objects.get(student=student,take_test=take_test)
                participant.completed = datetime.now()
                participant.save()

                answer_score = Answer.objects.filter(participant=participant).aggregate(sum=Sum('score'))['sum']
            
            return {"score":answer_score}
        else:
            return None

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_test_time(self, info, take_test):
        if info.context.user.is_student==True:
        
            student=Student.objects.get(user=info.context.user)

            participant = Participant.objects.filter(student=student,take_test=take_test).first()

            take_test = Take_test.objects.filter(pk=take_test).first()
    
            return {"started":participant.started,"duration":take_test.duration,"end_at":take_test.end_at}
        else:
            return None
      
    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_all_take_level_by_test(self, info, take_test):
        if info.context.user.is_student==True:
            return None
        else:
            return Take_level.objects.filter(take_test_id=take_test)

    @login_required
    @permission_required('online_test.view_take_test')
    def resolve_all_participant_by_test(self, info, take_test):
        if info.context.user.is_student==True:
            return None
        else:
            return Participant.objects.filter(take_test_id=take_test)

#******************* 😎 Online_test-MUTATIONS 😎 *************************#
class CreateOnline_test(graphene.Mutation):
    online_test = graphene.Field(Online_testType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        subject = graphene.Int()

    @login_required
    @permission_required('online_test.add_online_test')
    def mutate(self, info, title, description, subject):
        
        create_userID_i = info.context.user

        subject_o = Subject(pk=subject)

        online_test = Online_test(title=title, description=description, subject=subject_o, create_userID=create_userID_i)
        online_test.save()
        return CreateOnline_test(online_test=online_test)

class UpdateOnline_test(graphene.Mutation):
    Online_test = graphene.Field(Online_testType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        subject = graphene.Int()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_online_test')
    def mutate(self, info, title, description, subject, id):

        online_test = Online_test.objects.get(pk=id)
        subject_o = Subject(pk=subject)

        online_test.title = title
        online_test.description = description
        online_test.subject = subject_o
        online_test.save()
        return UpdateOnline_test(online_test=online_test)
        
class DeleteOnline_test(graphene.Mutation):
    online_test = graphene.Field(Online_testType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_online_test')
    def mutate(self, info, **kwargs):
        online_test = Online_test.objects.get(pk=kwargs["id"])
        if online_test is not None:
            online_test.delete()
        return DeleteOnline_test(online_test=online_test)

#******************* 😎 Question_level-MUTATIONS 😎 *************************#
class CreateQuestion_level(graphene.Mutation):
    question_level = graphene.Field(Question_levelType)

    class Arguments:
        level = graphene.String()

    @login_required
    @permission_required('online_test.add_question_level')
    def mutate(self, info, level):

        question_level_o = Question_level(level=level)
        question_level_o.save()
        return CreateQuestion_level(question_level=question_level_o)

class UpdateQuestion_level(graphene.Mutation):
    question_level = graphene.Field(Question_levelType)

    class Arguments:
        level = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_question_level')
    def mutate(self, info, level, id):

        question_level_o = Question_level.objects.get(pk=id)

        question_level_o.level = level
        question_level_o.save()
        return UpdateQuestion_level(question_level=question_level_o)
        
class DeleteQuestion_level(graphene.Mutation):
    question_level = graphene.Field(Question_levelType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_question_level')
    def mutate(self, info, **kwargs):
        question_level = Question_level.objects.get(pk=kwargs["id"])
        if question_level is not None:
            question_level.delete()
        return DeleteQuestion_level(question_level=question_level)

#******************* 😎 Question-MUTATIONS 😎 *************************#
class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        online_test =  graphene.Int()
        question_level =  graphene.Int()
        question_l =  graphene.String()
        hint =  graphene.String()
        image = Upload()
        answer_type =  graphene.String()

    @login_required
    @permission_required('online_test.add_question')
    def mutate(self, info, online_test, question_level, question_l, hint, image, answer_type):
        
        online_test_i = Online_test.objects.get(pk=online_test)

        question_o = Question(online_test=online_test_i, question=question_l, hint=hint, image=image, answer_type=answer_type)
        question_o.save()
        try:
            question_level_i = Question_level.objects.get(pk=question_level)
            question_o.question_level = question_level_i
            question_o.save()
            return CreateQuestion(question=question_o)
        except Question_level.DoesNotExist:
            return CreateQuestion(question=question_o)
        

class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        online_test =  graphene.Int()
        question_level =  graphene.Int()
        question_l =  graphene.String()
        hint =  graphene.String()
        image = Upload()
        answer_type =  graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_question')
    def mutate(self, info, online_test, question_level, question_l, hint, image, answer_type, id):

        question_o = Question.objects.get(pk=id)
        online_test_i = Online_test.objects.get(pk=online_test)
        question_level_i = Question_level.objects.get(pk=question_level)

        question_o.online_test = online_test_i
        question_o.question_level = question_level_i
        question_o.question = question_l
        question_o.hint = hint
        if image != '':
            question_o.image = image
        question_o.answer_type = answer_type
        question_o.save()
        return UpdateQuestion(question=question_o)
        
class DeleteQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_Question')
    def mutate(self, info, **kwargs):
        question = Question.objects.get(pk=kwargs["id"])
        if question is not None:
            question.delete()
        return DeleteQuestion(question=question)

#******************* 😎 Question_choice-MUTATIONS 😎 *************************#
class CreateQuestion_choice(graphene.Mutation):
    question_choice = graphene.Field(Question_choiceType)

    class Arguments:
        question = graphene.Int()
        answer = graphene.String()
        score = graphene.Decimal()

    @login_required
    @permission_required('online_test.add_question_choice')
    def mutate(self, info, question, answer, score):
        
        question_i = Question.objects.get(pk=question)

        question_choice = Question_choice(question=question_i, answer=answer, score=score)
        question_choice.save()
        return CreateQuestion_choice(question_choice=question_choice)

class UpdateQuestion_choice(graphene.Mutation):
    question_choice = graphene.Field(Question_choiceType)

    class Arguments:
        question = graphene.Int()
        answer = graphene.String()
        score = graphene.Decimal()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_question_choice')
    def mutate(self, info, question, answer, score, id):

        question_choice = Question_choice.objects.get(pk=id)
        question_i = Question.objects.get(pk=question)

        question_choice.question = question_i
        question_choice.answer = answer
        question_choice.score = score
        question_choice.save()
        return UpdateQuestion_choice(question_choice=question_choice)
        
class DeleteQuestion_choice(graphene.Mutation):
    question_choice = graphene.Field(Question_choiceType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_question_choice')
    def mutate(self, info, **kwargs):
        question_choice = Question_choice.objects.get(pk=kwargs["id"])
        if question_choice is not None:
            question_choice.delete()
        return DeleteQuestion_choice(question_choice=question_choice)

#******************* 😎 Take_test-MUTATIONS 😎 *************************#
class CreateTake_test(graphene.Mutation):
    take_test = graphene.Field(Take_testType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        start_at = graphene.String()
        end_at = graphene.String()
        duration = graphene.Int()
        status = graphene.String()

    @login_required
    @permission_required('online_test.add_take_test')
    def mutate(self, info, title, description, start_at, end_at, duration, status):
        
        create_userID_i = info.context.user

        take_test = Take_test(title=title, description=description, start_at=start_at, end_at=end_at, duration=duration, status=status, create_userID=create_userID_i)
        take_test.save()
        return CreateTake_test(take_test=take_test)

class UpdateTake_test(graphene.Mutation):
    take_test = graphene.Field(Take_testType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        start_at = graphene.String()
        end_at = graphene.String()
        duration = graphene.Int()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_take_test')
    def mutate(self, info, title, description, start_at, end_at, duration, status, id):

        take_test_o = Take_test.objects.get(pk=id)

        take_test_o.title = title
        take_test_o.description = description
        take_test_o.start_at = start_at
        take_test_o.end_at = end_at
        take_test_o.duration = duration
        take_test_o.status = status
        take_test_o.save()
        return UpdateTake_test(take_test=take_test_o)
        
class DeleteTake_test(graphene.Mutation):
    take_test = graphene.Field(Take_testType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_take_test')
    def mutate(self, info, **kwargs):
        take_test = Take_test.objects.get(pk=kwargs["id"])
        if take_test is not None:
            take_test.delete()
        return DeleteTake_test(take_test=take_test)

#******************* 😎 Take_level-MUTATIONS 😎 *************************#
class CreateTake_level(graphene.Mutation):
    take_level = graphene.Field(Take_levelType)

    class Arguments:
        take_test = graphene.Int()
        online_test = graphene.Int()
        question_level = graphene.Int()
        take_number = graphene.Int()

    @login_required
    @permission_required('online_test.add_take_level')
    def mutate(self, info, take_test, online_test, question_level, take_number):
        
        take_test_i = Take_test.objects.get(pk=take_test)
        online_test_i = Online_test.objects.get(pk=online_test)
        question_level_i = Question_level.objects.get(pk=question_level)

        take_level = Take_level(take_test=take_test_i, online_test=online_test_i, question_level=question_level_i, take_number=take_number)
        take_level.save()
        return CreateTake_level(take_level=take_level)
        
class DeleteTake_level(graphene.Mutation):
    take_level = graphene.Field(Take_levelType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('online_test.delete_take_level')
    def mutate(self, info, **kwargs):
        take_level = Take_level.objects.get(pk=kwargs["id"])
        if take_level is not None:
            take_level.delete()
        return DeleteTake_level(take_level=take_level)

#******************* 😎 Participant-MUTATIONS 😎 *************************#
class CreateParticipant(graphene.Mutation):
    participant = graphene.Field(ParticipantType)

    class Arguments:
        student_code = graphene.String()
        section = graphene.Int()
        take_test = graphene.Int()

    @login_required
    @permission_required('online_test.add_participant')
    def mutate(self, info, student_code, section, take_test):

        if(student_code==''):
            for student in Student.objects.filter(section_id=section):
                participant_o = Participant.objects.get_or_create(
                    student=student,
                    take_test_id=take_test
                )[0]
        else:
            student_i = Student.objects.get(student_code=student_code)
            participant_o = Participant.objects.get_or_create(
                student=student_i,
                take_test_id=take_test
            )[0]
        return CreateParticipant(participant=participant_o)
        
class DeleteParticipant(graphene.Mutation):
    participant = graphene.Field(ParticipantType)
    class Arguments:
        id = graphene.ID()
        take_test = graphene.Int()

    @login_required
    @permission_required('online_test.delete_participant')
    def mutate(self, info, **kwargs):
        try:
            if(kwargs["take_test"]==0):
                participant = Participant.objects.get(pk=kwargs["id"])
                if participant is not None:
                    participant.delete()
            else:
                participant = Participant.objects.filter(take_test_id=kwargs["take_test"]).delete()
            return True
        except:
            return None

#******************* 😎 Answer-MUTATIONS 😎 *************************#
class UpdateAnswer(graphene.Mutation):
    answer = graphene.Field(AnswerType)

    class Arguments:
        given_answer = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('online_test.change_answer')
    def mutate(self, info, given_answer, id):

        answer_o = Answer.objects.get(pk=id)

        if(answer_o.answer_type=='TEXT'):
            answer_o.given_answer = given_answer
            answer_o.score = 0
            answer_o.save()
        elif(answer_o.answer_type=='MULTIPLE'):
            score = 0
            given_answer_i = ""

            for q in given_answer.split(","):
                question_choice_i = Question_choice.objects.get(pk=q)
                score += question_choice_i.score
                given_answer_i += question_choice_i.answer+",|"

            answer_o.given_answer = given_answer_i
            answer_o.score = score
            answer_o.save()
        elif(answer_o.answer_type=='CHOOSE'):
            question_choice_i = Question_choice.objects.get(pk=given_answer)
            answer_o.given_answer = question_choice_i.answer
            answer_o.score = question_choice_i.score
            answer_o.save()

        return UpdateAnswer(answer=answer_o)

class Mutation(graphene.ObjectType):
    create_online_test = CreateOnline_test.Field()
    update_online_test = UpdateOnline_test.Field()
    delete_online_test = DeleteOnline_test.Field()
    create_question_level = CreateQuestion_level.Field()
    update_question_level = UpdateQuestion_level.Field()
    delete_question_level = DeleteQuestion_level.Field()
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()
    create_question_choice = CreateQuestion_choice.Field()
    update_question_choice = UpdateQuestion_choice.Field()
    delete_question_choice = DeleteQuestion_choice.Field()
    create_take_test = CreateTake_test.Field()
    update_take_test = UpdateTake_test.Field()
    delete_take_test = DeleteTake_test.Field()
    create_take_level = CreateTake_level.Field()
    delete_take_level = DeleteTake_level.Field()
    create_participant = CreateParticipant.Field()
    delete_participant = DeleteParticipant.Field()
    update_answer = UpdateAnswer.Field()