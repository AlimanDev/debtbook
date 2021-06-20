from django.urls import path

from apps.restapi import views as rest_views


app_name = 'restapi'

urlpatterns = [
    # users
    path('user/auth/', rest_views.AuthUserAPIView.as_view(), name='user-auth'),
    path('user/acoount/', rest_views.AccountAPIView.as_view()),

    # contacts
    path('contact/', rest_views.ContactAPIView.as_view({'get': 'list', 'post': 'create'})),
    path('contact/<int:pk>/', rest_views.ContactAPIView.as_view({'get': 'retrieve', 'put': 'update'})),

    # debt
    path('payment/', rest_views.PaymentAPIView.as_view({'post': 'create'})),
    path('payment/<int:pk>/', rest_views.PaymentAPIView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('payment/list/contact/<int:pk>/', rest_views.PaymentAPIView.as_view({'get': 'list'})),
]
