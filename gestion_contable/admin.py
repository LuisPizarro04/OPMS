from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action
from .models import Bancos, CategoriaPago, FormaPago, Pagos, ValorUf
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from unfold.decorators import action

from .forms import SincronizarUfForm
from .services.uf_service import sincronizar_uf as sincronizar_uf_service


# ============================================================
# BANCOS
# ============================================================

@admin.register(Bancos)
class BancoAdmin(ModelAdmin):
    list_display = (
        "id_banco",
        "nombre_banco",
    )

    search_fields = (
        "nombre_banco",
    )

    ordering = (
        "nombre_banco",
    )

    list_per_page = 25


# ============================================================
# CATEGORÍAS DE PAGO
# ============================================================

@admin.register(CategoriaPago)
class CategoriaPagoAdmin(ModelAdmin):
    list_display = (
        "id_categoria_pago",
        "nombre_categoria_pago",
    )

    search_fields = (
        "nombre_categoria_pago",
    )

    ordering = (
        "id_categoria_pago",
    )

    list_per_page = 25


# ============================================================
# FORMAS DE PAGO
# ============================================================

@admin.register(FormaPago)
class FormaPagoAdmin(ModelAdmin):
    list_display = (
        "id_forma_pago",
        "nombre_forma_pago",
    )

    search_fields = (
        "nombre_forma_pago",
    )

    ordering = (
        "id_forma_pago",
    )

    list_per_page = 25


# ============================================================
# INLINE DE PAGOS
# Se utiliza dentro de VentaAdmin
# ============================================================

class PagosInline(TabularInline):
    model = Pagos
    extra = 0

    fields = (
        "estado_pago",
        "id_categoria_pago",
        "id_forma_pago",
        "id_banco",
        "num_documento",
        "fecha_real_pago",
        "monto_pago",
        "uf_pago",
    )

    readonly_fields = (
        "uf_pago",
    )

    show_change_link = True


# ============================================================
# PAGOS
# ============================================================

@admin.register(Pagos)
class PagoAdmin(ModelAdmin):

    # --------------------------------------------------------
    # LISTADO
    # --------------------------------------------------------

    list_display = (
        "id_pago",
        "id_venta",
        "estado_pago",
        "id_categoria_pago",
        "id_forma_pago",
        "fecha_real_pago",
        "format_monto_pago",
        "format_valor_uf",
        "format_uf_pago",
    )

    list_display_links = (
        "id_pago",
        "id_venta",
    )

    list_filter = (
        "estado_pago",
        "id_categoria_pago",
        "id_forma_pago",
        "id_banco",
    )

    search_fields = (
        "num_documento",
        "observacion_pago",
        "id_venta__id_venta",
        "id_venta__id_cliente__rut_cliente",
        "id_venta__id_propiedad__numero_propiedad",
    )

    ordering = (
        "-fecha_real_pago",
        "-id_pago",
    )

    date_hierarchy = "fecha_real_pago"

    list_per_page = 25

    list_select_related = (
        "id_venta",
        "id_venta__id_cliente",
        "id_venta__id_propiedad",
        "id_forma_pago",
        "id_categoria_pago",
        "id_banco",
    )

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    readonly_fields = (
        "uf_pago",
    )

    fieldsets = (
        (
            "Información del pago",
            {
                "fields": (
                    ("id_venta", "estado_pago"),
                    ("id_categoria_pago", "id_forma_pago"),
                    ("id_banco", "num_documento"),
                ),
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    ("fecha_registro_pago", "fecha_real_pago"),
                ),
            },
        ),
        (
            "Montos",
            {
                "fields": (
                    ("monto_pago", "uf_pago"),
                ),
                "description": (
                    "El monto en UF se calcula automáticamente utilizando "
                    "el valor UF correspondiente a la fecha contable."
                ),
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "observacion_pago",
                ),
            },
        ),
    )

    # --------------------------------------------------------
    # COLUMNAS CALCULADAS
    # --------------------------------------------------------

    @admin.display(
        description="Monto",
        ordering="monto_pago",
    )
    def format_monto_pago(self, obj):
        if obj.monto_pago is None:
            return "-"

        return f"${obj.monto_pago:,.0f}".replace(",", ".")

    @admin.display(
        description="Monto UF",
        ordering="uf_pago",
    )
    def format_uf_pago(self, obj):
        # Si existe monto UF, lo mostramos normalmente
        if obj.uf_pago is not None:
            return f"{obj.uf_pago:,.2f}".replace(
                ",", "X"
            ).replace(
                ".", ","
            ).replace(
                "X", "."
            )

        # Si está contabilizado pero no tiene UF,
        # existe una inconsistencia
        if obj.estado_pago == "Contabilizado" and obj.fecha_real_pago:
            return format_html(
                '<span title="Pago contabilizado sin monto UF calculado">'
                '⚠ Sin calcular'
                '</span>'
            )

        # Para pagos pendientes es normal no tener monto UF
        return "-"

    @admin.display(description="Valor UF")
    def format_valor_uf(self, obj):
        if not obj.fecha_real_pago:
            return "-"

        try:
            uf = ValorUf.objects.get(fecha_registro=obj.fecha_real_pago)
            return f"${uf.valor_uf:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except ValorUf.DoesNotExist:
            return "-"


# ============================================================
# VALOR UF
# ============================================================

@admin.register(ValorUf)
class ValorUfAdmin(ModelAdmin):

    list_display = (
        "fecha_registro",
        "format_valor_uf",
    )

    list_display_links = (
        "fecha_registro",
    )

    list_filter = (
        "fecha_registro",
    )

    search_fields = (
        "fecha_registro",
    )

    ordering = (
        "-fecha_registro",
    )

    date_hierarchy = "fecha_registro"

    list_per_page = 31

    actions_list = [
        "sincronizar_uf",
    ]

    @admin.display(
        description="Valor UF",
        ordering="valor_uf",
    )
    def format_valor_uf(self, obj):
        if obj.valor_uf is None:
            return "-"

        return f"${obj.valor_uf:,.2f}".replace(
            ",", "X"
        ).replace(
            ".", ","
        ).replace(
            "X", "."
        )

    @action(description="Sincronizar UF")
    def sincronizar_uf(self, request):

        if request.method == "POST":
            form = SincronizarUfForm(request.POST)

            if form.is_valid():
                fecha_inicio = form.cleaned_data["fecha_inicio"]
                fecha_fin = form.cleaned_data["fecha_fin"]

                try:
                    resultados = sincronizar_uf_service(
                        fecha_inicio,
                        fecha_fin,
                    )

                    creados = sum(
                        1 for resultado in resultados
                        if resultado["creado"]
                    )

                    actualizados = len(resultados) - creados

                    self.message_user(
                        request,
                        (
                            f"UF sincronizada correctamente. "
                            f"{creados} registros creados y "
                            f"{actualizados} actualizados."
                        ),
                        messages.SUCCESS,
                    )

                    return redirect(
                        "admin:gestion_contable_valoruf_changelist"
                    )

                except Exception as error:
                    self.message_user(
                        request,
                        f"Error al sincronizar UF: {error}",
                        messages.ERROR,
                    )

        else:
            form = SincronizarUfForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Sincronizar UF",
            "form": form,
            "opts": self.model._meta,
        }

        return TemplateResponse(
            request,
            "admin/gestion_contable/sincronizar_uf.html",
            context,
        )