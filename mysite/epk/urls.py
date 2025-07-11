from django.urls import path
from . import views

app_name = "epk"

urlpatterns = [
    path("", views.main, name="main"),
    path("waitingList/", views.customerWaitingList, name="waitingList"),
    path("workingList/", views.customerWorkingList, name="workingList")
    ]