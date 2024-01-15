from django.db.models import CharField, ForeignKey, DateTimeField, DecimalField, TextField, Model, CASCADE, BooleanField
from django.conf import settings
from ..student.models import Student

class Payment(Model):
    title = CharField(max_length=50)
    description = CharField(max_length=50)
    amount = DecimalField(max_digits=12, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_current = BooleanField(default=False)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'payment_create_userID', on_delete=CASCADE)

    def __str__(self):
        return self.title

class Invoice(Model):
    STATUS_CHOICES = (
        ('PENDING', 'Төлөөгүй',),
        ('PAID', 'Төлсөн',),
    )

    student = ForeignKey(Student, on_delete=CASCADE, null=True)
    title = CharField(max_length=50)
    description = CharField(max_length=50)
    amount = DecimalField(max_digits=12, decimal_places=2)
    pay_date = DateTimeField(blank=True, null=True)
    paid_date = DateTimeField(blank=True, null=True)
    qpay_invoice_id = CharField(max_length=200, null=True)
    qpay_qr_text = TextField(null=True)
    qpay_qr_image = TextField(null=True)
    qpay_shortUrl = TextField(null=True)
    status = CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    create_userID = ForeignKey(settings.AUTH_USER_MODEL, related_name = 'invoice_create_userID', on_delete=CASCADE)

    def __str__(self):
        return self.title

class Invoice_stock(Model):
    invoice = ForeignKey(Invoice, on_delete=CASCADE)
    name = CharField(max_length=50, null=True)
    description = CharField(max_length=50, null=True)
    logo = CharField(max_length=200, null=True)
    link = TextField(null=True)
    
    def __str__(self):
        return self.name