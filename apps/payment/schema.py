import graphene
from graphene_django.types import DjangoObjectType
from .models import Payment, Invoice, Invoice_stock
from ..student.models import Student
from django.conf import settings
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required, permission_required
import requests
from requests.structures import CaseInsensitiveDict
import json
from datetime import datetime

class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        
class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice
        
class Invoice_stockType(DjangoObjectType):
    class Meta:
        model = Invoice_stock

class Query(object):
    all_payments = graphene.List(PaymentType)
    payment_by_id = graphene.Field(PaymentType, id=graphene.Int(required=True))

    all_invoices = graphene.List(InvoiceType)
    invoice_by_id = graphene.Field(InvoiceType, id=graphene.Int(required=True))
    invoice_stocks = graphene.List(Invoice_stockType, invoice=graphene.Int(required=True))

    invoice_by_student = graphene.Field(InvoiceType)

    check_invoice_status = graphene.String(id=graphene.Int(required=True))

    @login_required
    @permission_required('payment.view_payment')
    def resolve_all_payments(self, info, **kwargs):
        return Payment.objects.all()

    @login_required
    @permission_required('payment.view_payment')
    def resolve_payment_by_id(root, info, id):
        try:
            return Payment.objects.get(pk=id)
        except Payment.DoesNotExist:
            return None

    @login_required
    @permission_required('payment.view_invoice')
    def resolve_all_invoices(self, info, **kwargs):
        return Invoice.objects.all()

    @login_required
    @permission_required('payment.view_invoice')
    def resolve_invoice_by_student(root, info):
        if info.context.user.is_student == True:
            return Invoice.objects.filter(student=info.context.user.student, status='PENDING').last()
        elif info.context.user.is_parent == True:
            return Invoice.objects.filter(student=info.context.user.parent.student, status='PENDING').last()
        else: 
            return None

    @login_required
    @permission_required('payment.view_invoice')
    def resolve_check_invoice_status(self, info, id):
        invoice = Invoice.objects.get(pk=id)
        auth_url = 'https://merchant.qpay.mn/v2/auth/token'
        auth_headers = CaseInsensitiveDict()
        auth_headers["Content-Type"] = "application/json"
        auth_headers["Authorization"] = "Basic RV9NSU5EOktNU01HSlVi"
        
        auth_resp = requests.post(auth_url, headers=auth_headers)
        
        if auth_resp.status_code == 401:
            return 'CONNECTION_FAIL'
        if auth_resp.status_code == 200:

            success_res = json.loads(auth_resp.content)
            access_token = json.dumps(success_res['access_token'])

            access_token = access_token.replace("\"", "")

            qpay_check_url = 'https://merchant.qpay.mn/v2/payment/check'
            qpay_check_headers = CaseInsensitiveDict()
            qpay_check_headers["Content-Type"] = "application/json"
            qpay_check_headers["charset"] = "utf-8"
            qpay_check_headers["Authorization"] = 'Bearer {}'.format(access_token)

            qpay_check_data = {
                "object_type": "INVOICE",
                "object_id": invoice.qpay_invoice_id,
                "offset": {
                    'page_number': 1,
                    'page_limit': 100 
                }
            } 

            json_qpay_check_data = json.dumps(qpay_check_data)
            
            qpay_check_resp = requests.post(qpay_check_url, headers=qpay_check_headers, data=json_qpay_check_data)
            qpay_check_resp = json.loads(qpay_check_resp.content)
            if qpay_check_resp['count'] == 1 and qpay_check_resp['rows'][0]['payment_status'] == 'PAID':
                invoice.status = qpay_check_resp['rows'][0]['payment_status']
                invoice.save()
                student = Student.objects.get(pk=invoice.student.id)
                student.is_paid = True
                student.save()
                return qpay_check_resp['rows'][0]['payment_status']
            else: 
                return 'PENDING'

    @login_required
    @permission_required('payment.view_invoice')
    def resolve_invoice_by_id(root, info, id):
        try:
            return Invoice.objects.get(pk=id)
        except Invoice.DoesNotExist:
            return None

    @login_required
    @permission_required('payment.view_invoice')
    def resolve_invoice_stocks(root, info, invoice):
        try:
            return Invoice_stock.objects.filter(invoice=invoice)
        except Invoice_stock.DoesNotExist:
            return None

