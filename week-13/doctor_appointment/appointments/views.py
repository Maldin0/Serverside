from django.shortcuts import render
from appointments.models import *
from appointments.serializer import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from appointments.permissions import AppointmentListPermission, AppointmentDetailsPermission

class MyTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
# Create your views here.
class DoctorList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [AppointmentListPermission]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializers = AppointmentSerializer(appointments, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        
        # doctor = Doctor.objects.get(id=data['doctor'])
        # patient = Patient.objects.get(id=data['patient'])
        
        # doctor_serializer = DoctorSerializer(doctor)
        # patient_serializer = PatientSerializer(patient)
        
        # data['doctor'] = doctor_serializer.data
        # data['patient'] = patient_serializer.data
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        data['at_time'] = datetime.strptime(data['at_time'], '%H:%M:%S').time()
        appointment = CreatAppointmentSerializer(data=data)

        if appointment.is_valid():
            appointment.save(created_by=request.user)
            return Response(appointment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(appointment.errors, status=status.HTTP_200_OK)
    
class AppointmentDetails(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [AppointmentDetailsPermission]
    
    def get(self, request, app_id):
        try:
            appo = Appointment.objects.get(id=app_id)
            serializers = AppointmentSerializer(appo)
            return Response(serializers.data, status=status.HTTP_302_FOUND)
        except:
            return Response(data={'error' : 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, app_id):
        
        try:
            appo = Appointment.objects.get(id=app_id)
        except Appointment.DoesNotExist:
            return Response(data={'error' : 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, appo)
        serializers = CreatAppointmentSerializer(appo, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, app_id):
        try:
            appo = Appointment.objects.get(id=app_id)
        except Appointment.DoesNotExist:
            return Response(data={'error' : 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, appo)
        appo.delete()
        return Response(data={'message' : "Appointment Deleted"}, status=status.HTTP_200_OK)

        
