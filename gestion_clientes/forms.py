from unfold.contrib.import_export.forms import SelectableFieldsExportForm


class ClienteExportForm(SelectableFieldsExportForm):

    FIELD_LABELS = {
        "clienteresource_rut_cliente": "RUT",
        "clienteresource_nombres_1": "Primer nombre",
        "clienteresource_nombres_2": "Segundo nombre",
        "clienteresource_apellidos_1": "Primer apellido",
        "clienteresource_apellidos_2": "Segundo apellido",
        "clienteresource_correo": "Correo",
        "clienteresource_telefono": "Teléfono",
        "clienteresource_genero": "Género",
        "clienteresource_estado_civil": "Estado civil",
        "clienteresource_fecha_nacimiento": "Fecha de nacimiento",
        "clienteresource_direccion": "Dirección",
        "clienteresource_region": "Región",
        "clienteresource_ciudad": "Ciudad",
        "clienteresource_nivel_educacional": "Nivel educacional",
        "clienteresource_renta": "Renta",
        "clienteresource_id_nacionalidad": "Nacionalidad",
        "clienteresource_id_profesion": "Profesión",
        "clienteresource_tipo_cliente": "Tipo de cliente",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Nombres amigables para los campos exportables
        for field_name, label in self.FIELD_LABELS.items():
            if field_name in self.fields:
                self.fields[field_name].label = label

        # Texto del selector de formato
        if "format" in self.fields:
            self.fields["format"].empty_label = "Seleccionar formato"