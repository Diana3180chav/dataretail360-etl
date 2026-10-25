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
