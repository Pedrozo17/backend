from django.urls import path
from .views import TareasAPIView
from .views_auth import RegistroAPIView, LoginAPIView
from .views_perfil import PerfilImagenAPIView, PerfilAPIView
from .views_chat import ChatHistorialAPIView

urlpatterns = [
    path('auth/registro/', RegistroAPIView.as_view(), name='api_registro'),
    path('auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('tareas/', TareasAPIView.as_view(), name='api_tareas'),
    path('tareas/<str:tarea_id>/', TareasAPIView.as_view(), name='api_tarea_detalle'),
    path('perfil/foto/', PerfilImagenAPIView.as_view(),name='api_perfil_foto'),
    path('perfil/', PerfilAPIView.as_view()),
    path('chat/historial/', ChatHistorialAPIView.as_view(), name= 'api_chat_historial'),
]