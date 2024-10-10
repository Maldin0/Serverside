from django.contrib.auth.models import User
from rest_framework import serializers
from appointments.models import *
from datetime import datetime

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]
        
class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only = True)
    patient = PatientSerializer(read_only = True)
    class Meta:    
        model = Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'date',
            'at_time',
            'details',
        ]
    def create(self, validated_data):
        
        return Appointment.objects.create(**validated_data)
    
    def validate(self, data):
        print("Called")
        present = datetime.now()
        appointmentDT = datetime.combine(date=data['date'], time=data['at_time'])
        print(f'{appointmentDT} < {present}')
        if appointmentDT < present:
            raise serializers.ValidationError("The appointment date or time must be in the future.")
        return super().validate(data)
    
class CreatAppointmentSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'date',
            'at_time',
            'details',
        ]
    
    def validate(self, data):
        print("Called")
        present = datetime.now()
        appointmentDT = datetime.combine(date=data['date'], time=data['at_time'])
        print(f'{appointmentDT} < {present}')
        if appointmentDT < present:
            raise serializers.ValidationError("The appointment date or time must be in the future.")
        return super().validate(data)