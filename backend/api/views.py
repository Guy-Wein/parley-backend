from timeit import repeat
from .serializers import AdvanceSerializer, TransactionSerializer, FiveDaysSerializer
from .models import Transaction, User, Advance
from rest_framework import generics, permissions, mixins
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta, datetime
import requests
from rest_framework.reverse import reverse
from django_q.tasks import schedule

class ProcessorListMixin(mixins.ListModelMixin, generics.GenericAPIView):
    today = date.today()
    fivedays_before = today - timedelta(days=5)
    queryset = Transaction.objects.filter(timestamp__gte=fivedays_before).order_by('-timestamp')
    serializer_class = FiveDaysSerializer

    def get(self, request, *args, **kargs):
        return self.list(request, *args, **kargs)

class ProcessorCreateMixin(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kargs):
        return self.create(request, *args, **kargs)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(timestamp=datetime.now())
        # get the amount that was transfered
        amount = serializer.data.get('amount')
        # get the bank accounts qs
        src = User.objects.get(pk=serializer.data.get('src_bank_account'))
        dst = User.objects.get(pk=serializer.data.get('dst_bank_account'))
        # get the transaction's id
        id = Transaction.objects.get(pk=serializer.data.get('id'))
        # check for the direction method
        if serializer.data.get('direction') == 'debit':
            if src.balance < amount:
                id.status = "fail"
                id.save()
                raise ValidationError({"message":"not enough money in the payer account"})
            # subtract amount from source and add to dst
            src.balance -= amount
            src.save()
            dst.balance += amount
            dst.save()
        else:
            if dst.balance < amount:
                id.status = "fail"
                id.save()
                raise ValidationError({"message":"not enough money in the payer account"})
            # add amount to source and subtract from dst
            src.balance += amount
            src.save()
            dst.balance -= amount
            dst.save()

class ProcessorCreateAdvance(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Advance.objects.all()
    serializer_class = AdvanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kargs):
        return self.create(request, *args, **kargs)

    def call_transaction_create(self, json_obj):
        print("check 3333333333333")
        url = reverse("processor_create")
        print("check 3333333333333")
        api_request = requests.post(url, json=json_obj)
        print("check 3333333333333")
        # check if the request is successful
        try:
            # check if request is successful
            api_request.raise_for_status() 
            # do something else with it
        except:
            # request failed
            pass
    def perform_create(self, serializer):
        # check if serializer is valid
        if serializer.is_valid():
            # add the values to the serializer 
            serializer.save(src_bank_account=self.request.user)
            # add the amount to the dst's user balance
            # get the amount from serializer
            amount = int(serializer.data.get('amount')) / 12
            dst_account = serializer.data.get('dst_bank_account')
            # get the dst_user's qs
            dst = User.objects.get(pk=dst_account)
            dst.balance += amount
            dst.save()

            print(self.request.user.id)
            print(dst_account)
            # call the 12 debit function
            json_obj = {
                "src_bank_account":self.request.user.id,
                "dst_bank_account":dst_account,
                "amount":amount,
                "direction":"debit"
            }
            schedule(
                'self.call_transaction_create',
                json_obj, 
                schedule_type='W', 
                repeats=12
            )
        else:
            raise ValidationError

    '''
    src_bank_account
    dst_bank_account
    amount
    direction
    status
    timestamp
    '''