from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
# from rest_framework import mixins
# from django.http import JsonResponse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throtlling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPPagination
from rest_framework.renderers import JSONRenderer


class UserReview(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username')
        pk = self.request.query_params.get('pk')
        # if username is not None:
        #     queryset = queryset.filter(purchaser__username=username)
        # return queryset
        if pk is not None:
            return Review.objects.filter(review_user__username=username, id=pk)

        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError(
                "You have already written a review for the watchlist")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    # permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        # watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.get(
            pk=pk)

        review_queryset.watchlist.avg_rating = ((review_queryset.watchlist.avg_rating * 2) -
                                                review_queryset.rating + serializer.validated_data['rating'])/2
        # review_queryset.review_user = review_user
        review_queryset.watchlist.save()
        review_queryset.save()

        serializer.save(pk=pk)

    def perform_destroy(self, serializer):
        pk = self.kwargs.get('pk')

        review_user = self.request.user
        review_queryset = Review.objects.get(
            pk=pk)
        review_queryset.watchlist.avg_rating = (
            review_queryset.watchlist.avg_rating * 2) - review_queryset.rating

        review_queryset.watchlist.number_rating = review_queryset.watchlist.number_rating - 1
        review_queryset.watchlist.save()
        review_queryset.delete()
    #     serializer.save(watchlist=watchlist, review_user=review_user)
    # return super().perform_destroy(instance)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [JSONRenderer]

    # super(StreamPlatformVS, self).initial(request, *args,**kwargs)

# class StreamPlatformVS(viewsets.ViewSet):
#     permission_classes = [IsAdminOrReadOnly]

#     def list(self, request, *args, **kwargs):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(
#             watchlist, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


class StreamPlatformAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response({"Message": "Data Deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

    pagination_class = WatchListCPPagination


class WatchListAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        try:
            movie = WatchList.objects.get(pk=pk)
            movie.delete()
            return Response({"Message": "Data Deleted"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except:
#         return Response({"error": "No data found for given id"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'PUT':
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie.delete()
#         return Response({"Message": "Data Deleted"}, status=status.HTTP_204_NO_CONTENT)
