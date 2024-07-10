from rest_framework.decorators import api_view , action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets , status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication 

from .models import Person , Color
from .serializers import PeopleSerializer , ColorsSerializer ,  RegisterSerializer , LoginSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.core.paginator import Paginator



class LoginApi(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.data.get('username') , password=serializer.data.get('password'))
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'status': '200','message': 'login successfull', 'token' : token.key}, status.HTTP_200_OK)
            return Response({"status": 404 ,"message":serializer.errors}, status.HTTP_404_NOT_FOUND)


class RegisterApi(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'message': 'registration successfull' , 'data' : serializer.data}, status.HTTP_200_OK)
        return Response({'status': '404','message':serializer.errors}, status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message': "successfull", "data": data})


@api_view(['GET'])
def index(request):
    course = {
        "course_name": "Python",
        "learning": ["Flask", "Django", "FastApi"],
        "course_provider": "Scalar"
    }
    return Response(course)


class PersonView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self,request):
        persons = Person.objects.all()
        print(request.user)
        try:
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(persons , page_size)
            serializer = PeopleSerializer(instance=paginator.page(page), many=True)
            return Response({
                'status': 200,
                'result': serializer.data
            }, status.HTTP_200_OK)
        except:
            return Response({
                'status': 404,
                'message': "Invalid page no"
            }, status.HTTP_404_NOT_FOUND)
    
    def post(self,request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self,request):
        person = get_object_or_404(Person, pk=int(request.GET.get('id')))
        serializer = PeopleSerializer(data=request.data, instance=person)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request):
        person = get_object_or_404(Person, pk=int(request.GET.get('id')))
        serializer = PeopleSerializer(data=request.data, instance=person, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request):
        person = get_object_or_404(Person, pk=int(request.GET.get('id')))
        person.delete()
        return Response({"message": "Person deleted successfully", "person": person})


# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# # def people(request):
#     if request.method=="GET":
#         persons = Person.objects.all()
#         serializer = PeopleSerializer(persons, many=True)
#         return Response(serializer.data) 
     
#     elif request.method=="POST":
#         data = request.data
#         serializer = PeopleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     elif request.method=="PUT":
#         person = get_object_or_404(Person, pk=int(request.GET.get('id')))
#         serializer = PeopleSerializer(data=request.data, instance=person)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
        
#     elif request.method=="PATCH":
#         person = get_object_or_404(Person, pk=int(request.GET.get('id')))
#         serializer = PeopleSerializer(data=request.data, instance=person, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     elif request.method=="DELETE":
#         person = get_object_or_404(Person, pk=int(request.GET.get('id')))
#         person.delete()
#         return Response({"message": "Person deleted successfully"})
    


@api_view(['GET'])
def colors(request):
    colors = Color.objects.all()
    seriailizer = ColorsSerializer(colors, many=True)
    return Response(seriailizer.data)


class PersonViewset(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    http_method_names = ['get','post']

    def list(self, request):
        search = request.GET.get('search')
        queryset =  self.queryset
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = PeopleSerializer(queryset, many=True)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})
    
    @action(detail=True ,methods=['POST'])
    def send_mail(self, request , pk):
        queryset = self.queryset
        person = get_object_or_404(queryset , pk=pk)
        serializer = PeopleSerializer(instance=person)
        return Response({
            'status': 200,
            'message': 'email sent',
            'user': serializer.data
        })