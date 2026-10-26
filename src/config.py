"""
config.py
---------
Configuración central del pipeline: rutas, base de datos y archivos de cada lote.
Separar la configuración del código permite cambiar una ruta o agregar un lote
sin tocar la lógica del ETL (checklist 2.3.4, punto 7).
"""

from pathlib import Path

# --- Rutas del proyecto ---
RAIZ = Path(__file__).resolve().parent.parent
CARPETA_RAW = RAIZ / "data" / "raw"
CARPETA_LOGS = RAIZ / "logs"
RUTA_BD = RAIZ / "db" / "dataretail360.db"

# Cadena de conexión de SQLAlchemy: "motor:///ruta_al_archivo"
URL_BD = f"sqlite:///{RUTA_BD}"

# --- Archivos que entrega cada lote ---
# clave: nombre lógico de la fuente (también define la tabla bronze_<clave>)
# valor: nombre del archivo en data/raw
FUENTES_POR_LOTE = {
    1: {
        "canales": "canales.csv",
        "sucursales": "sucursales.csv",
        "campanas": "campanas.csv",
        "productos": "productos.csv",
        "clientes": "clientes.csv",
        "ventas_tienda": "ventas_tienda_lote1.csv",
        "ventas_online": "ventas_online_lote1.csv",
    },
    2: {
        "productos": "productos_lote2.csv",
        "clientes": "clientes_lote2.csv",
        "ventas_tienda": "ventas_tienda_lote2.csv",
        "ventas_online": "ventas_online_lote2.csv",
    },
}

# --- Parámetros de la capa Silver ---
# Fecha de corte de cada lote: se usa para calcular la edad (y el tramo de edad)
FECHA_CORTE_POR_LOTE = {1: "2026-06-30", 2: "2026-09-30"}

# Tramos de edad: (edad mínima, edad máxima, etiqueta)
TRAMOS_EDAD = [(18, 25, "18-25"), (26, 35, "26-35"), (36, 45, "36-45"),
               (46, 55, "46-55"), (56, 65, "56-65"), (66, 120, "66+")]

# Tabla de referencia geográfica oficial: comuna -> región.
# Se usa para homologar comunas y validar la jerarquía Región > Comuna.
REGION_POR_COMUNA = {
    "Santiago": "Metropolitana", "Maipú": "Metropolitana", "Puente Alto": "Metropolitana",
    "Las Condes": "Metropolitana", "Ñuñoa": "Metropolitana", "La Florida": "Metropolitana",
    "Providencia": "Metropolitana", "Viña del Mar": "Valparaíso", "Valparaíso": "Valparaíso",
    "Antofagasta": "Antofagasta", "La Serena": "Coquimbo", "Coquimbo": "Coquimbo",
    "Concepción": "Biobío", "Talcahuano": "Biobío", "Temuco": "La Araucanía",
}

# Homologación de canales del e-commerce a los códigos del catálogo de canales
CANAL_ONLINE = {"WEB": "CAN02", "APP": "CAN03"}
CANAL_TIENDA = "CAN01"
SUCURSAL_ONLINE = "WEB01"

# --- Parámetros de la capa Gold ---
# Primer día de cada lote: desde esa fecha rigen las nuevas versiones SCD2
FECHA_INICIO_POR_LOTE = {1: "2026-01-01", 2: "2026-07-01"}
FECHA_INICIO_HISTORICA = "1900-01-01"    # vigencia inicial de la primera versión
FECHA_FIN_ABIERTA = "9999-12-31"         # vigencia de la versión actual

# Calendario de la dimensión Tiempo
ANIO_CALENDARIO = 2026
# Feriados nacionales de Chile 2026 (referencia para la dimensión Tiempo)
FERIADOS = {
    "2026-01-01", "2026-04-03", "2026-04-04", "2026-05-01", "2026-05-21",
    "2026-06-21", "2026-06-29", "2026-07-16", "2026-08-15", "2026-09-18",
    "2026-09-19", "2026-10-12", "2026-10-31", "2026-11-01", "2026-12-08", "2026-12-25",
}
