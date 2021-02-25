from django.urls import path


from .views import registration, auth, activate, UserProfile_view

urlpatterns = [
    path('register/',registration),
    path('login/', auth, name='login'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('profile/',UserProfile_view,name='profile'),
]

