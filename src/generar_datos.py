"""
generar_datos.py
----------------
Simula los sistemas de origen de DataRetail 360 y genera archivos CSV
en la carpeta data/raw.

Este script NO forma parte del ETL: representa a las áreas de la empresa
(Comercial, Marketing, Operaciones, Canal digital) que entregan los datos.
El ETL solo leerá los archivos que este script deja en data/raw.
"""

from pathlib import Path

import numpy as np
import pandas as pd

# ------------------------------------------------------------------
# 1. Configuración general
# ------------------------------------------------------------------
SEMILLA = 360                      # misma semilla = mismos datos en cada ejecución
rng = np.random.default_rng(SEMILLA)

RAIZ = Path(__file__).resolve().parent.parent      # carpeta dataretail360-etl
CARPETA_RAW = RAIZ / "data" / "raw"
CARPETA_RAW.mkdir(parents=True, exist_ok=True)


def guardar(df: pd.DataFrame, nombre_archivo: str) -> None:
    """Guarda un DataFrame como CSV en data/raw e informa cuántas filas tiene."""
    ruta = CARPETA_RAW / nombre_archivo
    df.to_csv(ruta, index=False, encoding="utf-8")
    print(f"[OK] {nombre_archivo}: {len(df)} filas")


def precio_retail(valor: float) -> int:
    """Redondea un precio al estilo retail chileno: termina en 990 (ej. 24.990)."""
    return int(round(valor / 1000) * 1000 - 10)


# ------------------------------------------------------------------
# 2. Canales de venta  (origen: Canal digital / Comercial)
# ------------------------------------------------------------------
def generar_canales() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("CAN01", "Tienda física", "Presencial"),
            ("CAN02", "Web", "Digital"),
            ("CAN03", "App", "Digital"),
        ],
        columns=["cod_canal", "nombre_canal", "tipo_canal"],
    )


# ------------------------------------------------------------------
# 3. Sucursales  (origen: Operaciones)
# ------------------------------------------------------------------
def generar_sucursales() -> pd.DataFrame:
    filas = [
        # cod,   nombre,                    tipo,      comuna,          región,          zona,     lat,      lon,      apertura
        ("SUC01", "DataRetail Santiago Centro", "Física", "Santiago",      "Metropolitana", "Centro", -33.4378, -70.6505, "2015-03-01"),
        ("SUC02", "DataRetail Maipú",           "Física", "Maipú",         "Metropolitana", "Centro", -33.5110, -70.7580, "2016-08-15"),
        ("SUC03", "DataRetail Puente Alto",     "Física", "Puente Alto",   "Metropolitana", "Centro", -33.6117, -70.5758, "2017-04-10"),
        ("SUC04", "DataRetail Las Condes",      "Física", "Las Condes",    "Metropolitana", "Centro", -33.4080, -70.5670, "2018-11-20"),
        ("SUC05", "DataRetail Viña del Mar",    "Física", "Viña del Mar",  "Valparaíso",    "Centro", -33.0245, -71.5518, "2019-06-01"),
        ("SUC06", "DataRetail Antofagasta",     "Física", "Antofagasta",   "Antofagasta",   "Norte",  -23.6509, -70.3975, "2020-02-14"),
        ("SUC07", "DataRetail La Serena",       "Física", "La Serena",     "Coquimbo",      "Norte",  -29.9045, -71.2489, "2021-09-01"),
        ("SUC08", "DataRetail Concepción",      "Física", "Concepción",    "Biobío",        "Sur",    -36.8270, -73.0503, "2022-05-05"),
        ("SUC09", "DataRetail Temuco",          "Física", "Temuco",        "La Araucanía",  "Sur",    -38.7359, -72.5904, "2023-10-10"),
        # Sucursal virtual: recibe todas las ventas web y app
        ("WEB01", "Tienda Online",              "Virtual", "Online",       "Online",        "Online", None,     None,     "2020-04-01"),
    ]
    return pd.DataFrame(
        filas,
        columns=["cod_sucursal", "nombre_sucursal", "tipo", "comuna", "region",
                 "zona", "latitud", "longitud", "fecha_apertura"],
    )


