from django import forms


class SincronizarUfForm(forms.Form):
    fecha_inicio = forms.DateField(
        label="Desde",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": (
                    "border border-base-200 bg-white font-medium "
                    "min-w-20 placeholder-base-400 rounded-default "
                    "shadow-xs text-font-default-light text-sm "
                    "focus:outline-2 focus:-outline-offset-2 "
                    "focus:outline-primary-600 "
                    "dark:bg-base-900 dark:border-base-700 "
                    "dark:text-font-default-dark "
                    "w-full px-3 py-2"
                ),
            }
        ),
    )

    fecha_fin = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": (
                    "border border-base-200 bg-white font-medium "
                    "min-w-20 placeholder-base-400 rounded-default "
                    "shadow-xs text-font-default-light text-sm "
                    "focus:outline-2 focus:-outline-offset-2 "
                    "focus:outline-primary-600 "
                    "dark:bg-base-900 dark:border-base-700 "
                    "dark:text-font-default-dark "
                    "w-full px-3 py-2"
                ),
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha inicial no puede ser posterior a la fecha final."
            )

        return cleaned_data