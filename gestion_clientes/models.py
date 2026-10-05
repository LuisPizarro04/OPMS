from django.db import models
from utils_project.choices import *
# Create your models here.

class Nacionalidade(models.Model):
    id_nacionalidad = models.AutoField(primary_key=True)
    nombre_nacionalidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'nacionalidade'
        verbose_name = 'Nacionalidade'
        verbose_name_plural = 'Nacionalidades'

    def __str__(self):
        return self.nombre_nacionalidad

class AreaProfesion(models.Model):
    id_area_profesion = models.AutoField(primary_key=True)
    nombre_area_profesion = models.CharField(max_length=100)

    class Meta:
        db_table = 'area_profesion'
        verbose_name = 'Area de Profesion'
        verbose_name_plural = 'Areas de Profesion'
        # unique_together = ('id_area_profesion', 'nombre_area_profesion')
    def __str__(self):
        return self.nombre_area_profesion



class Profesione(models.Model):
    id_profesione = models.AutoField(primary_key=True)
    id_area_profesion = models.ForeignKey(AreaProfesion, on_delete=models.CASCADE)
    nombre_profesione = models.CharField(max_length=100)

    class Meta:
        db_table = 'profesione'
        verbose_name = 'Profesione'
        verbose_name_plural = 'Profesiones'

    def __str__(self):
        return self.nombre_profesione


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(choices=CLIENTES_CHOICES, max_length=50, default=CLIENTES_CHOICES[0][0])
    rut_cliente = models.CharField(verbose_name="Rut Cliente", max_length=50)
    id_nacionalidad = models.ForeignKey(Nacionalidade, verbose_name="Nacionalidad",
                                        on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(verbose_name="Fecha nacimiento")
    genero = models.CharField(verbose_name="Género", max_length=30, choices=SEXO_CHOICES, default=sin_definir)
    region = models.CharField(verbose_name="Región", max_length=31, choices=REGIONES_CHOICES, default=iv_reg_coquimbo)
    nombres_1 = models.CharField(verbose_name="1er Nombre", max_length=50)
    nombres_2 = models.CharField(verbose_name="2do Nombre", max_length=50)
    apellidos_1 = models.CharField(verbose_name="1er Apellido", max_length=50)
    apellidos_2 = models.CharField(verbose_name="2do Apellido", max_length=50)
    correo = models.EmailField(verbose_name="Correo")
    telefono = models.CharField(verbose_name="Teléfono", max_length=9)
    renta = models.IntegerField(verbose_name="Renta")
    id_profesion = models.ForeignKey(Profesione, verbose_name="Profesión", on_delete=models.CASCADE)  # PENDIENTE
    estado_civil = models.CharField(
        verbose_name="Estado civil",
        max_length=30,
        choices=ESTADO_CIVIL_CHOICES,
        blank=True,
        default=""
    )

    direccion = models.CharField(
        verbose_name="Dirección",
        max_length=255,
        blank=True,
        default=""
    )

    ciudad = models.CharField(
        verbose_name="Ciudad",
        max_length=100,
        blank=True,
        default=""
    )

    nivel_educacional = models.CharField(
        verbose_name="Nivel educacional",
        max_length=100,
        choices=ENSENAGSA_CHOICES,
        blank=True,
        default=""
    )



    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_cliente']
    def __str__(self):
        return str(self.nombres_1)+ " " +str(self.apellidos_1)+  " (" +str(self.rut_cliente) +  ")"