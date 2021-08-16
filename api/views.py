from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from .serializers import UserSerializer, PortfolioSerializer, PromoSerializer
from app.models import User, Portfolio, Promo


@permission_classes([IsAuthenticated])
class userAdd(APIView):

    def post(self, request, *args, **kwargs):
        renderer_classes = [JSONRenderer]
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class usersList(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')


@permission_classes([IsAuthenticated])
class portfoliosList(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Portfolio.objects.all()
        serializer = PortfolioSerializer(queryset, many=True)

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')

@permission_classes([IsAuthenticated])
class portfolioDetail(APIView):
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
class userGet(APIView):

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
