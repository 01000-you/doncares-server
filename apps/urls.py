from django.urls import path
from . import views

urlpatterns = [
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/create/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('drivers/<int:pk>/update/', views.driver_update, name='driver_update'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),
    path('drivers/search/', views.driver_search, name='driver_search'),
    path('drivers/validation/', views.driver_validate, name='driver_validate'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customers/search/', views.customer_search, name='customer_search'),
    path('customers/validation/', views.customer_validate, name='customer_validate'),

    path('kakao_users/', views.kakao_user_list, name='kakao_user_list'),
    path('kakao_users/create/', views.kakao_user_create, name='kakao_user_create'),
    path('kakao_users/<int:pk>/', views.kakao_user_detail, name='kakao_user_detail'),
    path('kakao_users/<int:pk>/update/', views.kakao_user_update, name='kakao_user_update'),
    path('kakao_users/<int:pk>/delete/', views.kakao_user_delete, name='kakao_user_delete'),
    path('kakao_users/search/', views.kakao_user_search, name='kakao_user_search'),

    path('skills/', views.skill_view, name='skill'),
]
