"""
URL configuration for OPMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from gestion_escrituracion import views
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import IsAuthenticated
from OPMS.admin_views import configuracion
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "", RedirectView.as_view(url="/admin/", permanent=True)
    ),  # Redirige la raíz al admin
    path(
        "admin/configuracion/",
        configuracion,
        name="admin_configuracion",
    ),
    path("", RedirectView.as_view(url="/admin/", permanent=True)),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/configuracion/",
        configuracion,
        name="admin_configuracion",
    ),
    # Recuperación de contraseña
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "admin/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "admin/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("admin/", admin.site.urls),
    path("ventas/", include("gestion_escrituracion.urls")),
    # path('test_datatables/', views.test_datatables, name='test_datatables'),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/clientes", include("gestion_clientes.urls")),
    path("api/v1/empresas", include("gestion_empresa.urls")),
    path("api/v1/postventa", include("gestion_postventa.urls")),
    path("api/v1/gestvent", include("gestion_escrituracion.urls")),
    path("api/v1/propiedad", include("gestion_propiedad.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(
            permission_classes=[IsAuthenticated], url_name="schema"
        ),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
