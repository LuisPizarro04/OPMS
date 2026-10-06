# Create your views here.
import os
# from unittest.mock import right
from django.utils import timezone as django_timezone
from aiohttp import request
from aiohttp import request
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.sites import site
from xhtml2pdf import pisa
from OPMS import settings
from gestion_propiedad.models import Propiedade
from .models import Venta, VentaEtapa, CampoEtapa, ValoresEtapa
from gestion_contable.models import Pagos, ValorUf
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, redirect
from datetime import datetime, timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import (Venta, Etapas, VentaEtapa, CampoEtapa, ValoresEtapa)
from .serializers import (
    VentaSerializer,
    EtapasSerializer,
    VentaEtapaSerializer,
    CampoEtapaSerializer,
    ValoresEtapaSerializer
)
from django.db.models import Prefetch, Q
from gestion_propiedad.models import Propiedade, Condominio
fecha_hoy = datetime.now()


class ListaVentasView(TemplateView):
    template_name = "ventas/listado_ventas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(site.each_context(self.request))

        tipo_venta = self.request.GET.get("tipo_venta", "").strip()
        ejecutivo = self.request.GET.get("ejecutivo", "").strip()
        estado_hitos = self.request.GET.get("estado_hitos", "").strip()
        buscar = self.request.GET.get("buscar", "").strip()
        condominio = self.request.GET.get("condominio", "").strip()

        ventas = (
            Venta.objects.select_related(
                "id_cliente",
                "id_propiedad",
            )
            .prefetch_related(
                Prefetch(
                    "ventaetapa_set",
                    queryset=VentaEtapa.objects.select_related("id_etapa"),
                    to_attr="hitos_operacionales",
                )
            )
            .filter(estado_venta="Promesa")
        )

        # Condominio
        if condominio:
            ventas = ventas.filter(
                id_propiedad__condominio_id=condominio)
        # Tipo de venta
        if tipo_venta:
            ventas = ventas.filter(tipo_venta=tipo_venta)

        # Ejecutivo
        if ejecutivo:
            ventas = ventas.filter(ejecutivo=ejecutivo)

        # Búsqueda general
        if buscar:
            ventas = ventas.filter(
                Q(id_cliente__nombres_1__icontains=buscar)
                | Q(id_cliente__nombres_2__icontains=buscar)
                | Q(id_cliente__apellidos_1__icontains=buscar)
                | Q(id_cliente__apellidos_2__icontains=buscar)
                | Q(id_cliente__rut_cliente__icontains=buscar)
                | Q(id_propiedad__numero_propiedad__icontains=buscar)
            )

        # Evaluamos el queryset antes de calcular los estados
        ventas = list(ventas)

        for venta in ventas:
            hitos = venta.hitos_operacionales

            venta.total_hitos = len(hitos)

            venta.hitos_completados = sum(
                1 for hito in hitos if hito.fecha_fin
            )

            venta.hitos_en_proceso = sum(
                1
                for hito in hitos
                if hito.fecha_inicio and not hito.fecha_fin
            )

            venta.hitos_pendientes = sum(
                1
                for hito in hitos
                if not hito.fecha_inicio and not hito.fecha_fin
            )

        # Filtro operacional
        if estado_hitos == "en_proceso":
            ventas = [
                venta
                for venta in ventas
                if venta.hitos_en_proceso > 0
            ]

        elif estado_hitos == "sin_iniciar":
            ventas = [
                venta
                for venta in ventas
                if venta.hitos_pendientes == venta.total_hitos
            ]

        elif estado_hitos == "completados":
            ventas = [
                venta
                for venta in ventas
                if venta.total_hitos > 0
                and venta.hitos_completados == venta.total_hitos
            ]

        context["ventas"] = ventas
        context["condominios"] = Condominio.objects.all().order_by("alias_condominio")

        # Opciones para los filtros
        context["ejecutivos"] = (
            Venta.objects.filter(estado_venta="Promesa")
            .exclude(ejecutivo__isnull=True)
            .exclude(ejecutivo="")
            .values_list("ejecutivo", flat=True)
            .distinct()
            .order_by("ejecutivo")
        )

        # Mantener selección después de filtrar
        context["filtros"] = {
            "condominio": condominio,
            "tipo_venta": tipo_venta,
            "ejecutivo": ejecutivo,
            "estado_hitos": estado_hitos,
            "buscar": buscar,
        }

        return context
    


