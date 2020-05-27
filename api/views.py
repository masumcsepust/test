
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie,Rating
from .serializers import MovieSerializer,RatingSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
        queryset=User.objects.all()
        serializer_class=UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
        queryset=Movie.objects.all()
        serializer_class=MovieSerializer
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        @action(detail=True,methods=['POST'])
        def rate_movie(self,request,pk=None):
                if 'stars' in request.data:
                        movie=Movie.objects.get(id=pk)
                        stars=request.data['stars']
                        user=request.user
                        print(user)
                        try:
                                rating=Rating.objects.get(movie=movie.id,user=user.id)
                                rating.stars=stars
                                rating.save()
                                serializer=RatingSerializer(rating,many=False)
                                response = {'Message': 'Rating Updated', 'result':serializer.data}
                                return Response(response, status=status.HTTP_200_OK)
                        except:
                                rating=Rating.objects.create(user=user,movie=movie,stars=stars)
                                serializer = RatingSerializer(rating, many=False)
                                response = {'Message': 'Rating Created', 'result': serializer.data}
                                return Response(response, status=status.HTTP_200_OK)


                else:
                        response={'Message':'You need to provide stars'}
                        return Response(response,status=status.HTTP_404_NOT_FOUND)




class RatingViewSet(viewsets.ModelViewSet):
        queryset=Rating.objects.all()
        serializer_class=RatingSerializer
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        def update(self, request, *args, **kwargs):
                response = {'Message': 'You cant update ratings like that'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        def create(self, request, *args, **kwargs):
                response = {'Message': 'You cant create ratings like that'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)



