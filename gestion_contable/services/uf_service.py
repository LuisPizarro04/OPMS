from datetime import datetime

import requests
from django.conf import settings

from gestion_contable.models import ValorUf


BCCH_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
UF_SERIES_ID = "F073.UFF.PRE.Z.D"


def obtener_uf_banco_central(fecha_inicio, fecha_fin=None):
    if fecha_fin is None:
        fecha_fin = fecha_inicio

    token = settings.BCCH_API_TOKEN

    if not token:
        raise ValueError(
            "No se encontró BCCH_API_TOKEN en la configuración."
        )

    params = {
        "token": token,
        "function": "GetSeries",
        "timeseries": UF_SERIES_ID,
        "firstdate": fecha_inicio.strftime("%Y-%m-%d"),
        "lastdate": fecha_fin.strftime("%Y-%m-%d"),
    }

    response = requests.get(
        BCCH_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("Codigo") != 0:
        raise ValueError(
            f"Error Banco Central: {data.get('Descripcion')}"
        )

    return data


def sincronizar_uf(fecha_inicio, fecha_fin=None):
    data = obtener_uf_banco_central(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    observaciones = data.get("Series", {}).get("Obs", [])

    resultados = []

    for observacion in observaciones:
        if observacion.get("statusCode") != "OK":
            continue

        fecha = datetime.strptime(
            observacion["indexDateString"],
            "%d-%m-%Y",
        ).date()

        valor = float(observacion["value"])

        registro, creado = ValorUf.objects.update_or_create(
            fecha_registro=fecha,
            defaults={
                "valor_uf": valor,
            },
        )

        resultados.append({
            "fecha": fecha,
            "valor": valor,
            "creado": creado,
        })

    return resultados