from django.db import models
from baham.enum_types import VehicleType, VehicleStatus, UserType
from baham.constants import COLORS, TOWNS
from django.utils import timezone
from django.contrib.auth.models import User


def validate_color(val):
    return val.upper() in COLORS


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=[
                              ('M', 'Male'), ('F', 'Female')])
    type = models.CharField(max_length=10, choices=[
                            (t.name, t.value) for t in UserType])
    primary_contact = models.CharField(max_length=20, null=False, blank=False)
    alternate_contact = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255)
    address_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True)
    address_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True)
    landmark = models.CharField(max_length=255, null=False)
    town = models.CharField(max_length=50, null=False,
                            choices=[(c, c) for c in TOWNS])
    active = models.BooleanField(default=True, editable=False)
    date_deactivated = models.DateTimeField(editable=False, null=True)
    bio = models.TextField()
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.username} {self.user.first_name} {self.user.last_name}"

    def delete(self, *args, **kwargs):
        if not self.user.is_staff:
            raise PermissionError(
                "NOT aLLOWED")
        super().delete(*args, **kwargs)


class VehicleModel(models.Model):
    make_id = models.AutoField(primary_key=True, db_column='id')
    # # E.g. Vitz, Corolla, Swift
    vendor = models.CharField(max_length=20, null=False, blank=False)
    model = models.CharField(max_length=20, null=False,
                             blank=False, default='Unknown')
    type = models.CharField(max_length=50, choices=[(
        t.name, t.value) for t in VehicleType], help_text="Select the vehicle chassis type")
    capacity = models.PositiveSmallIntegerField(null=False, default=2)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "baham_vehicle_model"

    def __str__(self):
        return f"{self.vendor} {self.model}"

    def delete(self, *args, **kwargs):
        if not self.updated_by.is_staff:
            raise PermissionError(
                "NOT aLLOWED")
        super().delete(*args, **kwargs)


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, db_column='id')
    registration_number = models.CharField(max_length=10, unique=True, null=False,
                                           blank=False, help_text="Unique registration/license plate no. of the vehicle.")
    color = models.CharField(
        max_length=50, default='white', validators=[validate_color])
    model = models.ForeignKey(VehicleModel, null=False,
                              on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date_added = models.DateField(models.DateTimeField(
        default=timezone.now, editable=False))
    status = models.CharField(max_length=50, choices=[
                              (t.name, t.value) for t in VehicleStatus])
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.model.vendor} {self.model.model} {self.color}"

    def delete(self, *args, **kwargs):
        if self.owner.is_staff:
            super().delete(*args, **kwargs)
        else:
            raise PermissionError(
                "NOT aLLOWED")


class Contract (models.Model):
    contract_id = models.AutoField(primary_key=True, db_column='id')
    vehicle = models.ForeignKey(Vehicle, null=False, on_delete=models.CASCADE)
    companion = models.ForeignKey(
        UserProfile, null=False, on_delete=models.CASCADE)
    effective_start_date = models.DateField(null=False)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    fuel_share = models.PositiveSmallIntegerField(
        help_text="Percentage of fuel contribution")
    maintenance_share = models.PositiveSmallIntegerField(
        help_text="Percentage of maintainance contribution")
    schedule = models.JSONField()  # use TODO: Scheduler
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    def delete(self, *args, **kwargs):
        if self.companion.user.is_staff:
            super().delete(*args, **kwargs)
        else:
            raise PermissionError(
                "NOT aLLOWED")