# ------------------------------------------------------------------
# 4. Productos  (origen: Comercial)
# ------------------------------------------------------------------
# subcategoría: (categoría, marcas posibles, [(producto, precio mínimo, precio máximo), ...])
CATALOGO = {
    "Celulares": ("Tecnología", ["Samsung", "Motorola", "Xiaomi"], [
        ("Smartphone gama alta 256GB", 550_000, 900_000),
        ("Smartphone gama media 128GB", 200_000, 350_000),
        ("Smartphone básico 64GB", 90_000, 150_000),
    ]),
    "Computación": ("Tecnología", ["Lenovo", "HP", "Asus"], [
        ("Notebook 15 pulgadas", 450_000, 800_000),
        ("Notebook 14 pulgadas", 350_000, 600_000),
        ("Monitor 24 pulgadas", 110_000, 180_000),
        ("Teclado inalámbrico", 15_000, 35_000),
    ]),
    "Audio": ("Tecnología", ["JBL", "Sony"], [
        ("Audífonos Bluetooth", 25_000, 90_000),
        ("Parlante portátil", 40_000, 120_000),
        ("Barra de sonido", 120_000, 250_000),
    ]),
    "Electrodomésticos": ("Hogar", ["Oster", "Thomas", "Mademsa"], [
        ("Hervidor eléctrico", 15_000, 30_000),
        ("Microondas 20 litros", 60_000, 100_000),
        ("Aspiradora", 70_000, 150_000),
        ("Freidora de aire", 50_000, 110_000),
    ]),
    "Cocina": ("Hogar", ["Tramontina", "Rochedo"], [
        ("Batería de cocina 7 piezas", 60_000, 120_000),
        ("Set de cuchillos", 15_000, 40_000),
        ("Sartén antiadherente", 12_000, 30_000),
    ]),
    "Decoración": ("Hogar", ["Casaideas", "Mica"], [
        ("Lámpara de mesa", 15_000, 40_000),
        ("Cojín decorativo", 8_000, 15_000),
        ("Espejo de pared", 25_000, 60_000),
    ]),
    "Vestuario Hombre": ("Vestuario", ["Ellus", "Doo Australia"], [
        ("Polera básica hombre", 9_000, 15_000),
        ("Jeans hombre", 25_000, 40_000),
        ("Chaqueta hombre", 45_000, 80_000),
    ]),
    "Vestuario Mujer": ("Vestuario", ["Basement", "Sybilla"], [
        ("Blusa mujer", 12_000, 25_000),
        ("Jeans mujer", 25_000, 40_000),
        ("Vestido", 20_000, 45_000),
    ]),
    "Calzado": ("Vestuario", ["Nike", "Adidas", "Bata"], [
        ("Zapatillas urbanas", 40_000, 80_000),
        ("Zapatillas running", 55_000, 120_000),
        ("Zapatos formales", 35_000, 70_000),
    ]),
    "Fitness": ("Deportes", ["Everlast", "Kettler"], [
        ("Mancuernas 5 kg (par)", 15_000, 30_000),
        ("Mat de yoga", 10_000, 25_000),
        ("Bicicleta estática", 180_000, 350_000),
    ]),
}


def generar_productos() -> pd.DataFrame:
    filas = []
    n = 1
    for subcategoria, (categoria, marcas, productos) in CATALOGO.items():
        for nombre_base, pmin, pmax in productos:
            marca = str(rng.choice(marcas))
            precio = precio_retail(rng.uniform(pmin, pmax))
            margen = rng.uniform(0.25, 0.45)          # margen bruto entre 25% y 45%
            costo = int(round(precio * (1 - margen)))
            filas.append({
                "cod_producto": f"PRD{n:04d}",
                "nombre_producto": f"{nombre_base} {marca}",
                "marca": marca,
                "subcategoria": subcategoria,
                "categoria": categoria,
                "precio_lista": precio,
                "costo_unitario": costo,
                "estado": "Activo",
            })
            n += 1
    return pd.DataFrame(filas)


# ------------------------------------------------------------------
# 5. Campañas  (origen: Marketing)
# ------------------------------------------------------------------
def generar_campanas() -> pd.DataFrame:
    filas = [
        ("CMP01", "Liquidación de Verano", "Descuento porcentual", "Redes sociales",     "2026-01-10", "2026-02-28",  8_000_000),
        ("CMP02", "Vuelta a Clases",       "Descuento porcentual", "Correo electrónico", "2026-02-20", "2026-03-20",  5_000_000),
        ("CMP03", "Día de la Madre",       "Descuento porcentual", "Redes sociales",     "2026-05-01", "2026-05-10",  6_000_000),
        ("CMP04", "CyberDay",              "Descuento porcentual", "Sitio web",          "2026-06-01", "2026-06-03", 12_000_000),
        ("CMP05", "Fiestas Patrias",       "Descuento porcentual", "Televisión",         "2026-09-01", "2026-09-20", 10_000_000),
    ]
    return pd.DataFrame(
        filas,
        columns=["cod_campana", "nombre_campana", "tipo_promocion", "medio",
                 "fecha_inicio", "fecha_fin", "presupuesto"],
    )


# ------------------------------------------------------------------
# Ejecución
# ------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generando datos de origen en: {CARPETA_RAW}")
    guardar(generar_canales(), "canales.csv")
    guardar(generar_sucursales(), "sucursales.csv")
    guardar(generar_productos(), "productos.csv")
    guardar(generar_campanas(), "campanas.csv")
