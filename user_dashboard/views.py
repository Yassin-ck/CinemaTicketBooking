from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from django.db.models import Q , Prefetch , F
from admin_dashboard.models import MoviesDetails
from rest_framework import status
from datetime import timedelta
from utils.mapping_variables import to_third_day,today, RELEASED, Available_dates
from rest_framework.permissions import (
    AllowAny,
)
from admin_dashboard.models import (
    Languages,
    MoviesDetails
    )
from theatre_dashboard.models import (
    TheatreDetails,
    ScreenDetails,
    ScreenSeatArrangement,

)
from admin_dashboard.serializers import (
    MovieDetailListSerializer,
)
from theatre_dashboard.serializers import (
    ScreenSeatArrangementChoiceSerailizer,
    
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

    

def screen_seat_details(Q_Base):
    return ScreenSeatArrangement.objects.filter(Q_Base).annotate(
        theatre_name=F('screen__theatre__theatre_name'),
        screen_number=F('screen__screen_number'),
        show_time=F('screen__shows__show_time__time'),
        show_dates=F('screen__shows__show_dates__dates'),
        movie_name=F('screen__shows__movies__movie_name'),
        language=F('screen__shows__language__name')).values(
            'seating',
            'screen_number',
            'show_time',
            'show_dates',
            'movie_name',
            'language',
            'theatre_name'
            ).first()  

@permission_classes([AllowAny])
class MovieSearching(APIView):
    name = openapi.Parameter('q',in_=openapi.IN_QUERY, description="movie name or director name",type=openapi.TYPE_STRING,)
    @swagger_auto_schema(
        operation_description="return list of movies by searching movie name or director name",
        manual_parameters=[name],
        responses={
            200:MovieDetailListSerializer,
            404:"Not Found",
            500:"errors"
        }
    )
    def get(self, reqeust):
        q = reqeust.GET.get("q")
        movies = MoviesDetails.objects.filter(Q(movie_name__icontains=q) | Q(director__icontains=q)).values('id','movie_name')
        if movies:
            return Response(movies, status=status.HTTP_200_OK)
        return Response({"data":"Not Found"}, status=status.HTTP_404_NOT_FOUND)




@permission_classes([AllowAny])
class MovieSelectionView(APIView):
    location = openapi.Parameter( 'search', in_=openapi.IN_QUERY, description='location', type=openapi.TYPE_STRING, )
    language = openapi.Parameter( 'q', in_=openapi.IN_QUERY, description='language', type=openapi.TYPE_STRING, )
    movie = openapi.Parameter( 'movie', in_=openapi.IN_QUERY, description='movies', type=openapi.TYPE_STRING, )
    cinemas = openapi.Parameter( 'cinemas', in_=openapi.IN_QUERY, description='theatre', type=openapi.TYPE_STRING, )
    screen = openapi.Parameter( 'screen', in_=openapi.IN_QUERY, description='screen number', type=openapi.TYPE_STRING, )
    date = openapi.Parameter( 'dt', in_=openapi.IN_QUERY, description='date', type=openapi.TYPE_STRING, )
    @swagger_auto_schema(
    manual_parameters=( location, language, movie, cinemas, screen,date),
    operation_description = f"return list of all recordes of theatre and details by location of user",
    responses = {
        200:ScreenSeatArrangementChoiceSerailizer,
        400:'bad syntax',
        500:'error'
        })
    def get(self, request):
        q = request.GET.get("q")
        location = request.GET.get("search")
        movie = request.GET.get("movie")
        cinemas = request.GET.get("cinemas")
        screen = request.GET.get("screen")
        date = request.GET.get('dt')
        times = request.GET.get('tm')
        
        if location:
            Q_Base = (
                ~Q(status=RELEASED) &
                (Q(shows__screen__theatre__location__place=location) |
                Q(shows__screen__theatre__location__district=location)) &
                Q(shows__show_dates__dates__range=(today,to_third_day)))
        if movie and cinemas and screen:
            if q != 'all' and q is not None :
                response = self.get_screen_details(location ,cinemas,date,screen,movie,times,q)
            else:
                response = self.get_screen_details(location ,cinemas,date,screen,movie,times)
            return Response(response, status=status.HTTP_200_OK)
        elif movie: 
            Q_Base = (
                Q(shows__movies__movie_name=movie) & ( 
                Q(theatre__location__place=location)| 
                Q(theatre__location__district=location)) &
                Q(screenseatarrangement__is_approved=True)&
                Q(shows__show_dates__dates=date))
            if q != 'all' and q is not None :  
                Q_Base &= Q(shows__language__name=q)
            response = self.get_theatre_screen_details(Q_Base) 
            return Response({'data':response,'dates':Available_dates}, status=status.HTTP_200_OK)       
        if q != 'all' and q is not None :
            Q_Base &= Q(shows__language__name=q)
        movies = MoviesDetails.objects.filter(Q_Base).distinct().values('id','movie_name','poster','director')
        languages = Languages.objects.all().values('name')
        return Response({"movies": movies,"languages":languages}, status=status.HTTP_200_OK)


    
    def get_theatre_screen_details(self,Q_Base):
        theatres = ScreenDetails.objects.filter(Q_Base).annotate(
            theatre_name=F('theatre__theatre_name'),
            show_time=F('shows__show_time__time'),
            language = F('shows__language__name')
            ).values('screen_number',
                     'theatre_name',
                     'show_time',
                     'language'
                     ).distinct()
        screen_data = []
        for i in theatres:
            time = i['show_time']
            screen = str(i['screen_number'])
            theatre = i['theatre_name']
            language = i['language']
            entry = next((entry for entry in screen_data if entry['theatre_name'] == theatre and entry['screen_number'] == screen), None)
            if entry:
                entry['times'].append(time)
            else:
                screen_data.append({'theatre_name': theatre, 'screen_number': screen,'language':language, 'times': [time]})
        return screen_data



    def get_screen_details(self,location ,cinemas,date,screen,movie,times,q=None):
        Q_Base = (
            Q(screen__theatre__theatre_name=cinemas) &
            (Q(screen__theatre__location__place=location) |
            Q(screen__theatre__location__district=location)) &
            Q(screen__screen_number=screen) &
            Q(screen__shows__movies__movie_name=movie) &
            Q(screen__shows__show_dates__dates=date) &
            Q(screen__shows__show_time__time=times) &
            Q(is_approved=True)
            )
        if q :
            Q_Base &= Q(screen__shows__language__name=q) 
        screen_details = screen_seat_details(Q_Base)   
        if screen_details is None:
            return {"data": "No data"}    
        return  screen_details



@permission_classes([AllowAny])
class TheatreSelectionView(APIView):
    location = openapi.Parameter( 'search', in_=openapi.IN_QUERY, description='location', type=openapi.TYPE_STRING, )
    cinemas = openapi.Parameter( 'cinemas', in_=openapi.IN_QUERY, description='theatre', type=openapi.TYPE_STRING, )
    screen = openapi.Parameter( 'screen', in_=openapi.IN_QUERY, description='screen number', type=openapi.TYPE_STRING, )
    date = openapi.Parameter( 'dt', in_=openapi.IN_QUERY, description='date', type=openapi.TYPE_STRING, )
    @swagger_auto_schema(
        tags={
            'users' },
        manual_parameters=(location,cinemas,screen,date),
        operation_description="return Theatre detials , screens , movies by users location",
        responses={
            200:ScreenSeatArrangementChoiceSerailizer,
            404:"Not Found",
            500:"errors"
        }
    )
    def get(self, request):
        location = request.GET.get("search")
        cinemas = request.GET.get("cinemas")
        screen = request.GET.get("screen")
        date = request.GET.get("dt")
        if not cinemas and not screen :
            theatres = TheatreDetails.objects.filter(Q(location__place=location) | Q(location__district=location)).values("theatre_name", "address")
            return Response(theatres, status=status.HTTP_200_OK)
        if date not in Available_dates:
            return Response({"error":"page not found"},status=status.HTTP_404_NOT_FOUND)
        if not screen and date: 
            screens = ScreenDetails.objects.filter((
                Q(theatre__theatre_name=cinemas) & (
                Q(theatre__location__place=location) | 
                Q(theatre__location__district=location) & 
                Q(shows__show_dates__dates=date))
                )).annotate(
                theatre_name=F('theatre__theatre_name'),
                show_time=F('shows__show_time__time'),
                movie_name=F('shows__movies__movie_name'),
                language=F('shows__language__name')).values(
                    "screen_number",
                    'theatre_name',
                    'show_time',
                    'movie_name',
                    'language'
                    )
            return Response({'data':screens,'dates':Available_dates}, status=status.HTTP_200_OK)
        
    
    


class SingleMovieDetailsView(APIView):
    def get (self,request,movie,id):
        movies = MoviesDetails.objects.filter(Q(movie_name=movie) & Q(id=id)).values('movie_name','director','poster').first()
        return Response({'data':movies},status=status.HTTP_200_OK)
        