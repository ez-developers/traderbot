from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from .serializers import UserSerializer, PortfolioSerializer, PromoSerializer, VideoLessonSerializer
from app.models import User, Portfolio, Promo, VideoLesson


@permission_classes([IsAuthenticated])
class UserAdd(APIView):

    def post(self, request, *args, **kwargs):
        renderer_classes = [JSONRenderer]
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserGet(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, *args, **kwargs):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, content_type='application/json')

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UsersList(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')


@permission_classes([IsAuthenticated])
class PromoList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Promo.objects.all()
        serializer = PromoSerializer(queryset, many=True)

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
    
    def post(self, request, *args, **kwargs):
        serializer = PromoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class PromoDetail(APIView):
    def get_object(self, pk):
        try:
            return Promo.objects.get(pk=pk)
        except Promo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None, *args, **kwargs):
        promo = self.get_object(pk)
        serializer = PromoSerializer(promo)
        return Response(serializer.data, content_type='application/json')

    def put(self, request, pk, format=None):
        promo = self.get_object(pk)
        serializer = PromoSerializer(promo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class PortfoliosList(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Portfolio.objects.all()
        serializer = PortfolioSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')


@permission_classes([IsAuthenticated])
class PortfolioDetail(APIView):
    def get_object(self, pk):
        try:
            return Portfolio.objects.get(pk=pk)
        except:
            return Portfolio.DoesNotExist

    def get(self, request, pk, format=None, *args, **kwargs):
        porfolio = self.get_object(pk)
        serializer = PortfolioSerializer(porfolio)
        return Response(serializer.data, content_type='application/json')

    def put(self, request, pk, format=None):
        portfolio = self.get_object(pk)
        serializer = PortfolioSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class VideoLessonList(APIView):

    def get(self, request, *args, **kwargs):
        queryset = VideoLesson.objects.all()
        serializer = VideoLessonSerializer(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')


@permission_classes([IsAuthenticated])
class VideoLessonDetail(APIView):
    def get_object(self, pk):
        try:
            return VideoLesson.objects.get(pk=pk)
        except:
            return VideoLesson.DoesNotExist

    def get(self, request, pk, format=None, *args, **kwargs):
        video = self.get_object(pk)
        serializer = VideoLessonSerializer(video)
        return Response(serializer.data, content_type='application/json')

    def put(self, request, pk, format=None):
        video = self.get_object(pk)
        serializer = VideoLessonSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
