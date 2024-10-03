from django.urls import path
from appointments.views import *
urlpatterns = [
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('patients/', PatientList.as_view(), name='patient-list'),
    path('appointments/', AppointmentList.as_view(), name='appointment-list'),
    path('appointments/<int:app_id>/', AppointmentDetails.as_view(), name='appointment-get')
]