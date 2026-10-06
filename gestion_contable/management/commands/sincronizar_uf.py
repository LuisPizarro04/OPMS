from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, CommandError

from gestion_contable.services.uf_service import sincronizar_uf


class Command(BaseCommand):
    help = "Sincroniza los valores de la UF desde el Banco Central de Chile."

    def add_arguments(self, parser):
        parser.add_argument(
            "--desde",
            type=str,
            help="Fecha inicial en formato YYYY-MM-DD.",
        )

        parser.add_argument(
            "--hasta",
            type=str,
            help="Fecha final en formato YYYY-MM-DD.",
        )

    def handle(self, *args, **options):
        hoy = date.today()

        try:
            fecha_inicio = (
                datetime.strptime(
                    options["desde"],
                    "%Y-%m-%d",
                ).date()
                if options["desde"]
                else hoy - timedelta(days=3)
            )

            fecha_fin = (
                datetime.strptime(
                    options["hasta"],
                    "%Y-%m-%d",
                ).date()
                if options["hasta"]
                else hoy
            )

        except ValueError:
            raise CommandError(
                "Las fechas deben utilizar el formato YYYY-MM-DD."
            )

        if fecha_inicio > fecha_fin:
            raise CommandError(
                "La fecha inicial no puede ser posterior a la fecha final."
            )

        self.stdout.write(
            f"Sincronizando UF desde {fecha_inicio} hasta {fecha_fin}..."
        )

        try:
            resultados = sincronizar_uf(
                fecha_inicio,
                fecha_fin,
            )
        except Exception as error:
            raise CommandError(
                f"Error al sincronizar UF: {error}"
            )

        creados = sum(
            1 for resultado in resultados
            if resultado["creado"]
        )

        actualizados = len(resultados) - creados

        self.stdout.write(
            self.style.SUCCESS(
                f"Sincronización completada: "
                f"{creados} creados, "
                f"{actualizados} actualizados."
            )
        )