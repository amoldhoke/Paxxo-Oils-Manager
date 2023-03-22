from .serializers import CustomerSerializer, ListSerializer, MessageSerializer, CustomerStatusSerializer, EmailSerializer
from Inbox.models import Customer

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,RetrieveDestroyAPIView, RetrieveAPIView

from .paginations import CustomerPagination
from rest_framework.filters import SearchFilter

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.mail import EmailMessage

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# ROUTE GUIDE
@api_view(['GET'])
def getRoutes(request):
    routes = [
      'For API Documentation: api/docs/',
      'For token Authentication',
      'To get Token: gettoken/',
      'To get Refreshtoken: refreshtoken/',
      'To Verify Token: verifytoken/',
      'For Enquiry: send_message/',
      'Get List: inbox/',
      'Invidual Customer: inbox/<int:pk>/',
      'Email : email/<int:pk>/',
    ]
    return Response(routes)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# CANDIDATE REGISTRATON
class CustomerMessage(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = MessageSerializer


# FOR ADMIN AND STAFF
class InboxList(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination
    # FOR FILTER AND SEARCH
    filter_backends = [SearchFilter]
    search_fields = ['name','email', 'phone']
    http_method_names = ['get', 'delete']
    # FOR AUTHENTICATION
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListSerializer
        return CustomerSerializer


class StatusUpdate(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerStatusSerializer
    # FOR AUTHENTICATION
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Email(RetrieveDestroyAPIView):
    queryset = Customer.objects.all()
    # FOR AUTHENTICATION
    authentication_classes=[JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerSerializer
        else:
            return EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        cc = serializer.validated_data.get('cc')
        subject = serializer.validated_data.get('subject')
        message = serializer.validated_data.get('message')
        files = request.FILES.getlist('files')

        # create email message
        email_message = EmailMessage(
            cc=[cc],
            subject=subject,
            body=message,
            from_email='PAXXO OIL <wowcreativity07@gmail.com>',
            to=[email],
        )

        # attach files to email message
        for file in files:
            email_message.attach(file.name, file.read(), file.content_type)

        # send email message
        email_message.send()
        # return a Response with a success message
        return Response({'message': 'Email sent successfully'}, status=200)



