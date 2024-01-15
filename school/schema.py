import graphene
import account.schema
import apps.classes.schema
import apps.core.schema
import apps.event.schema
# import apps.library.schema
import apps.live.schema
import apps.mark.schema
import apps.menu.schema
import apps.online_lesson.schema
import apps.online_test.schema
import apps.parent.schema
import apps.payment.schema
import apps.program.schema
import apps.report.schema
import apps.routine.schema
import apps.school.schema
import apps.schoolyear.schema
import apps.section.schema
import apps.student.schema
import apps.sub_school.schema
import apps.subject.schema
import apps.teacher.schema
import apps.employee.schema
import apps.support.schema
import apps.plan.schema
import apps.conversation.schema
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

class Query(
    UserQuery, 
    MeQuery, 
    account.schema.Query,
    apps.support.schema.Query,
    apps.classes.schema.Query, 
    apps.core.schema.Query, 
    apps.event.schema.Query, 
    apps.live.schema.Query, 
    apps.mark.schema.Query, 
    apps.menu.schema.Query, 
    apps.online_lesson.schema.Query, 
    apps.online_test.schema.Query, 
    apps.parent.schema.Query, 
    apps.payment.schema.Query, 
    apps.program.schema.Query, 
    apps.report.schema.Query, 
    apps.routine.schema.Query, 
    apps.school.schema.Query, 
    apps.schoolyear.schema.Query, 
    apps.section.schema.Query, 
    apps.student.schema.Query, 
    apps.sub_school.schema.Query, 
    apps.subject.schema.Query, 
    apps.teacher.schema.Query, 
    apps.employee.schema.Query, 
    apps.plan.schema.Query,
    apps.conversation.schema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    AuthMutation, 
    account.schema.Mutation,
    apps.support.schema.Mutation,
    apps.classes.schema.Mutation, 
    apps.core.schema.Mutation, 
    apps.event.schema.Mutation, 
    apps.live.schema.Mutation, 
    apps.mark.schema.Mutation, 
    apps.menu.schema.Mutation, 
    apps.online_lesson.schema.Mutation, 
    apps.online_test.schema.Mutation, 
    apps.parent.schema.Mutation, 
    apps.payment.schema.Mutation, 
    apps.program.schema.Mutation, 
    apps.routine.schema.Mutation, 
    apps.school.schema.Mutation, 
    apps.schoolyear.schema.Mutation, 
    apps.section.schema.Mutation, 
    apps.student.schema.Mutation, 
    apps.sub_school.schema.Mutation, 
    apps.subject.schema.Mutation, 
    apps.teacher.schema.Mutation, 
    apps.employee.schema.Mutation,
    apps.plan.schema.Mutation,
    apps.conversation.schema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)