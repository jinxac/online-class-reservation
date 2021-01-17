from django.urls import path

from .views import ClassViewSet, reserve_class_seat, confirm_class_seat

urlpatterns = [
    path('classes/', ClassViewSet.as_view({
      'get': 'list',
      'post': 'create'
    })),
    path('classes/<int:pk>/', ClassViewSet.as_view({
      'get': 'retrieve',
      'put': 'update',
      'delete': 'destroy'
    })),
    path('classes/reserve-seat/', reserve_class_seat),
    path('classes/confirm-seat/', confirm_class_seat)
]
