from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import AppointmentsPermission

class TokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

# Create your views here.
class DoctorList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppintmentDetailList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, AppointmentsPermission]
    
    def get(self, request, pk):
        appointments = self.get_appointment(pk)
        if not appointments:
            return Response({"message": "No appointments found for this doctor."})
        serializer = AppointmentSerializer(appointments)
        return Response(serializer.data)
    
    def put(self, request, pk):
        appointments = self.get_appointment(pk)
        if not appointments:
            return Response({"message": "No appointments found for this doctor."})
        if appointments.created_by != request.user:
            return Response({"message": "You do not have permission to update this appointment."}, status=403)
        serializer = UpdateAppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        appointments = self.get_appointment(pk)
        if not appointments:
            return Response({"message": "No appointments found for this doctor."})
        if appointments.created_by != request.user:
            return Response({"message": "You do not have permission to update this appointment."}, status=403)
        serializer = UpdateAppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        appointments = self.get_appointment(pk)
        if not appointments:
            return Response({"message": "No appointments found for this doctor."})
        if appointments.created_by != request.user:
            return Response({"message": "You do not have permission to delete this appointment."}, status=403)
        appointments.delete()
        return Response({"message": "Appointment deleted successfully."})
    
    def get_appointment(self, pk: int):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return None
        

class AppointmentList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.has_perm('appointments.add_appointment'):
            return Response({"message": "You do not have permission to add an appointment."}, status=403)
        serializer = UpdateAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)