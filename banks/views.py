from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import BankSerializer, TransactionReceiptSerializer, WaletSerializer
from django.db import transaction as trans
from rest_framework.response import Response
from .models import Bank, Walet, Transaction, TransactionType, TransactionReceipt, StarUser
from django.db.models import F

class TransactionBankToWaletViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            queryset = TransactionReceipt.objects.get(transaction_id=pk, sender=request.user)
            serializer = TransactionReceiptSerializer(queryset)
            return Response(serializer.data)
        except TransactionReceipt.DoesNotExist:
            return Response({"error": "Receipt not found or not accessible"}, status=404)

    def list(self, request):

        if request.user.is_superuser:
            queryset = Bank.objects.all()
        else:
            queryset = Bank.objects.filter(user=request.user)

        serializer = BankSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bank(self, request):
        amount = int(request.data.get('amount'))

        if amount <= 0:
            return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank = Bank.objects.get(user=request.user)
        except Bank.DoesNotExist:
            return Response({"error": "Bank account not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            walet = Walet.objects.get(user=request.user)
        except Walet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        if bank.amount < amount:
            return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        if amount > 500:
                staruser, created = StarUser.objects.get_or_create(user=request.user, defaults={"star": 0})
                staruser.star = F("star") + 1
                staruser.save(update_fields=["star"])
                staruser.refresh_from_db()
        
        with trans.atomic():
            bank.amount -= amount
            walet.amount += amount
            bank.save()
            walet.save()

            transaction_type, _ = TransactionType.objects.get_or_create(
            transactionType="Bank to Walet",
            name_bank=bank
        )
            transaction = Transaction.objects.create(
                sender=request.user,
                amount=amount,
                transaction_type=transaction_type
            )

            queryset = TransactionReceipt.objects.create(
                transaction=transaction,
                sender=request.user,
                receiver=None,
                amount=amount,
                transaction_type=transaction_type.transactionType
            )

        return Response({
            "message": "Transaction successfully completed.",
            "transaction_id": transaction.id,
            "receipt_id": queryset.receipt_id,
            "bank_balance": bank.amount,
            "wallet_balance": walet.amount,
            "transaction_type": transaction.transaction_type.transactionType
        }, status=status.HTTP_201_CREATED)
        
    
            
class TransactionWaletToWaletViewSet(viewsets.ViewSet):

    def list(self, request):

        if request.user.is_superuser:
            queryset = Walet.objects.all()
        else:
            queryset = Walet.objects.filter(user=request.user)

        serializer = WaletSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def walet(self, request):
        sender_phone = request.data.get('sender_phone')
        receiver_phone = request.data.get('receiver_phone')
        amount = int(request.data.get('amount'))

        if not sender_phone or not receiver_phone:
            return Response({"error": "The sender's or recipient's phone number is missing."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_wallet = Walet.objects.get(user=request.user)
        except Walet.DoesNotExist:
            return Response({"error": "User wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        if user_wallet.phone != sender_phone:
            return Response({"error": "The sender's phone number does not match the logged-in user's phone number."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = Walet.objects.get(phone=sender_phone)
            receiver = Walet.objects.get(phone=receiver_phone)

            if sender.amount < amount:
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            if amount > 500:
                staruser, created = StarUser.objects.get_or_create(user=request.user, defaults={"star": 0})
                staruser.star = F("star") + 1
                staruser.save(update_fields=["star"])
                staruser.refresh_from_db()
            
            with trans.atomic():  
                sender.amount -= amount
                receiver.amount += amount
                sender.save()
                receiver.save()

                
                transaction = Transaction.objects.create(
                    sender=sender.user,
                    receiver=receiver.user,
                    amount=amount,
                    transaction_type=TransactionType.objects.get_or_create(
                        transactionType="Walet to Walet"
                    )[0],
                )

                
                receipt = TransactionReceipt.objects.create(
                    transaction=transaction,
                    sender=sender.user,
                    receiver=receiver.user,
                    amount=amount,
                    transaction_type="Walet to Walet"
                )

            return Response({
                "message": "Transaction successfully completed.",
                "transaction_id": transaction.id,
                "receipt_id": receipt.receipt_id,
                "sender_balance": sender.amount,
                "receiver_balance": receiver.amount
            }, status=status.HTTP_201_CREATED)

        except Walet.DoesNotExist:
            return Response({"error": "One of the wallets was not found."}, status=status.HTTP_404_NOT_FOUND)
        



    