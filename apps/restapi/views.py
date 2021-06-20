from rest_framework import generics, viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.users import models as user_models
from apps.users import serializers as user_serializers
from apps.contacts import models as contact_models
from apps.contacts import serializers as contact_serializers


class AuthUserAPIView(generics.GenericAPIView):
    """ Для авторизации/регистрации и получения токена """
    serializer_class = user_serializers.AuthUserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        account, _ = user_models.Account.objects.get_or_create(phone=phone)
        if code:
            return self.code_verification(account, code)
        new_code = self.send_sms_code(phone)
        account.sms_code = new_code
        account.save(update_fields=['sms_code'])
        return Response({'detail': 'Отправлен смс-код'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def gen_code():
        """ Генерация смс-кода """
        code = 1234
        # from random import randint
        # code = randint(0000, 9999)  # TODO: подключить генерацию кода
        return str(code)

    def send_sms_code(self, phone):
        """ Отправка смс-кода """
        # TODO: интегрировать СМС-сервис
        return self.gen_code()

    def code_verification(self, account, code):
        """ Если код от аккаунта верный - возвращает токен,
        иначе возвращает ошибку"""
        if account.sms_code == str(code):
            token = Token.objects.get(user=account)
            account.sms_code = self.gen_code()
            account.save(update_fields=['sms_code'])
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Неверный смс-код'}, status=status.HTTP_401_UNAUTHORIZED)


class AccountAPIView(generics.RetrieveUpdateAPIView):
    """ Для получения/редактирования своего аккаунта """
    serializer_class = user_serializers.AccountSerializer
    model = user_models.Account
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_object(self):
        return self.request.user


class ContactAPIView(viewsets.ModelViewSet):
    """ Для управления контактами """
    serializer_class = contact_serializers.ContactSerializer
    queryset = contact_models.Contact.objects.all()  # TODO: скрыть 'удалённые/скрытые' контакты
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'post']

    def create(self, request, *args, **kwargs):
        """ Для создания контакта """
        # TODO: написать проверку на дубликат контакта - 'phone'
        request.data['accounts'] = [request.user.id]
        return super().create(request, *args, **kwargs)


class PaymentAPIView(viewsets.ModelViewSet):
    """ Для управления платежами """
    serializer_class = contact_serializers.PaymentSerializer
    queryset = contact_models.Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'post']


class PaymentAPIListView(generics.ListAPIView):
    """ Для получения списка платежей контакта """
    serializer_class = contact_serializers.PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        try:
            obj = contact_models.Contact.objects.get(pk=self.kwargs.get(self.lookup_field))
            return obj.payments.all()
        except contact_models.Contact.DoesNotExist:
            return None
