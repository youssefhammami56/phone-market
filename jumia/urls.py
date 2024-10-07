from django.urls import path
from . import views
urlpatterns = [
 path('', views.jumia_data, name='jumia_data'),
   path('/detailsPhone/<str:name>', views.detailsPhone, name='detailsPhone'),
]