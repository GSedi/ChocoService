from django.urls import path
from main import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('clients/', views.ClientList.as_view(), name='client_list'),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name='client_detail'),
    path('partners/', views.PartnerList.as_view(), name='partner_list'),
    path('partners/<int:pk>/', views.PartnerDetail.as_view(), name='partner_detail'),
    path('salons/', views.SalonList.as_view(), name='salon_list'),
    path('salons/<int:pk>/', views.SalonDetail.as_view(), name='salon_detail'),
    path('salons/<int:salon_id>/masters/', views.MasterList.as_view(), name='master_list'),
    path('masters/<int:pk>/', views.MasterDetail.as_view(), name='master_detail'),
    path('masterservices/', views.MasterServiceList.as_view(), name='master_service_list'),
    path('masterservices/<int:pk>/', views.MasterServiceDetail.as_view(), name='master_service_detail'),

    path('services/<int:pk>/', views.ServiceDetail.as_view()),
    path('salons/<int:salon_id>/services/', views.ServiceList.as_view(), name='salon_services'),
    path('salons/<int:salon_id>/masterservices/', views.MasterServiceList.as_view(), name='salon_naster_services'),
    
    path('services/<int:service_id>/masterservices/', views.CustomMasterServiceList.as_view(), name='service_master_services'),
    path('masters/<int:master_id>/masterservices/', views.CustomMasterServiceList.as_view(), name='master_master_services'),

    path('orders/', views.OrderCreate.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('partners/<int:partner_id>/orders/', views.OrderList.as_view()),
    path('salons/<int:salon_id>/orders/', views.OrderList.as_view()),
    path('clients/<int:client_id>/orders/', views.OrderList.as_view()),
    path('masters/<int:master_id>/orders/', views.OrderList.as_view()),

    path('partners/<int:partner_id>/salons/', views.SalonList.as_view()),

    path('filter/', views.filter, name='filter_service_time'),
    path('filter/', views.filter, name='salon_masters_free_filter'),
    path('filter/', views.filter, name='master_filter'),


    path('salons/<int:salon_id>/comments/', views.CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),

    path('masters/<int:pk>/rate/', views.SetMasterRating.as_view()),
    path('clients/<int:pk>/rate/', views.SetClienRating.as_view()),
    path('salons/<int:pk>/rate/', views.SetSalonRating.as_view()),

    # path('update-flag/<int:pk>/', views.UpdateOrderFlag.as_view(), name='update_flag'),
    # path('update-master-time/<int:pk>/', views.update_master_time, name='update_master_time'),
]


urlpatterns = format_suffix_patterns(urlpatterns)