from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'polls'
urlpatterns = [
    path('', views.AuthenticationView, name='authentication'),
    path('register', views.Register.as_view(), name='register'),
    path('edit/<int:id>', views.edit, name='vote'),
    path('delete/<int:id>', views.delete, name='vote'),
    path('account', views.account, name='account'),
    path('question/', views.IndexView.as_view(), name='index'),
    path('<int:question_id>/<int:user_id>/', views.detail, name='detail'),
    path('<int:question_id>/<int:user_id>/results/', views.results, name='results'),
    path('<int:question_id>/<int:user_id>/vote/', views.vote, name='vote'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)