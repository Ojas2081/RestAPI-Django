from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformAV, StreamDetailAV, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformVS, UserReview, WatchListGV
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformVS,
                basename='streamplatform')

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="movie-list"),
    path('<int:pk>/', WatchDetailAV.as_view(), name="movie-detail"),
    path('list2/', WatchListGV.as_view(), name="movie-detail"),

    path('', include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name="stream-platform"),
    # path('stream/<int:pk>/', StreamDetailAV.as_view(), name="stream-detail"),


    # path('review/', ReviewList.as_view(), name="review-list"),
    path('<int:pk>/reviews/', ReviewList.as_view(), name="review-list"),

    path('<int:pk>/review-create/',
         ReviewCreate.as_view(), name="review-create"),


    # path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),

    path('review/', UserReview.as_view(), name="user-review-detail"),
]
