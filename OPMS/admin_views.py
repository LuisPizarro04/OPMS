from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse


@staff_member_required
def configuracion(request):
    context = {
        **admin.site.each_context(request),
        "title": "Administración",

        "urls": {
            # Empresa
            "empresas": reverse(
                "admin:gestion_empresa_empresa_changelist"
            ),

            # Clientes
            "nacionalidades": reverse(
                "admin:gestion_clientes_nacionalidade_changelist"
            ),
            "areas_profesion": reverse(
                "admin:gestion_clientes_areaprofesion_changelist"
            ),
            "profesiones": reverse(
                "admin:gestion_clientes_profesione_changelist"
            ),

            # Finanzas
            "categorias_pago": reverse(
                "admin:gestion_contable_categoriapago_changelist"
            ),
            "formas_pago": reverse(
                "admin:gestion_contable_formapago_changelist"
            ),

            # Postventa
            "recintos": reverse(
                "admin:gestion_postventa_recinto_changelist"
            ),
            "lugares": reverse(
                "admin:gestion_postventa_lugar_changelist"
            ),
            "items": reverse(
                "admin:gestion_postventa_item_changelist"
            ),
            "problemas": reverse(
                "admin:gestion_postventa_problema_changelist"
            ),
            "especialidades": reverse(
                "admin:gestion_postventa_especialidad_changelist"
            ),
            "causas": reverse(
                "admin:gestion_postventa_causa_changelist"
            ),
            "alcances": reverse(
                "admin:gestion_postventa_alcanceresponsabilidad_changelist"
            ),

            # Seguridad
            "usuarios": reverse(
                "admin:auth_user_changelist"
            ),
            "grupos": reverse(
                "admin:auth_group_changelist"
            ),
            "etapas": reverse(
                "admin:gestion_escrituracion_etapas_changelist"
            ),
        },
    }

    return render(
        request,
        "admin/configuracion.html",
        context,
    )