#******************* 😎 Payment-MUTATIONS 😎 *************************#
class CreatePayment(graphene.Mutation):
    payment = graphene.Field(PaymentType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        amount = graphene.Decimal()
        is_current = graphene.Boolean()

    @login_required
    @permission_required('payment.add_payment')
    def mutate(self, info, title, description, amount, is_current):
        
        create_userID_i = info.context.user

        payment = Payment(title=title, description=description, amount=amount, create_userID=create_userID_i)
        payment.save()

        if is_current == True:
            Payment.objects.exclude(pk=payment.pk).update(is_current=False)

        return CreatePayment(payment=payment)

class UpdatePayment(graphene.Mutation):
    payment = graphene.Field(PaymentType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        amount = graphene.Decimal()
        id = graphene.ID()
        is_current = graphene.Boolean()

    @login_required
    @permission_required('payment.change_payment')
    def mutate(self, info, title, description, amount, id, is_current):

        payment = Payment.objects.get(pk=id)

        payment.title = title
        payment.description = description
        payment.amount = amount
        payment.save()

        if is_current == True:
            Payment.objects.exclude(pk=payment.pk).update(is_current=False)
        return UpdatePayment(payment=payment)
        
class DeletePayment(graphene.Mutation):
    payment = graphene.Field(PaymentType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('payment.delete_payment')
    def mutate(self, info, **kwargs):
        payment = Payment.objects.get(pk=kwargs["id"])
        if payment is not None:
            payment.delete()
        return DeletePayment(payment=payment)

        
#******************* 😎 Invoice-MUTATIONS 😎 *************************#
class CreateInvoice(graphene.Mutation):
    invoice = graphene.Field(InvoiceType)

    @login_required
    @permission_required('payment.add_invoice')
    def mutate(self, info):

        if info.context.user.is_student == True:
            student = Student.objects.get(pk=info.context.user.student.id)
        elif info.context.user.is_parent == True:
            student = Student.objects.get(pk=info.context.user.parent.student.id)
        payment = Payment.objects.get(is_current=True)

        auth_url = 'https://merchant.qpay.mn/v2/auth/token'
        auth_headers = CaseInsensitiveDict()
        auth_headers["Content-Type"] = "application/json"
        auth_headers["Authorization"] = "Basic RV9NSU5EOktNU01HSlVi"
        
        auth_resp = requests.post(auth_url, headers=auth_headers)
        
        if auth_resp.status_code == 401:
            return CreateInvoice(auth_resp.status_code)
        if auth_resp.status_code == 200:

            success_res = json.loads(auth_resp.content)
            access_token = json.dumps(success_res['access_token'])

            access_token = access_token.replace("\"", "")

            invoice_url = 'https://merchant.qpay.mn/v2/invoice'
            invoice_headers = CaseInsensitiveDict()
            invoice_headers["Content-Type"] = "application/json"
            invoice_headers["charset"] = "utf-8"
            invoice_headers["Authorization"] = 'Bearer {}'.format(access_token)

            invoice_data = {
                "invoice_code": "E_MIND_INVOICE",
                "sender_invoice_no": " ".join((student.school.name, student.student_code )),
                "invoice_receiver_code": " ".join((student.school.name, student.student_code )),
                "sender_branch_code": student.school.name,
                "amount": int(payment.amount),
                "invoice_description": " ".join((student.school.name, student.student_code )),
                "callback_url": "http://localhost:8000/graphql#query=%0Aquery%20check_invoice_status%20%7B%0A%20%20checkInvoiceStatus%20(id%3A%2010)%0A%7D"
            } 

            json_invoice_data = json.dumps(invoice_data)
            
            invoice_resp = requests.post(invoice_url, headers=invoice_headers, data=json_invoice_data)
            invoice_resp = json.loads(invoice_resp.content)

            qpay_invoice_id = invoice_resp['invoice_id']
            qpay_qr_text = invoice_resp['qr_text']
            qpay_qr_image = invoice_resp['qr_image']
            qpay_shortUrl = invoice_resp['qPay_shortUrl']
            qpay_deeplinks = invoice_resp['urls']
            
            create_userID_i = info.context.user

            invoice = Invoice(student=student, 
                            title=" ".join((student.school.name, student.student_code )), 
                            description=" ".join((student.school.name, student.student_code )),
                            amount=int(payment.amount), 
                            pay_date=datetime.now(),
                            status='PENDING', 
                            qpay_invoice_id=qpay_invoice_id,
                            qpay_qr_text=qpay_qr_text,
                            qpay_qr_image=qpay_qr_image,
                            qpay_shortUrl=qpay_shortUrl,
                            create_userID=create_userID_i)
            invoice.save()

            for link in qpay_deeplinks:
                invoice_stock = Invoice_stock(invoice=invoice, name=link['name'], description=link['description'], logo=link['logo'], link=link['link'])
                invoice_stock.save()
            return CreateInvoice(invoice=invoice)

class UpdateInvoice(graphene.Mutation):
    invoice = graphene.Field(InvoiceType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        amount = graphene.Decimal()
        pay_date = graphene.String()
        paid_date = graphene.String()
        status = graphene.String()
        id = graphene.ID()

    @login_required
    @permission_required('payment.change_invoice')
    def mutate(self, info, user, title, description, amount, pay_date, paid_date, status, id):

        invoice = Invoice.objects.get(pk=id)
        user_i = get_user_model().objects.get(pk=user)

        invoice.user = user_i
        invoice.title = title
        invoice.description = description
        invoice.amount = amount
        invoice.pay_date = pay_date
        invoice.paid_date = paid_date
        invoice.status = status
        invoice.save()
        return UpdateInvoice(invoice=invoice)
        
class DeleteInvoice(graphene.Mutation):
    invoice = graphene.Field(InvoiceType)
    class Arguments:
        id = graphene.ID()

    @login_required
    @permission_required('payment.delete_invoice')
    def mutate(self, info, **kwargs):
        invoice = Invoice.objects.get(pk=kwargs["id"])
        if invoice is not None:
            invoice.delete()
        return DeleteInvoice(invoice=invoice)

#******************* 😎 Invoice_stock-MUTATIONS 😎 *************************#
class CreateInvoice_stock(graphene.Mutation):
    invoice_stock = graphene.Field(Invoice_stockType)

    class Arguments:
        invoice = graphene.Int()
        title = graphene.String()
        description = graphene.String()
        amount = graphene.Decimal()

    @login_required
    @permission_required('payment.add_invoice_stock')
    def mutate(self, info, invoice, title, description, amount):
        
        invoice_i = Invoice.objects.get(pk=invoice)
        create_userID_i = info.context.user

        invoice_stock = Invoice_stock(invoice=invoice_i, title=title, description=description, amount=amount, create_userID=create_userID_i)
        invoice_stock.save()
        return CreateInvoice_stock(invoice_stock=invoice_stock)

class Mutation(graphene.ObjectType):
    create_payment = CreatePayment.Field()
    update_payment = UpdatePayment.Field()
    delete_payment = UpdatePayment.Field()
    create_invoice = CreateInvoice.Field()