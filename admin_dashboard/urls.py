from django.urls import path
from .views import (
    UserProfileViewBYAdmin,
    TheatreOwnerRequest, 
    TheatreRequest,
    MovieDetailsAdding
)

urlpatterns = [
    path("users/", UserProfileViewBYAdmin.as_view(), name="users"),
    path("theatreowner/", TheatreOwnerRequest.as_view(), name="theatreowner"),
    path("theatreowner/<int:pk>/", TheatreOwnerRequest.as_view(), name="ownerdetails"),
    path("theatre/", TheatreRequest.as_view(), name="theatres"),
    path("theatre/<int:pk>/", TheatreRequest.as_view(), name="theatre"),
    path("moviedetails/", MovieDetailsAdding.as_view(), name="moviedetails"),
    path("moviedetails/<int:pk>/", MovieDetailsAdding.as_view(), name="moviedetailssingle"),
]
