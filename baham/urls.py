from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.view_home, name="home"),
    path("view-vehicles", views.view_vehicles, name="view-vehicles"),
    path("add-vehicles", views.add_vehicles, name="add-vehicles"),
    path("add-vehicles/save-vehicle", views.save_vehicle, name="save-vehicle"),
]
