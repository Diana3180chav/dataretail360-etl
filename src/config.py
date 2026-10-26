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
