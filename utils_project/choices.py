CLIENTES_CHOICES = [
    ('Natural', 'Natural'),
    ('Empresa', 'Empresa'),
]

POSTVENTA_CHOICES = [
    ('Resuelto', 'Resuelto'),
    ('Trabajos', 'Trabajos'),
    ('Visita', 'Visita'),
    ('Cerrado', 'Cerrado'),
    ('Pendiente', 'Pendiente'),
    ('No Aplica', 'No Aplica'),
    ('Pospuesto', 'Pospuesto'),
    ('Propietario rechaza trabajos ', 'Propietario rechaza trabajos '),
    ('Observación', 'Observación'),
    ('Observación Entrega', 'Observación Entrega'),
    ('Terminado', 'Terminado'),

]

APLICACION_DSCTO_CHOICES = [
    ('No Aplica', 'No Aplica'),
    ('Precio', 'Precio'),
    ('Pie', 'Pie'),
]

TIPO_VENTA_CHOICES = [
    ('Credito', 'Crédito'),
    ('Contado', 'Contado'),
]

VENTAS_CHOICES = [
    ('Activa', 'Activa'),
    ('Inactiva', 'Inactiva'),
    ('Desistida', 'Desistida'),
    ('Promesa', 'Promesa'),
    ('Reserva', 'Reserva'),
]
PAGOS_CHOICES = [
    ('Pendiente', 'Pendiente'),
    ('Contabilizado', 'Contabilizado'),
]

PROPIEDAD_CHOICES = [
    ('Libre', 'Libre'),
    ('Tomada', 'Tomada'),
    ('Entregada', 'Entregada'),
]

is_active = 'Activo'
is_inactive = 'Inactivo'

IS_ACTIVE_CHOICES = [(is_active, 'Activo'),
                     (is_inactive, 'Inactivo'), ]

masculino = 'Masculino'
femenino = 'Femenino'
sin_definir = 'Sin Definir'
otro = 'Otro'

SEXO_CHOICES = [(masculino, 'Masculino'),
                (femenino, 'Femenino'),
                (sin_definir, 'Sin Definir'),
                (otro, 'Otro'), ]

soltero_a = 'Soltero/a'
casado_a = 'Casado/a'
divorciado_a = 'Divorciado/a'

ESTADO_CIVIL_CHOICES = [(soltero_a, 'Soltero/a'),
                        (casado_a, 'Casado/a'),
                        (divorciado_a, 'Divorciado/a'), ]

ens_basica = 'Enseñanza Básica'
ens_media = 'Enseñanza Media'
tec_prof = 'Técnico Profesional'
tec_nvl_sup = 'Técnico Nivel Superior'
profesional = 'Profesional'

ENSENAGSA_CHOICES = [(ens_basica, 'Enseñanza Básica'),
                     (ens_media, 'Enseñanza Media'),
                     (tec_prof, 'Técnico Profesional'),
                     (tec_nvl_sup, 'Técnico Nivel Superior'),
                     (profesional, 'Profesional'), ]

############################################################################################
i_reg_tarapaca = 'I REGIÓN DE TARAPACÁ'
ii_reg_antofagasta = 'II REGIÓN DE ANTOFAGASTA'
iii_reg_atacama = 'III REGIÓN DE ATACAMA'
iv_reg_coquimbo = 'IV REGIÓN DE COQUIMBO'
v_reg_valparaiso = 'V REGIÓN DE VALPARAÍSO'
vi_reg_ohiggins = 'VI REGIÓN DE O´HIGGINS'
vii_reg_maule = 'VII REGIÓN DEL MAULE'
xvi_reg_nugble = 'XVI REGIÓN DEL ÑUBLE'
viii_reg_biobio = "VIII REGIÓN DEL BÍO-BÍO"
ix_reg_araucania = "IX REGIÓN DE LA ARAUCANÍA"
x_reg_lagos = "X REGIÓN DE LOS LAGOS"
xi_reg_aysen = "XI REGIÓN DE AYSÉN"
xii_reg_magallanes = "XII REGIÓN DE MAGALLANES"
reg_met = "REGIÓN METROPOLITANA"
xiv_reg_rios = "XIV DE LOS RÍOS"
xv_reg_arica = "XV REGIÓN DE ARICA Y PARINACOTA"
# Regiones
REGIONES_CHOICES = [(i_reg_tarapaca, 'I REGIÓN DE TARAPACÁ'),
                    (ii_reg_antofagasta, 'II REGIÓN DE ANTOFAGASTA'),
                    (iii_reg_atacama, 'III REGIÓN DE ATACAMA'),
                    (iv_reg_coquimbo, 'IV REGIÓN DE COQUIMBO'),
                    (v_reg_valparaiso, 'V REGIÓN DE VALPARAÍSO'),
                    (vi_reg_ohiggins, 'VI REGIÓN DE O´HIGGINS'),
                    (vii_reg_maule, 'VII REGIÓN DEL MAULE'),
                    (xvi_reg_nugble, 'XVI REGIÓN DEL ÑUBLE'),
                    (viii_reg_biobio, "VIII REGIÓN DEL BÍO-BÍO"),
                    (ix_reg_araucania, "IX REGIÓN DE LA ARAUCANÍA"),
                    (x_reg_lagos, "X REGIÓN DE LOS LAGOS"),
                    (xi_reg_aysen, "XI REGIÓN DE AYSÉN"),
                    (xii_reg_magallanes, "XII REGIÓN DE MAGALLANES"),
                    (reg_met, "REGIÓN METROPOLITANA"),
                    (xiv_reg_rios, "XIV DE LOS RÍOS"),
                    (xv_reg_arica, "XV REGIÓN DE ARICA Y PARINACOTA"), ]
