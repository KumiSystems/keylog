from django.urls import path, include

urlpatterns = [
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('', include('frontend.urls', "frontend")),
]
