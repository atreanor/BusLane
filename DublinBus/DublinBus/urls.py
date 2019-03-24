from django.contrib import admin
from django.urls import include, path
from DublinBusTest import views
from django.conf.urls.static import static
from django.conf import settings 

# Code below routes the different aspects of the webpage to the required URL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DublinBusTest.urls')),
   # path('api/get_routes_stops/', views.get_routes_stops, name='get_routes_stops'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
