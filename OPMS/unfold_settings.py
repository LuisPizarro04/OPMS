from django.urls import reverse_lazy

from django.urls import reverse_lazy


# ============================================================
# PERMISOS
# ============================================================

def has_perm(permission):
    """
    Retorna un callback compatible con Unfold.
    El elemento del sidebar solo se muestra si el usuario
    posee el permiso indicado.
    """

    def check(request):
        return request.user.has_perm(permission)

    return check


UNFOLD = {

    # ==============================
    # IDENTIDAD
    # ==============================

    "SITE_TITLE": "SARAMS",
    "SITE_HEADER": "SARAMS",
    "SITE_SUBHEADER": "Administra Operaciones",

    "SITE_SYMBOL": "apartment",

    # ==============================
    # COMPORTAMIENTO
    # ==============================

    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "SHOW_BACK_BUTTON": True,

    # ==============================
    # COLORES
    # ==============================

    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,

        "navigation": [

            # ====================================================
            # PRINCIPAL
            # ====================================================
            {
                "title": "",
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": "Inicio",
                        "icon": "home",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Clientes",
                        "icon": "groups",
                        "link": reverse_lazy(
                            "admin:gestion_clientes_cliente_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_clientes.view_cliente"
                        ),
                    },
                ],
            },

            # ====================================================
            # PROPIEDADES
            # ====================================================
            {
                "title": "Propiedades",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Condominios",
                        "icon": "apartment",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_condominio_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_condominio"
                        ),
                    },
                    {
                        "title": "Etapas",
                        "icon": "domain",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_etapa_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_etapa"
                        ),
                    },
                    {
                        "title": "Sub Etapas",
                        "icon": "account_tree",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_subetapa_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_subetapa"
                        ),
                    },
                    {
                        "title": "Torres",
                        "icon": "location_city",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_torre_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_torre"
                        ),
                    },
                    {
                        "title": "Modelos",
                        "icon": "view_in_ar",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_modelo_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_modelo"
                        ),
                    },
                    {
                        "title": "Propiedades",
                        "icon": "home_work",
                        "link": reverse_lazy(
                            "admin:gestion_propiedad_propiedade_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_propiedad.view_propiedade"
                        ),
                    },
                ],
            },

            # ====================================================
            # VENTAS
            # ====================================================
            {
                "title": "Ventas",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Ventas",
                        "icon": "real_estate_agent",
                        "link": reverse_lazy(
                            "admin:gestion_escrituracion_venta_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_escrituracion.view_venta"
                        ),
                    },
                ],
            },

            # ====================================================
            # FINANZAS
            # ====================================================
            {
                "title": "Finanzas",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Pagos",
                        "icon": "payments",
                        "link": reverse_lazy(
                            "admin:gestion_contable_pagos_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_contable.view_pagos"
                        ),
                    },
                    {
                        "title": "Bancos",
                        "icon": "account_balance",
                        "link": reverse_lazy(
                            "admin:gestion_contable_bancos_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_contable.view_bancos"
                        ),
                    },
                    {
                        "title": "Valor UF",
                        "icon": "currency_exchange",
                        "link": reverse_lazy(
                            "admin:gestion_contable_valoruf_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_contable.view_valoruf"
                        ),
                    },
                ],
            },

            # ====================================================
            # POSTVENTA
            # ====================================================
            {
                "title": "Postventa",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Requerimientos",
                        "icon": "construction",
                        "link": reverse_lazy(
                            "admin:gestion_postventa_requerimientopostventa_changelist"
                        ),
                        "permission": has_perm(
                            "gestion_postventa.view_requerimientopostventa"
                        ),
                    },
                ],
            },

            # ====================================================
            # REPORTES
            # ====================================================
            {
                "title": ("Gestión Operacional"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": ("Hitos Operacionales"),
                        "icon": "account_tree",
                        "link": reverse_lazy("lista_ventas"),
                    },
                ],
            },

            # ====================================================
            # ADMINISTRACIÓN
            # ====================================================
            {
                "title": "",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Administración",
                        "icon": "settings",
                        "link": reverse_lazy("admin_configuracion"),
                    },
                ],
            },
        ],
    },

}
