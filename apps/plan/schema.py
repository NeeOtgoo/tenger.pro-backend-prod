import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required
from .models import Plan, PlanAction, PlanMark
from apps.teacher.models import Teacher
from apps.subject.models import Subject
from apps.section.models import Section
from apps.schoolyear.models import Schoolyear
from apps.employee.models import Employee

class PlanType(DjangoObjectType):
    class Meta:
        model = Plan

class PlanActionType(DjangoObjectType):
    class Meta:
        model = PlanAction

class PlanMarkType(DjangoObjectType):
    class Meta:
        model = PlanMark

class Query(object):
    all_plan_marks = graphene.List(PlanMarkType)
    all_plans = graphene.List(PlanType)
    plan_by_id = graphene.Field(PlanType, id=graphene.ID(required=True))
    all_plan_actions_by_plan = graphene.List(PlanActionType, plan=graphene.ID(required=True))

    def resolve_all_plan_marks(self, info):
        return PlanMark.objects.all()

    def resolve_all_plans(self, info):
        if info.context.user.is_teacher == True:
            teacher_o = Teacher.objects.get(user=info.context.user)
            return Plan.objects.filter(teacher=teacher_o)
        else:
            return Plan.objects.all()

    def resolve_plan_by_id(self, info, id):
        return Plan.objects.get(pk=id)

    def resolve_all_plan_actions_by_plan(self, info, plan):
        plan_o = Plan.objects.get(pk=plan)
        return PlanAction.objects.filter(plan=plan_o).order_by('pk') 

class CreatePlanMark(graphene.Mutation):
    plan_mark = graphene.Field(PlanMarkType)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):

        plan_mark_o = PlanMark(name=name)
        plan_mark_o.save()
        return CreatePlanMark(plan_mark=plan_mark_o)

class UpdatePlanMark(graphene.Mutation):
    plan_mark = graphene.Field(PlanMarkType)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    def mutate(self, info, id, name):

        plan_mark_o = PlanMark.objects.get(pk=id)

        plan_mark_o.name = name
        plan_mark_o.save()
        return UpdatePlanMark(plan_mark=plan_mark_o)

class DeletePlanMark(graphene.Mutation):
    plan_mark = graphene.Field(PlanMarkType)

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):

        plan_mark_o = PlanMark.objects.get(pk=id)
        if plan_mark_o is not None:
            plan_mark_o.delete()
        return DeletePlanMark(plan_mark=plan_mark_o)

class CreatePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        subject = graphene.ID()
        section = graphene.ID()
        schoolyear = graphene.ID()
        topic = graphene.String()
        subject_topic = graphene.String()
        intention = graphene.String()
        keyword = graphene.String()
        consumables = graphene.String()
        title = graphene.String()
        duration = graphene.Int()

    def mutate(self, info, subject, section, schoolyear, topic, subject_topic, intention, keyword, consumables, title, duration):

        teacher_o = Teacher.objects.get(user=info.context.user)
        subject_o = Subject.objects.get(pk=subject)
        section_o = Section.objects.get(pk=section)
        schoolyear_o = Schoolyear.objects.get(pk=schoolyear)

        plan_o = Plan(
            teacher=teacher_o, 
            subject=subject_o,
            section=section_o,
            schoolyear=schoolyear_o,
            topic=topic,
            subject_topic=subject_topic,
            intention=intention,
            keyword=keyword,
            consumables=consumables,
            title=title,
            duration=duration
        )
        plan_o.save()

        return CreatePlan(plan=plan_o)

class ApprovePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments: 
        plan = graphene.ID()

    def mutate(self, info, plan):

        plan_o = Plan.objects.get(pk=plan)
        employee_o = Employee.objects.get(user=info.context.user)
        plan_o.approved_by = employee_o
        plan_o.save()

        return ApprovePlan(plan=plan_o)
        

class UpdatePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        id = graphene.ID()
        subject = graphene.ID()
        section = graphene.ID()
        schoolyear = graphene.ID()
        topic = graphene.String()
        subject_topic = graphene.String()
        intention = graphene.String()
        keyword = graphene.String()
        consumables = graphene.String()
        title = graphene.String()
        duration = graphene.Int()
    
    def mutate(self, info, id, subject, section, schoolyear, topic, subject_topic, intention, keyword, consumables, title, duration):

        subject_o = Subject.objects.get(pk=subject)
        section_o = Section.objects.get(pk=section)
        schoolyear_o = Schoolyear.objects.get(pk=schoolyear)
        plan_o = Plan.objects.get(pk=id)

        plan_o.subject=subject_o
        plan_o.section=section_o
        plan_o.schoolyear=schoolyear_o
        plan_o.topic=topic
        plan_o.subject_topic=subject_topic
        plan_o.intention=intention
        plan_o.keyword=keyword
        plan_o.consumables=consumables
        plan_o.duration=duration
        plan_o.title=title
        plan_o.save()

        return CreatePlan(plan=plan_o)

class DeletePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments: 
        id = graphene.ID()

    def mutate(self, info, id):

        plan_o = Plan.objects.get(pk=id)
        plan_o.delete()

        return DeletePlan(plan=plan_o)

class CreatePlanAction(graphene.Mutation):
    plan_action = graphene.Field(PlanActionType)

    class Arguments:
        plan = graphene.ID()
        plan_mark = graphene.String()
        name = graphene.String()
        teaching_method = graphene.String()
        teacher_activity = graphene.String()
        student_activity = graphene.String()
        student_assignment = graphene.String()
        duration = graphene.Int()

    def mutate(self, info, plan, plan_mark, name, teaching_method, teacher_activity, student_activity, student_assignment, duration):

        plan_o = Plan.objects.get(pk=plan)
        
        plan_action_o = PlanAction(
            plan=plan_o, 
            plan_mark=plan_mark, 
            name=name, 
            teaching_method=teaching_method, 
            teacher_activity=teacher_activity, 
            student_activity=student_activity, 
            student_assignment=student_assignment, 
            duration=duration
        )
        plan_action_o.save()

        return CreatePlanAction(plan_action=plan_action_o)

class UpdatePlanAction(graphene.Mutation):
    plan_action = graphene.Field(PlanActionType)

    class Arguments:
        id = graphene.ID()
        plan = graphene.ID()
        plan_mark = graphene.String()
        name = graphene.String()
        teaching_method = graphene.String()
        teacher_activity = graphene.String()
        student_activity = graphene.String()
        student_assignment = graphene.String()
        duration = graphene.Int()

    def mutate(self, info, id, plan, plan_mark, name, teaching_method, teacher_activity, student_activity, student_assignment, duration):

        plan_o = Plan.objects.get(pk=plan)
        plan_action_o = PlanAction.objects.get(pk=id)
        
        plan_action_o.plan=plan_o
        plan_action_o.plan_mark=plan_mark
        plan_action_o.name=name
        plan_action_o.teaching_method=teaching_method
        plan_action_o.teacher_activity=teacher_activity
        plan_action_o.student_activity=student_activity
        plan_action_o.student_assignment=student_assignment
        plan_action_o.duration=duration
        plan_action_o.save()

        return UpdatePlanAction(plan_action=plan_action_o)

class DeletePlanAction(graphene.Mutation):
    plan_action = graphene.Field(PlanActionType)

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):

        plan_action_o = PlanAction.objects.get(pk=id)
        plan_action_o.delete()

        return DeletePlanAction(plan_action=plan_action_o)

class Mutation(graphene.ObjectType):
    create_plan_mark = CreatePlanMark.Field()
    update_plan_mark = UpdatePlanMark.Field()
    delete_plan_mark = DeletePlanMark.Field()
    create_plan = CreatePlan.Field()
    update_plan = UpdatePlan.Field()
    delete_plan = DeletePlan.Field()
    create_plan_action = CreatePlanAction.Field()
    update_plan_action = UpdatePlanAction.Field()
    delete_plan_action = DeletePlanAction.Field()
    approve_plan = ApprovePlan.Field()