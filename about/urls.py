from django.urls import path
from .views import LinePayCallbackView, AboutView, LinePayRequestView

app_name = "about"

urlpatterns = [
    path("", AboutView.as_view(), name='about'),
    path('linepay/request/', LinePayRequestView.as_view(), name='linepay_request'),
    path('about/', LinePayCallbackView.as_view(), name='linepay_callback'),
]


