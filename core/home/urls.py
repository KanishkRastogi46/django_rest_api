from django.urls import path , include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"people", views.PersonViewset, basename='person')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    # path('people/', views.people, name='people'),
    path('colors/', views.colors, name='colors'),
    # path('login/', views.login, name='login'),
    path('person/', views.PersonView.as_view(), name='person'),
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('login/', views.LoginApi.as_view(), name='login'),
]
