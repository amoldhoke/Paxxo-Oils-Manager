from django.urls import path, include
from rest_framework import routers
from .views import CustomerMessage, getRoutes, Email, InboxList, StatusUpdate, MyTokenObtainPairView
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'inbox', InboxList)

urlpatterns = [
    path('', getRoutes, name='getRoutes'),
    path('send_message/', CustomerMessage.as_view()),
    path('', include(router.urls)),
    path('inbox-status/<int:pk>/', StatusUpdate.as_view()),
    path('email/<int:pk>/', Email.as_view()),
    # Token Authentication
    path('gettoken/', MyTokenObtainPairView.as_view()),
    path('refreshtoken/', TokenRefreshView.as_view()),
    path('verifytoken/', TokenVerifyView.as_view()),
]


# httpie shortcuts
# http POST http://127.0.0.1:8000/api/gettoken/ username="amoldhoke" password="root"
# http POST http://127.0.0.1:8000/api/verifytoken/ token=""
# http POST http://127.0.0.1:8000/api/refreshtoken/ refresh=""
# http http://127.0.0.1:8000/api/send_message/ 'Authorization:Bearer '
# http http://127.0.0.1:8000/api/inbox/ 'Authorization:Bearer '
# http http://127.0.0.1:8000/api/inbox/22/ 'Authorization:Bearer '
# http http://127.0.0.1:8000/api/email/22/ 'Authorization:Bearer '
# http http://127.0.0.1:8000/api/inbox-status/22/ 'Authorization:Bearer '