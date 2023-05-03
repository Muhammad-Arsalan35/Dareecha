from django.template import loader
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from baham.enum_types import VehicleType
from baham.models import VehicleModel
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.

def view_home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render({}, request))

def view_vehicles(request):
    template = loader.get_template("vehicles.html")
    vehicles = VehicleModel.objects.all().order_by("vendor")
    context = {
        "vehicles" : vehicles,
    }
    return HttpResponse(template.render(context, request))

def add_vehicles(request):
    template = loader.get_template("add_vehicles.html")
    vehicleTypes = [tag for tag in VehicleType]
    context = {
        "VehicleType" : vehicleTypes
    }
    return HttpResponse(template.render(context, request))



def save_vehicle(request):
    _vendor = request.POST.get('vendor')
    _model = request.POST.get('model')
    _capacity = request.POST.get('capacity')
    _type = request.POST.get('type')

    newModel = VehicleModel(vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    newModel.save()
    return HttpResponseRedirect(reverse('view-vehicles'))

