from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # <int:qid> is argument passed to view by the url
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:qid>/vote/', views.vote, name='vote'),
]
