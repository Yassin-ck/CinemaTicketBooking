from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from authentications.modules.smtp import send_email
from django.conf import settings
from theatre_dashboard.models import (
    TheareOwnerDetails,
    TheatreDetails,
    )
from django.db.models import Q
from .serializers import (
    UserProfileViewSerializer,
    RequestedLocationSerializer,
    TheatreOwnerDetailsSerializer,
    TheatreDetailsSerializer,
    )
from rest_framework.views import APIView
from authentications.models import (
    MyUser,
    UserProfile,
    RequestLocation,
    )
# Create your views here.

@permission_classes([IsAdminUser])
class UserProfileViewBYAdmin(APIView):
    def get(self,request):
        user_profile = UserProfile.objects.select_related('user')
        serializer = UserProfileViewSerializer(user_profile,many=True)
        return Response(serializer.data)
    

@permission_classes([IsAdminUser])
class LocationRequests(APIView):
    def get(self,request):
        requested_location = RequestLocation.objects.filter(status='PENDING')
        serializer = RequestedLocationSerializer(requested_location,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
      
    def patch(self,request,pk=None):
        if pk:
            location = RequestLocation.objects.get(id=pk)
            serializer = RequestedLocationSerializer(location)
            return Response(serializer.data,status=status.HTTP_200_OK)
           
           

@permission_classes([IsAdminUser])
class TheatreOwnerRequest(APIView):
    def get(self,request,pk=None):
        if not pk:
            details = TheareOwnerDetails.objects.filter(Q(is_verified=True) & Q(is_approved=False))
            serializer = TheatreOwnerDetailsSerializer(details,many=True)
        else:
            details = TheareOwnerDetails.objects.get(id=pk)
            serializer = TheatreOwnerDetailsSerializer(details)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


    def patch(self,request,pk=None):
        if pk:
            details=TheareOwnerDetails.objects.get(id=pk)
            serializer = TheatreOwnerDetailsSerializer(details, data=request.data, partial=True)
            if serializer.is_valid():
                verification = serializer.validated_data.get('is_approved')
                if verification:
                    subject = 'Request Approved...'
                    message = '''Welcome to BookMyShow....
                    Now you can update your theatre details
                    '''
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [details.email]
                    send_email(subject,message,email_from,recipient_list)
                    return Response({'msg':'is_approved'},status=status.HTTP_200_OK)
                subject = 'Request Rejected...'
                message = ''' 
                We cant verify your credentials,
                Please Contact with our customer service or You can use our message system
                '''
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [details.email]
                send_email(subject,message,email_from,recipient_list)
                return Response({'msg':'Rejected'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
    
 
@permission_classes([IsAdminUser])
class TheatreRequest(APIView):
    
    def get(self,request,pk=None):
        if not pk:
            details = TheatreDetails.objects.filter(is_verified=False)
            serializer = TheatreDetailsSerializer(details,many=True)
        else:
            details = TheatreDetails.objects.get(id=pk)
            serializer = TheatreDetailsSerializer(details)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def patch(self,request,pk=None):
        if pk:
            details=TheatreDetails.objects.get(id=pk)
            serializer = TheatreDetailsSerializer(details, data=request.data, partial=True)
            if serializer.is_valid():
                verification = serializer.validated_data.get('is_verified')
                print(verification)
                serializer.save()
                if verification:
                    subject = 'Request Approved...'
                    message = '''
                    Welcome to BookMyShow....
                    Your Theatre Registration is completed ,
                    Now You can go with you further details ...           
                    '''
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [details.email]
                    send_email(subject,message,email_from,recipient_list)
                    return Response({'msg':'verified'},status=status.HTTP_200_OK)
                subject = 'Theatre Request Rejected...'
                message = ''' We cant verify your credentials,
                Please Contact with our customer service or You can use our message system    '''
                email_from = settings.EMAIL_HOST_USER
                return Response({'msg':'Rejected'},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    