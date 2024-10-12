from django.urls import path
from .views import event_list, event_create, event_update, event_delete, LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # This is the login view
    path('list/', event_list, name='event_list'),  # Event list URL
    path('create/', event_create, name='event_create'),
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