class EtapasVentaView(View):
    template_name = 'ventas/editar_etapas.html'

    def get(self, request, venta_id):
        venta = get_object_or_404(Venta, id_venta=venta_id)
        etapas = VentaEtapa.objects.filter(id_venta=venta).select_related('id_etapa')

        campos_etapas = {
            ve.id_etapa.id_etapa: CampoEtapa.objects.filter(id_etapa=ve.id_etapa)
            for ve in etapas
        }

        valores_etapas = {
            ve.id_etapa.id_etapa: list(ValoresEtapa.objects.filter(id_venta_etapa=ve))
            for ve in etapas
        }

        context = {
            'venta': venta,
            'etapas': etapas,
            'campos_etapas': campos_etapas,
            'valores_etapas': valores_etapas,
            'title': f'Editar etapas de la venta #{venta.id_venta}',
            **site.each_context(request),
        }

        return render(request, self.template_name, context)

    def post(self, request, venta_id):
        venta = get_object_or_404(Venta, id_venta=venta_id)
        etapas = VentaEtapa.objects.filter(id_venta=venta).select_related('id_etapa')
        accion = request.POST.get("accion")
        venta_etapa_id = request.POST.get("venta_etapa_id")
        
        if accion == "iniciar_hito" and venta_etapa_id:
            venta_etapa = get_object_or_404(
                VentaEtapa,
                id_venta_etapa=venta_etapa_id,
                id_venta=venta
            )
            if not venta_etapa.fecha_inicio:
                venta_etapa.fecha_inicio = django_timezone.localdate()
                venta_etapa.save(update_fields=["fecha_inicio"])
                messages.success(
                    request,
                    f"Hito {venta_etapa.id_etapa.alias_etapa} iniciado correctamente."
                )
            return redirect(request.path)       

        if accion == "completar_hito" and venta_etapa_id:
            venta_etapa = get_object_or_404(
                VentaEtapa,
                id_venta_etapa=venta_etapa_id,
                id_venta=venta,
            )
            
            # Guardar los campos enviados antes de validar
            campos_etapa = CampoEtapa.objects.filter(
                id_etapa=venta_etapa.id_etapa
            )

            for campo in campos_etapa:
                field_name = f"campo_{campo.id_campo_etapa}"

                if field_name in request.POST:
                    valor = request.POST.get(field_name, "").strip()

                    ValoresEtapa.objects.update_or_create(
                        id_venta_etapa=venta_etapa,
                        id_campo_etapa=campo,
                        defaults={
                            "valor_campo": valor
                        }
                    )

            # Campos obligatorios configurados para este hito
            campos_obligatorios = CampoEtapa.objects.filter(
                id_etapa=venta_etapa.id_etapa,
                obligatorio=True,
            )

            campos_faltantes = []

            for campo in campos_obligatorios:
                valor = ValoresEtapa.objects.filter(
                    id_venta_etapa=venta_etapa,
                    id_campo_etapa=campo,
                ).first()

                if not valor or not valor.valor_campo or not valor.valor_campo.strip():
                    campos_faltantes.append(campo.nombre_campo)

            # No permitir completar si faltan campos obligatorios
            if campos_faltantes:
                messages.error(
                    request,
                    "No se puede completar el hito. "
                    "Complete los campos obligatorios: "
                    + ", ".join(campos_faltantes)
                    + ".",
                )

                return redirect(request.path)

            # Completar hito
            if venta_etapa.fecha_inicio and not venta_etapa.fecha_fin:
                venta_etapa.fecha_fin = django_timezone.localdate()
                venta_etapa.save(update_fields=["fecha_fin"])

                messages.success(
                    request,
                    f"Hito {venta_etapa.id_etapa.alias_etapa} completado correctamente.",
                )

            return redirect(request.path)
        
        for etapa in etapas:
            campos = CampoEtapa.objects.filter(id_etapa=etapa.id_etapa)
            for campo in campos:
                field_name = f"campo_{campo.id_campo_etapa}"
                valor = request.POST.get(field_name)
                if valor is not None:
                    valor_etapa, created = ValoresEtapa.objects.get_or_create(
                        id_venta_etapa=etapa,
                        id_campo_etapa=campo,
                        defaults={'valor_campo': valor}
                    )
                    if not created:
                        valor_etapa.valor_campo = valor
                        valor_etapa.save()

        messages.success(request, "Los datos fueron guardados correctamente.")
        return redirect(request.path)


