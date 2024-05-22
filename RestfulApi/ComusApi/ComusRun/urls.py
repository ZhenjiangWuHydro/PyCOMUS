from django.urls import path

from .views import ComusRunView

urlpatterns = [
    path('run/', ComusRunView.as_view(), name='run'),
]
