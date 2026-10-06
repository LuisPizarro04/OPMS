from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import routers

from .views import (
    VentaViewSet,
    EtapasViewSet,
    VentaEtapaViewSet,
    CampoEtapaViewSet,
    ValoresEtapaViewSet,
)

routers = routers.DefaultRouter()

# --- Registros para DRF ---
routers.register(r"Ventas", VentaViewSet)
routers.register(r"Etapas", EtapasViewSet)
routers.register(r"VentaEtapas", VentaEtapaViewSet)
routers.register(r"CamposEtapas", CampoEtapaViewSet)
routers.register(r"ValoresEtapas", ValoresEtapaViewSet)

urlpatterns = [
    path("ventas/", ListaVentasView.as_view(), name="lista_ventas"),
    # El endpoint para modificar etapas lo haremos luego:
    path(
        "ventas/<int:venta_id>/etapas/", EtapasVentaView.as_view(), name="editar_etapas"
    ),
    path("informe_pagos/<int:id_venta>/", informe_pagos_venta, name="informe_pagos"),
    # path('informe_pagos_print/<int:id_venta>/', login_required(informe_pagos_venta_print), name='informe_pagos_print'),
    path(
        "pagos_invoice_pdf/<int:id_venta>/",
        login_required(PagosInvoicePdf.as_view()),
        name="pagos_invoice_pdf",
    ),
    path("fpm_venta/<int:id_venta>/", login_required(fpm_venta), name="fpm_venta"),
    path(
        "fpm_venta_print/<int:id_venta>/",
        login_required(Fpm_VentaPdf.as_view()),
        name="fpm_venta_print",
    ),
    path(
        "entrega_docven/<int:id_venta>/",
        login_required(entrega_documentos_venta),
        name="entrega_docven",
    ),
    path(
        "entrega_docven_print/<int:id_venta>/",
        login_required(EntregaDocumentoPdf.as_view()),
        name="entrega_docven_print",
    ),
    path(
        "ccn/<int:id_venta>/", login_required(carta_cierre_negocios_venta), name="ccn"
    ),
    path(
        "ccn_print/<int:id_venta>/",
        login_required(CierreNegociopdf.as_view()),
        name="ccn_print",
    ),
    path("memoggoo/<int:id_venta>/", login_required(memo_ggoo), name="memoggoo"),
    path(
        "memoggoo_print/<int:id_venta>/",
        login_required(MemoGgooPdf.as_view()),
        name="memoggoo_print",
    ),
    path(
        "cartaoferta/<int:id_venta>/", login_required(carta_oferta), name="cartaoferta"
    ),
    path(
        "cartaoferta_print/<int:id_venta>/",
        login_required(CartaOfertaPdf.as_view()),
        name="cartaoferta_print",
    ),
    path("", include(routers.urls)),
    path(
        "ventas/<int:venta_id>/etapas/",
        EtapasVentaView.as_view(),
        name="gestvent_editar_etapas",
    ),
]
