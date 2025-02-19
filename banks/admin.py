from django.contrib import admin
from .models import Bank, StarUser, Walet, Transaction, TransactionType , TransactionReceipt


admin.site.register(Bank)
admin.site.register(StarUser)
admin.site.register(Walet)
admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(TransactionReceipt)