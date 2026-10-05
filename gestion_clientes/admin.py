from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm

from .forms import ClienteExportForm
from .models import (
    Nacionalidade,
    AreaProfesion,
    Profesione,
    Cliente,
)


# ============================================================
# NACIONALIDADES
# ============================================================

@admin.register(Nacionalidade)
class NacionalidadeAdmin(ModelAdmin):
    list_display = (
        "id_nacionalidad",
        "nombre_nacionalidad",
    )

    search_fields = (
        "nombre_nacionalidad",
    )

    ordering = (
        "nombre_nacionalidad",
    )


# ============================================================
# ÁREAS DE PROFESIÓN
# ============================================================

@admin.register(AreaProfesion)
class AreaProfesionAdmin(ModelAdmin):
    list_display = (
        "id_area_profesion",
        "nombre_area_profesion",
    )

    search_fields = (
        "nombre_area_profesion",
    )

    ordering = (
        "nombre_area_profesion",
    )


# ============================================================
# PROFESIONES
# ============================================================

@admin.register(Profesione)
class ProfesioneAdmin(ModelAdmin):
    list_display = (
        "id_profesione",
        "nombre_profesione",
        "id_area_profesion",
    )

    search_fields = (
        "nombre_profesione",
        "id_area_profesion__nombre_area_profesion",
    )

    list_filter = (
        "id_area_profesion",
    )

    ordering = (
        "nombre_profesione",
    )

    list_select_related = (
        "id_area_profesion",
    )


# ============================================================
# RECURSO IMPORT / EXPORT CLIENTES
# ============================================================

class ClienteResource(resources.ModelResource):

    rut_cliente = fields.Field(
        attribute="rut_cliente",
        column_name="RUT",
    )

    nombres_1 = fields.Field(
        attribute="nombres_1",
        column_name="Primer nombre",
    )

    nombres_2 = fields.Field(
        attribute="nombres_2",
        column_name="Segundo nombre",
    )

    apellidos_1 = fields.Field(
        attribute="apellidos_1",
        column_name="Primer apellido",
    )

    apellidos_2 = fields.Field(
        attribute="apellidos_2",
        column_name="Segundo apellido",
    )

    correo = fields.Field(
        attribute="correo",
        column_name="Correo",
    )

    telefono = fields.Field(
        attribute="telefono",
        column_name="Teléfono",
    )

    genero = fields.Field(
        attribute="genero",
        column_name="Género",
    )

    estado_civil = fields.Field(
        attribute="estado_civil",
        column_name="Estado civil",
    )

    fecha_nacimiento = fields.Field(
        attribute="fecha_nacimiento",
        column_name="Fecha de nacimiento",
    )

    direccion = fields.Field(
        attribute="direccion",
        column_name="Dirección",
    )

    region = fields.Field(
        attribute="region",
        column_name="Región",
    )

    ciudad = fields.Field(
        attribute="ciudad",
        column_name="Ciudad",
    )

    nivel_educacional = fields.Field(
        attribute="nivel_educacional",
        column_name="Nivel educacional",
    )

    renta = fields.Field(
        attribute="renta",
        column_name="Renta",
    )

    id_nacionalidad = fields.Field(
        attribute="id_nacionalidad",
        column_name="Nacionalidad",
        widget=ForeignKeyWidget(
            Nacionalidade,
            field="nombre_nacionalidad",
        ),
    )

    id_profesion = fields.Field(
        attribute="id_profesion",
        column_name="Profesión",
        widget=ForeignKeyWidget(
            Profesione,
            field="nombre_profesione",
        ),
    )

    tipo_cliente = fields.Field(
        attribute="tipo_cliente",
        column_name="Tipo de cliente",
    )

    class Meta:
        model = Cliente

        skip_unchanged = True
        report_skipped = True

        # El RUT será el identificador único utilizado
        # por django-import-export.
        import_id_fields = (
            "rut_cliente",
        )

        fields = (
            "rut_cliente",
            "nombres_1",
            "nombres_2",
            "apellidos_1",
            "apellidos_2",
            "correo",
            "telefono",
            "genero",
            "estado_civil",
            "fecha_nacimiento",
            "direccion",
            "region",
            "ciudad",
            "nivel_educacional",
            "renta",
            "id_nacionalidad",
            "id_profesion",
            "tipo_cliente",
        )

        export_order = fields


# ============================================================
# CLIENTES
# ============================================================

@admin.register(Cliente)
class ClienteAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = ClienteResource

    # ========================================================
    # IMPORT / EXPORT - INTEGRACIÓN UNFOLD
    # ========================================================

    import_form_class = ImportForm
    export_form_class = ClienteExportForm

    # ========================================================
    # LISTADO
    # ========================================================

    list_display = (
        "rut_cliente",
        "nombre_completo",
        "correo",
        "telefono",
        "region",
        "tipo_cliente",
        "id_profesion",
        "renta",
    )

    list_display_links = (
        "rut_cliente",
        "nombre_completo",
    )

    # ========================================================
    # BÚSQUEDA
    # ========================================================

    search_fields = (
        "rut_cliente",
        "nombres_1",
        "nombres_2",
        "apellidos_1",
        "apellidos_2",
        "correo",
        "telefono",
    )

    # ========================================================
    # FILTROS
    # ========================================================

    list_filter = (
        "tipo_cliente",
        "genero",
        "region",
        "id_nacionalidad",
        "id_profesion",
    )

    ordering = (
        "-id_cliente",
    )

    list_select_related = (
        "id_nacionalidad",
        "id_profesion",
    )
    fieldsets = (
        (
            "Información del cliente",
            {
                "fields": (
                    ("tipo_cliente", "rut_cliente"),
                    ("id_nacionalidad", "fecha_nacimiento"),
                ),
            },
        ),
        (
            "Datos personales",
            {
                "fields": (
                    ("nombres_1", "nombres_2"),
                    ("apellidos_1", "apellidos_2"),
                    ("genero", "estado_civil"),
                ),
            },
        ),
        (
            "Contacto y ubicación",
            {
                "fields": (
                    ("correo", "telefono"),
                    "direccion",
                    ("region", "ciudad"),
                ),
            },
        ),
        (
            "Información profesional",
            {
                "fields": (
                    ("nivel_educacional", "id_profesion"),
                    "renta",
                ),
            },
        ),
    )

    list_per_page = 25

    # ========================================================
    # CAMPOS CALCULADOS
    # ========================================================

    @admin.display(
        description="Cliente",
        ordering="apellidos_1",
    )
    def nombre_completo(self, obj):
        partes = [
            obj.nombres_1,
            obj.nombres_2,
            obj.apellidos_1,
            obj.apellidos_2,
        ]

        return " ".join(
            str(parte).strip()
            for parte in partes
            if parte
        )