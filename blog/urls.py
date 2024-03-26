from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list_name'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail_name'),
    path('create/', views.PostCreateView.as_view(), name='show_form_add_name'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update_view_name'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete_view_name'),
]