from django.shortcuts import render


def test_datatables(request):
    return render(request, 'ventas/test_datatable.html')


from django.db.models import Sum


def informe_pagos_venta(request, id_venta):
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    total_pagado = datos.aggregate(total=Sum('monto_pago'))['total'] or 0
    total_pagado_uf = datos.filter(estado_pago="Contabilizado") \
                          .aggregate(total=Sum('uf_pago'))['total'] or 0

    # ✅ Total pagado en categoría "Detalle Pie"
    total_detalle_pie = datos.filter(id_categoria_pago__nombre_categoria_pago="Detalle Pie") \
                            .aggregate(total=Sum('uf_pago'))['total'] or 0
    # Obtener valor UF por cada pago
    valores_uf_por_pago = {}
    for pago in datos:
        if pago.estado_pago == "Contabilizado":
            try:
                valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
            except ValorUf.DoesNotExist:
                valores_uf_por_pago[pago.id_pago] = None
        else:
            valores_uf_por_pago[pago.id_pago] = None

    # ✅ Extraer el valor inicial de la propiedad (asumiendo 1 resultado)
    valor_inicial_propiedad = None
    if datos_venta.exists():
        valor_inicial_propiedad = datos_venta[0].id_propiedad.valor_inicial_propiedad
        bono_pie = datos_venta[0].bono_pie or 0
        precio_final = datos_venta[0].precio_venta
        credito_hipotecario = datos_venta[0].credito_hipotecario or 0

        total = valor_inicial_propiedad - bono_pie
        saldo_pie = (
                valor_inicial_propiedad
                - bono_pie
                - credito_hipotecario
                - total_detalle_pie
        )

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'total_pagado': total_pagado,
        'total_pagado_uf': total_pagado_uf,
        'valor_inicial_propiedad': valor_inicial_propiedad,
        'bono_pie': bono_pie,
        'precio_final': precio_final,
        'credito_hipotecario': credito_hipotecario,
        'total': total,
        'saldo_pie': saldo_pie,
        'pie_cancelado': total_detalle_pie,
        'valores_uf_por_pago': valores_uf_por_pago,
        'fecha_hoy': fecha_hoy,
        **site.each_context(request),
    }
    print(total_pagado)

    return render(request, 'documentos/informe_pagos.html', context)