############################################################################################

enero = "Enero"
febrero = "Febrero"
marzo = "Marzo"
abril = "Abril"
mayo = "Mayo"
junio = "Junio"
julio = "Julio"
agosto = "Agosto"
septiembre = "Septiembre"
octubre = "Octubre"
noviembre = "Noviembre"
diciembre = "Diciembre"
# Meses
MESES_CHOICES = [(enero, "Enero"),
                 (febrero, "Febrero"),
                 (marzo, "Marzo"),
                 (abril, "Abril"),
                 (mayo, "Mayo"),
                 (junio, "Junio"),
                 (julio, "Julio"),
                 (agosto, "Agosto"),
                 (septiembre, "Septiembre"),
                 (octubre, "Octubre"),
                 (noviembre, "Noviembre"),
                 (diciembre, "Diciembre"), ]

realizado = 'Realizado'
pendiente = 'Pendiente'
protestado = 'Protestado'
# pago_estado_pago
EST_PAGO_CHOICES = [(realizado, 'Realizado'),
                    (pendiente, 'Pendiente'),
                    (protestado, 'Protestado'), ]

activa = 'Activa'
inactiva = 'Inactiva'
desistimiento = 'Desestimiento'
promesa = 'Promesa'
venta_comisionada = 'Venta Comisionada'
en_escritura = 'En Escritura'
escriturada = 'Escriturada'
# venta_estado_venta
EST_VENTA_CHOICES = [(activa, 'Activa'),
                     (inactiva, 'Inactiva'),
                     (desistimiento, 'Desestimiento'),
                     (promesa, 'Promesa'),
                     (venta_comisionada, 'Venta Comisionada'),
                     (en_escritura, 'En Escritura'),
                     (escriturada, 'Escriturada'), ]

si = 'Si'
no = 'No'
# venta_pie_abono_venta
SI_NO_CHOICES = [(si, 'Si'),
                 (no, 'No')]

rank_1 = '$0 a $499.999'
rank_2 = '$450.000 a $799.999'
rank_3 = '$750.000 a $1.299.999'
rank_4 = '$1.300.000 a $2.499.999'
rank_5 = '$2.500.000 a $2.999.999'
rank_6 = '$3.000.000 a $3.999.999'
rank_7 = '$4.000.000 a $4.999.999'
rank_8 = '$5.000.000 a $5.999.999'
rank_9 = '$6.000.000 a $6.999.999'
rank_10 = '> $7.000.000'
rank_11 = 'No definido'
# cotizacion_renta_cotizacion
RENTA_COTIZACION_CHOICES = [(rank_1, '$0 a $499.999'),
                            (rank_2, '$450.000 a $799.999'),
                            (rank_3, '$750.000 a $1.299.999'),
                            (rank_4, '$1.300.000 a $2.499.999'),
                            (rank_5, '$2.500.000 a $2.999.999'),
                            (rank_6, '$3.000.000 a $3.999.999'),
                            (rank_7, '$4.000.000 a $4.999.999'),
                            (rank_8, '$5.000.000 a $5.999.999'),
                            (rank_9, '$6.000.000 a $6.999.999'),
                            (rank_10, '> $7.000.000'),
                            (rank_11, 'No definido'), ]

# orientacion_vivienda
norte = 'NORTE'
sur = 'SUR'
oriente = 'ORIENTE'
poniente = 'PONIENTE'
nor_oriente = 'NOR ORIENTE'
sur_poniente = 'SUR PONIENTE'
nor_poniente = 'NOR PONIENTE'
sur_oriente = 'SUR ORIENTE'

ORIENTACION_VIVIENDA = [(norte, 'NORTE'),
                        (sur, 'SUR'),
                        (oriente, 'ORIENTE'),
                        (poniente, 'PONIENTE'),
                        (nor_oriente, 'NOR ORIENTE'),
                        (sur_poniente, 'SUR PONIENTE'),
                        (nor_poniente, 'NOR PONIENTE'),
                        (sur_oriente, 'SUR ORIENTE')]

# piso
uno = '1'
dos = '2'
tres = '3'
cuatro = '4'
cinco = '5'
seis = '6'
siete = '7'
ocho = '8'
nueve = '9'
dies = '10'
once = '11'
doce = '12'
trece = '13'
catorce = '14'
quince = '15'
dieciseis = '16'
diecisiete = '17'
dieciocho = '18'
diecinueve = '19'
veinte = '20'

PISO = [(uno, '1'),
        (dos, '2'),
        (tres, '3'),
        (cuatro, '4'),
        (cinco, '5'),
        (seis, '6'),
        (siete, '7'),
        (ocho, '8'),
        (nueve, '9'),
        (dies, '10'),
        (once, '11'),
        (doce, '12'),
        (trece, '13'),
        (catorce, '14'),
        (quince, '15'),
        (dieciseis, '16'),
        (diecisiete, '17'),
        (dieciocho, '18'),
        (diecinueve, '19'),
        (veinte, '20')]

disponible = 'Disponible'
no_disponible = 'No Disponible'

IS_DISPONIBLE_CHOICES = [(disponible, 'Disponible'),
                         (no_disponible, 'No Disponible'), ]

TIPO_DATO_CHOICES = [
    ("Texto", "Texto"),
    ("Fecha", "Fecha"),
    ("Numero", "Número"),
    ("Monto", "Monto"),
    ("SiNo", "Sí / No"),
    ("TextoLargo", "Texto largo"),
]