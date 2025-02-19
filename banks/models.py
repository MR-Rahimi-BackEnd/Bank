import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal




class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='موجودی به ریال')
    bank_name = models.CharField(max_length=500)
    phone = models.CharField(max_length=50)
    
    
    def __str__(self):
        return f'{self.bank_name} ({self.user})'

class Walet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField(verbose_name='موجودی به ریال')
    
    def __str__(self):
        return f'{self.phone} - {self.user}'
    

class TransactionType(models.Model):
    
    TRANSACTION_TYPE_CHOICES = (
        ("Bank to Walet","Bank to Walet"),
        ("Walet to Walet","Walet to Walet")
    )
    
    
    name_bank = models.ForeignKey(Bank,on_delete=models.CASCADE , blank=True , null=True)
    name_walet = models.ForeignKey(Walet,on_delete=models.CASCADE , blank=True , null=True)
    transactionType = models.CharField(choices=TRANSACTION_TYPE_CHOICES,max_length=15)
    
    
    def __str__(self):
        return f'{self.name_bank}'

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_transactions', null=True, blank=True)
    amount = models.IntegerField(verbose_name='موجودی به ریال')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        TransactionReceipt.objects.create(
            transaction=self,
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            transaction_type=self.transaction_type.transactionType
        )

    def __str__(self):
        return f"Transaction {self.id} from {self.sender}"


class TransactionReceipt(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='receipt')
    receipt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_receipts')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_receipts', null=True, blank=True)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Receipt {self.receipt_id} for Transaction {self.transaction.id}"
    
    
    
class StarUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    star = models.IntegerField()
    
    
    def __str__(self):
        return f'{self.star}'