class PagosInvoicePdf(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            id_venta = self.kwargs['id_venta']
            datos = Pagos.objects.filter(id_venta=id_venta)
            datos_venta = Venta.objects.filter(id_venta=id_venta)

            # Totales
            total_pagado = datos.aggregate(total=Sum('monto_pago'))['total'] or 0
            total_pagado_uf = datos.filter(estado_pago="Contabilizado") \
                                  .aggregate(total=Sum('uf_pago'))['total'] or 0

            total_detalle_pie = datos.filter(id_categoria_pago__nombre_categoria_pago="Detalle Pie") \
                                    .aggregate(total=Sum('uf_pago'))['total'] or 0

            # Valores UF por fecha contable
            valores_uf_por_pago = {}
            for pago in datos:
                if pago.estado_pago == "Contabilizado":
                    try:
                        valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                        valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
                    except ValorUf.DoesNotExist:
                        valores_uf_por_pago[pago.id_pago] = None
                else:
                    valores_uf_por_pago[pago.id_pago] = None

            # Información de la propiedad
            valor_inicial_propiedad = bono_pie = precio_final = credito_hipotecario = total = saldo_pie = None

            if datos_venta.exists():
                venta = datos_venta[0]
                valor_inicial_propiedad = venta.id_propiedad.valor_inicial_propiedad
                bono_pie = venta.bono_pie
                precio_final = venta.precio_venta
                credito_hipotecario = venta.credito_hipotecario
                total = valor_inicial_propiedad - bono_pie
                saldo_pie = valor_inicial_propiedad - bono_pie - credito_hipotecario - total_detalle_pie

            context = {
                'datos': datos,
                'id_venta': id_venta,
                'datos_venta': datos_venta,
                'total_pagado': total_pagado,
                'total_pagado_uf': total_pagado_uf,
                'valor_inicial_propiedad': valor_inicial_propiedad,
                'bono_pie': bono_pie,
                'precio_final': precio_final,
                'credito_hipotecario': credito_hipotecario,
                'total': total,
                'saldo_pie': saldo_pie,
                'pie_cancelado': total_detalle_pie,
                'valores_uf_por_pago': valores_uf_por_pago,
                'fecha_hoy': fecha_hoy,
                'icon': 'static/assets/img/illustrations/logo-horizontal.gif',
            }

            template = get_template('documentos/informe_pagos_pdf.html')
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)

            if pisa_status.err:
                raise Exception("Error al generar PDF con xhtml2pdf")

            return response

        except Exception as e:
            print("❌ Error generando PDF:", e)
            messages.error(request, "Ocurrió un error al generar el PDF.")
            return redirect('lista_ventas')


def fpm_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO

    datos_venta = Venta.objects.filter(id_venta=id_venta)

    context = {
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'fecha_hoy': fecha_hoy,
        **site.each_context(request),
    }

    return render(request, 'documentos/carta_fpm.html', context)


class Fpm_VentaPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])
            template = get_template('documentos/carta_fpm_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'fecha_hoy': fecha_hoy,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')


def entrega_documentos_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'fecha_hoy': fecha_hoy,
        **site.each_context(request),
    }

    return render(request, 'documentos/memo_entrega_documentos.html', context)


class EntregaDocumentoPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])

            template = get_template('documentos/memo_entrega_documentos_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'fecha_hoy': fecha_hoy,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')


def carta_cierre_negocios_venta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos_venta = Venta.objects.filter(id_venta=id_venta)
    datos = Pagos.objects.filter(id_venta=id_venta, estado_pago="Contabilizado")
    if datos_venta.exists():
        venta = datos_venta[0]
        valor_inicial_propiedad = venta.id_propiedad.valor_inicial_propiedad
        bono_pie = venta.bono_pie
        precio_final = venta.precio_venta
        credito_hipotecario = venta.credito_hipotecario
        total = valor_inicial_propiedad - bono_pie
    reserva = 10
    pie_contado = precio_final - credito_hipotecario - reserva

    # Valores UF por fecha contable
    valores_uf_por_pago = {}
    for pago in datos:
        if pago.estado_pago == "Contabilizado":
            try:
                valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
            except ValorUf.DoesNotExist:
                valores_uf_por_pago[pago.id_pago] = None
        else:
            valores_uf_por_pago[pago.id_pago] = None

    context = {
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'datos': datos,
        'valores_uf_por_pago': valores_uf_por_pago,
        'fecha_hoy': fecha_hoy,
        'precio_final': precio_final,
        'reserva': reserva,
        'pie_contado': pie_contado,
        'credito_hipotecario': credito_hipotecario,
        'total': total,
        **site.each_context(request),
    }

    return render(request, 'documentos/carta_cierre_negocio.html', context)


class CierreNegociopdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            id_venta = self.kwargs['id_venta']
            datos_venta = Venta.objects.filter(id_venta=id_venta)
            datos = Pagos.objects.filter(id_venta=id_venta, estado_pago="Contabilizado")
            if datos_venta.exists():
                venta = datos_venta[0]
                valor_inicial_propiedad = venta.id_propiedad.valor_inicial_propiedad
                bono_pie = venta.bono_pie
                precio_final = venta.precio_venta
                credito_hipotecario = venta.credito_hipotecario
                total = valor_inicial_propiedad - bono_pie
            reserva = 10
            pie_contado = precio_final - credito_hipotecario - reserva
            # Valores UF por fecha contable
            valores_uf_por_pago = {}
            for pago in datos:
                if pago.estado_pago == "Contabilizado":
                    try:
                        valor_uf = ValorUf.objects.get(fecha_registro=pago.fecha_real_pago)
                        valores_uf_por_pago[pago.id_pago] = valor_uf.valor_uf
                    except ValorUf.DoesNotExist:
                        valores_uf_por_pago[pago.id_pago] = None
                else:
                    valores_uf_por_pago[pago.id_pago] = None
            template = get_template('documentos/carta_cierre_negocio_pdf.html')

            context = {
                'id_venta': id_venta,
                'datos_venta': datos_venta,
                'datos': datos,
                'valores_uf_por_pago': valores_uf_por_pago,
                'fecha_hoy': fecha_hoy,
                'precio_final': precio_final,
                'reserva': reserva,
                'pie_contado': pie_contado,
                'credito_hipotecario': credito_hipotecario,
                'total': total,
                'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')


def memo_ggoo(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        **site.each_context(request),
    }

    return render(request, 'documentos/memo_gastos_operacionales.html', context)


class MemoGgooPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])

            template = get_template('documentos/memo_gastos_operacionales_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')


def carta_oferta(request, id_venta):  # ESTA VISTA ES PARA GENERAR UN DOCUMENTO
    datos = Pagos.objects.filter(id_venta=id_venta)
    datos_venta = Venta.objects.filter(id_venta=id_venta)

    if datos_venta.exists():
        venta = datos_venta[0]
        precio_venta = venta.precio_venta
        precio_bodega = venta.id_propiedad.valor_bodega
        precio_estacionamiento = venta.id_propiedad.valor_estacionamiento
        precio_depto = precio_venta - precio_bodega - precio_estacionamiento

    context = {
        'datos': datos,
        'id_venta': id_venta,
        'datos_venta': datos_venta,
        'fecha_hoy': fecha_hoy,
        'precio_depto': precio_depto,
        **site.each_context(request),
    }

    return render(request, 'documentos/carta_oferta.html', context)


class CartaOfertaPdf(View):
    # datos = Pago.objects.filter(id_venta=id_venta)
    # datos_venta = Venta.objects.filter(id_venta=id_venta)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_URL  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise RuntimeError(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            datos = Pagos.objects.filter(id_venta=self.kwargs['id_venta'])
            datos_venta = Venta.objects.filter(id_venta=self.kwargs['id_venta'])
            if datos_venta.exists():
                venta = datos_venta[0]
                precio_venta = venta.precio_venta
                precio_bodega = venta.id_propiedad.valor_bodega
                precio_estacionamiento = venta.id_propiedad.valor_estacionamiento
                precio_depto = precio_venta - precio_bodega - precio_estacionamiento

            template = get_template('documentos/carta_oferta_pdf.html')
            context = {'datos': datos, 'id_venta': self.kwargs['id_venta'], 'datos_venta': datos_venta,
                       'fecha_hoy': fecha_hoy, 'precio_depto': precio_depto,
                       'icon': 'static/assets/img/illustrations/logo-horizontal.gif'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback)
            return response
        except:
            pass
        return redirect('lista_ventas')


# API

# --- VENTA ---
@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las ventas registradas.",
        summary="Lista de Ventas",
        tags=["Ventas"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una Venta específica por su ID.",
        summary="Detalle de Ventas",
        tags=["Ventas"]
    ),
    create=extend_schema(
        description="Crea una nueva Ventas con los datos proporcionados.",
        summary="Crear Ventas",
        tags=["Ventas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una Venta existente.",
        summary="Actualizar Ventas",
        tags=["Ventas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una Venta existente.",
        summary="Actualizar Parcialmente Ventas",
        tags=["Ventas"]
    ),
    destroy=extend_schema(
        description="Elimina una Venta existente por su ID.",
        summary="Eliminar Ventas",
        tags=["Ventas"]
    ),
)
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]


