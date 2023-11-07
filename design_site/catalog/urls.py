from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ViewRequests, RequestCreate

urlpatterns = [
    path('', ViewRequests.as_view(), name='index'),
    path('register/', views.registration, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request_form/', RequestCreate.as_view(), name='request_form'),
    path('my_requests/', views.user_requests, name='user_requests'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('admin/requests/', views.admin_requests, name='admin_requests'),
    path('create_category/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.requests_by_category, name='requests_by_category'),
    path('admin/category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