# --- ETAPAS ---
@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las Etapas registradas.",
        summary="Lista de Etapas",
        tags=["Ventas"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una Etapas específica por su ID.",
        summary="Detalle de Etapas",
        tags=["Ventas"]
    ),
    create=extend_schema(
        description="Crea una nueva Etapas con los datos proporcionados.",
        summary="Crear Etapas",
        tags=["Ventas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una Etapas existente.",
        summary="Actualizar Etapas",
        tags=["Ventas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una Etapas existente.",
        summary="Actualizar Parcialmente Etapas",
        tags=["Ventas"]
    ),
    destroy=extend_schema(
        description="Elimina una Etapas existente por su ID.",
        summary="Eliminar Etapas",
        tags=["Ventas"]
    ),
)
class EtapasViewSet(viewsets.ModelViewSet):
    queryset = Etapas.objects.all()
    serializer_class = EtapasSerializer
    permission_classes = [IsAuthenticated]


# --- VENTA ETAPA ---
@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las VentasEtapa registradas.",
        summary="Lista de VentasEtapa",
        tags=["Ventas"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una VentasEtapa específica por su ID.",
        summary="Detalle de VentasEtapa",
        tags=["Ventas"]
    ),
    create=extend_schema(
        description="Crea una nueva VentasEtapa con los datos proporcionados.",
        summary="Crear VentasEtapa",
        tags=["Ventas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una VentasEtapa existente.",
        summary="Actualizar VentasEtapa",
        tags=["Ventas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una VentasEtapa existente.",
        summary="Actualizar Parcialmente VentasEtapa",
        tags=["Ventas"]
    ),
    destroy=extend_schema(
        description="Elimina una VentasEtapa existente por su ID.",
        summary="Eliminar VentasEtapa",
        tags=["Ventas"]
    ),
)
class VentaEtapaViewSet(viewsets.ModelViewSet):
    queryset = VentaEtapa.objects.all()
    serializer_class = VentaEtapaSerializer
    permission_classes = [IsAuthenticated]


# --- CAMPO ETAPA ---
@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las CampoEtapa registradas.",
        summary="Lista de CampoEtapa",
        tags=["Ventas"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una CampoEtapa específica por su ID.",
        summary="Detalle de CampoEtapa",
        tags=["Ventas"]
    ),
    create=extend_schema(
        description="Crea una nueva CampoEtapa con los datos proporcionados.",
        summary="Crear CampoEtapa",
        tags=["Ventas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una CampoEtapa existente.",
        summary="Actualizar CampoEtapa",
        tags=["Ventas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una CampoEtapa existente.",
        summary="Actualizar Parcialmente CampoEtapa",
        tags=["Ventas"]
    ),
    destroy=extend_schema(
        description="Elimina una CampoEtapa existente por su ID.",
        summary="Eliminar CampoEtapa",
        tags=["Ventas"]
    ),
)
class CampoEtapaViewSet(viewsets.ModelViewSet):
    queryset = CampoEtapa.objects.all()
    serializer_class = CampoEtapaSerializer
    permission_classes = [IsAuthenticated]


# --- VALORES ETAPA ---
@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las ValoresEtapa registradas.",
        summary="Lista de ValoresEtapa",
        tags=["Ventas"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una ValoresEtapa específica por su ID.",
        summary="Detalle de ValoresEtapa",
        tags=["Ventas"]
    ),
    create=extend_schema(
        description="Crea una nueva ValoresEtapa con los datos proporcionados.",
        summary="Crear ValoresEtapa",
        tags=["Ventas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una ValoresEtapa existente.",
        summary="Actualizar ValoresEtapa",
        tags=["Ventas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una ValoresEtapa existente.",
        summary="Actualizar Parcialmente ValoresEtapa",
        tags=["Ventas"]
    ),
    destroy=extend_schema(
        description="Elimina una ValoresEtapa existente por su ID.",
        summary="Eliminar ValoresEtapa",
        tags=["Ventas"]
    ),
)
class ValoresEtapaViewSet(viewsets.ModelViewSet):
    queryset = ValoresEtapa.objects.all()
    serializer_class = ValoresEtapaSerializer
    permission_classes = [IsAuthenticated]
