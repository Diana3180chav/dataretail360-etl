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
# 6. Clientes  (origen: Marketing / CRM)
# ------------------------------------------------------------------
# comuna: región (también se usa para validar la jerarquía Región › Comuna)
COMUNAS = {
    "Santiago": "Metropolitana", "Maipú": "Metropolitana", "Puente Alto": "Metropolitana",
    "Las Condes": "Metropolitana", "Ñuñoa": "Metropolitana", "La Florida": "Metropolitana",
    "Providencia": "Metropolitana", "Viña del Mar": "Valparaíso", "Valparaíso": "Valparaíso",
    "Antofagasta": "Antofagasta", "La Serena": "Coquimbo", "Coquimbo": "Coquimbo",
    "Concepción": "Biobío", "Talcahuano": "Biobío", "Temuco": "La Araucanía",
}
NOMBRES = ["Camila", "Valentina", "Francisca", "Javiera", "Constanza", "Catalina", "Fernanda",
           "Matías", "Benjamín", "Sebastián", "Nicolás", "Felipe", "Diego", "Tomás", "Joaquín"]
APELLIDOS = ["González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva",
             "Martínez", "Sepúlveda", "Morales", "Rodríguez", "López", "Fuentes", "Torres"]
SEGMENTOS = ["Nuevo", "Frecuente", "VIP"]


def generar_clientes(cantidad: int = 400) -> pd.DataFrame:
    comunas = list(COMUNAS.keys())
    # Más clientes en la Región Metropolitana, como en la realidad
    pesos = np.array([3 if COMUNAS[c] == "Metropolitana" else 1 for c in comunas], dtype=float)
    pesos /= pesos.sum()

    filas = []
    for i in range(1, cantidad + 1):
        nombre = f"{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)}"
        comuna = str(rng.choice(comunas, p=pesos))
        nacimiento = pd.Timestamp("1960-01-01") + pd.Timedelta(days=int(rng.integers(0, 365 * 45)))
        registro = pd.Timestamp("2020-01-01") + pd.Timedelta(days=int(rng.integers(0, 365 * 6)))
        filas.append({
            "id_cliente": f"CRM-{i:05d}",
            "nombre": nombre,                                   # dato personal
            "email": f"cliente{i:05d}@ejemplo.cl",              # dato personal (dominio ficticio)
            "fecha_nacimiento": nacimiento.strftime("%Y-%m-%d"),
            "comuna": comuna,
            "region": COMUNAS[comuna],
            "segmento": str(rng.choice(SEGMENTOS, p=[0.5, 0.35, 0.15])),
            "fecha_registro": registro.strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(filas)


# ------------------------------------------------------------------
# 7. Ventas de tiendas físicas  (origen: Comercial / sistema POS)
#    Formato: fecha AAAA-MM-DD, descuento en pesos, una fila por línea de boleta
# ------------------------------------------------------------------
def campana_vigente(fecha: pd.Timestamp, campanas: pd.DataFrame):
    """Devuelve el código de una campaña vigente en esa fecha, o None si no hay."""
    dia = fecha.strftime("%Y-%m-%d")
    # Las fechas en formato AAAA-MM-DD se pueden comparar directamente como texto
    vigentes = campanas[(campanas["fecha_inicio"] <= dia) & (campanas["fecha_fin"] >= dia)]
    if vigentes.empty:
        return None
    return str(vigentes.iloc[0]["cod_campana"])


def generar_ventas_tienda(productos, clientes, sucursales, campanas,
                          desde: str, hasta: str, cantidad_boletas: int,
                          primer_folio: int = 1) -> pd.DataFrame:
    fechas = pd.date_range(desde, hasta, freq="D")
    # Los fines de semana se vende el doble
    pesos_fecha = np.where(fechas.dayofweek >= 5, 2.0, 1.0)
    pesos_fecha /= pesos_fecha.sum()

    tiendas = sucursales[sucursales["tipo"] == "Física"]["cod_sucursal"].tolist()
    filas = []
    for k in range(cantidad_boletas):
        folio = f"B{primer_folio + k:07d}"
        fecha = fechas[rng.choice(len(fechas), p=pesos_fecha)]
        sucursal = str(rng.choice(tiendas))
        # 30% de las compras en tienda no identifica al cliente
        cliente = str(rng.choice(clientes["id_cliente"])) if rng.random() > 0.30 else ""
        campana = campana_vigente(fecha, campanas) if rng.random() < 0.5 else None
        pct_desc = rng.choice([0.10, 0.15, 0.20, 0.30]) if campana else 0.0
        # 1% de las boletas se anula; 2% corresponde a una nota de crédito (devolución)
        azar = rng.random()
        tipo_doc = "NOTA_CREDITO" if azar < 0.02 else "BOLETA"
        estado = "ANULADA" if 0.02 <= azar < 0.03 else "EMITIDA"

        n_lineas = int(rng.integers(1, 5))
        posiciones = rng.choice(len(productos), size=n_lineas, replace=False)
        for linea, pos in enumerate(posiciones, start=1):
            prod = productos.iloc[pos]
            cantidad = int(rng.choice([1, 1, 1, 2, 2, 3]))
            precio = int(prod["precio_lista"])
            filas.append({
                "nro_boleta": folio,
                "nro_linea": linea,
                "fecha": fecha.strftime("%Y-%m-%d"),
                "cod_sucursal": sucursal,
                "id_cliente": cliente,
                "cod_producto": prod["cod_producto"],
                "cantidad": cantidad,
                "precio_unitario": precio,
                "descuento": int(round(precio * cantidad * pct_desc)),
                "cod_campana": campana or "",
                "tipo_documento": tipo_doc,
                "estado": estado,
            })
    return pd.DataFrame(filas)


# ------------------------------------------------------------------
# 8. Ventas online  (origen: Canal digital / plataforma e-commerce)
#    Formato DISTINTO a propósito: fecha DD/MM/AAAA HH:MM, descuento en %,
#    nombres de columnas diferentes y estados propios del e-commerce.
# ------------------------------------------------------------------
def generar_ventas_online(productos, clientes, campanas,
                          desde: str, hasta: str, cantidad_pedidos: int,
                          primer_pedido: int = 1) -> pd.DataFrame:
    fechas = pd.date_range(desde, hasta, freq="D")
    filas = []
    for k in range(cantidad_pedidos):
        pedido = f"WEB-{primer_pedido + k:06d}"
        fecha = fechas[int(rng.integers(len(fechas)))] + pd.Timedelta(minutes=int(rng.integers(0, 1440)))
        canal = str(rng.choice(["WEB", "APP"], p=[0.6, 0.4]))
        cliente = str(rng.choice(clientes["id_cliente"]))        # online siempre hay cliente
        campana = campana_vigente(fecha.normalize(), campanas) if rng.random() < 0.6 else None
        pct = int(rng.choice([10, 15, 20, 30])) if campana else 0
        estado = str(rng.choice(["ENTREGADO", "CANCELADO", "DEVUELTO"], p=[0.94, 0.03, 0.03]))

        n_items = int(rng.integers(1, 4))
        posiciones = rng.choice(len(productos), size=n_items, replace=False)
        for item, pos in enumerate(posiciones, start=1):
            prod = productos.iloc[pos]
            filas.append({
                "id_pedido": pedido,
                "item": item,
                "fecha_pedido": fecha.strftime("%d/%m/%Y %H:%M"),
                "canal": canal,
                "cliente": cliente,
                "sku": prod["cod_producto"],
                "unidades": int(rng.choice([1, 1, 2])),
                "precio": int(prod["precio_lista"]),
                "dscto_pct": pct,
                "campana": campana or "",
                "estado_pedido": estado,
            })
    return pd.DataFrame(filas)


# ------------------------------------------------------------------
# 9. Inyección de errores de calidad (a propósito)
#    Cada error queda anotado para comprobar después que el ETL lo detecta.
# ------------------------------------------------------------------
def inyectar_errores_tienda(df: pd.DataFrame, registro: list) -> pd.DataFrame:
    df = df.copy()
    # Tipo "Int64" (con I mayúscula): entero que admite valores vacíos
    df["precio_unitario"] = df["precio_unitario"].astype("Int64")
    idx = rng.choice(df.index, size=40, replace=False)
    grupos = np.array_split(idx, 5)          # 5 tipos de error, 8 filas cada uno

    for i in grupos[0]:
        df.loc[i, "cantidad"] = -abs(int(df.loc[i, "cantidad"]))
        registro.append(("ventas_tienda", df.loc[i, "nro_boleta"], int(df.loc[i, "nro_linea"]), "Cantidad negativa en boleta"))
    for i in grupos[1]:
        df.loc[i, "fecha"] = str(rng.choice(["2026-02-30", "2026-13-05", "2026-04-31"]))
        registro.append(("ventas_tienda", df.loc[i, "nro_boleta"], int(df.loc[i, "nro_linea"]), "Fecha inválida"))
    for i in grupos[2]:
        df.loc[i, "cod_producto"] = "PRD9999"
        registro.append(("ventas_tienda", df.loc[i, "nro_boleta"], int(df.loc[i, "nro_linea"]), "Producto inexistente"))
    for i in grupos[3]:
        df.loc[i, "precio_unitario"] = pd.NA
        registro.append(("ventas_tienda", df.loc[i, "nro_boleta"], int(df.loc[i, "nro_linea"]), "Precio vacío"))
    # Filas duplicadas exactas (el POS envió dos veces la misma línea)
    duplicadas = df.loc[grupos[4]]
    for _, fila in duplicadas.iterrows():
        registro.append(("ventas_tienda", fila["nro_boleta"], int(fila["nro_linea"]), "Línea duplicada"))
    df = pd.concat([df, duplicadas]).sort_values(["nro_boleta", "nro_linea"]).reset_index(drop=True)
    return df


def inyectar_errores_online(df: pd.DataFrame, registro: list) -> pd.DataFrame:
    df = df.copy()
    idx = rng.choice(df.index, size=15, replace=False)
    grupos = np.array_split(idx, 3)

    for i in grupos[0]:
        df.loc[i, "cliente"] = "CRM-99999"
        registro.append(("ventas_online", df.loc[i, "id_pedido"], int(df.loc[i, "item"]), "Cliente inexistente"))
    for i in grupos[1]:
        df.loc[i, "unidades"] = 0
        registro.append(("ventas_online", df.loc[i, "id_pedido"], int(df.loc[i, "item"]), "Unidades en cero"))
    duplicadas = df.loc[grupos[2]]
    for _, fila in duplicadas.iterrows():
        registro.append(("ventas_online", fila["id_pedido"], int(fila["item"]), "Línea duplicada"))
    df = pd.concat([df, duplicadas]).sort_values(["id_pedido", "item"]).reset_index(drop=True)
    return df


def inyectar_errores_clientes(df: pd.DataFrame, registro: list) -> pd.DataFrame:
    df = df.copy()
    idx = rng.choice(df.index, size=20, replace=False)
    grupos = np.array_split(idx, 4)

    # Comuna escrita de forma inconsistente (minúsculas, sin tildes, espacios)
    for i in grupos[0]:
        df.loc[i, "comuna"] = f"  {df.loc[i, 'comuna'].lower().replace('ñ', 'n').replace('ú', 'u')} "
        registro.append(("clientes", df.loc[i, "id_cliente"], 0, "Comuna con formato inconsistente"))
    # Comuna asignada a una región que no le corresponde (rompe la jerarquía)
    for i in grupos[1]:
        df.loc[i, "region"] = "Valparaíso" if df.loc[i, "region"] != "Valparaíso" else "Biobío"
        registro.append(("clientes", df.loc[i, "id_cliente"], 0, "Región no coincide con la comuna"))
    # Fecha de nacimiento faltante
    for i in grupos[2]:
        df.loc[i, "fecha_nacimiento"] = ""
        registro.append(("clientes", df.loc[i, "id_cliente"], 0, "Fecha de nacimiento vacía"))
    # Clientes duplicados (el CRM exportó dos veces el mismo registro)
    duplicados = df.loc[grupos[3]]
    for _, fila in duplicados.iterrows():
        registro.append(("clientes", fila["id_cliente"], 0, "Cliente duplicado"))
    df = pd.concat([df, duplicados]).sort_values("id_cliente").reset_index(drop=True)
    return df


# ------------------------------------------------------------------
# Ejecución
# ------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generando datos de origen en: {CARPETA_RAW}")

    canales = generar_canales()
    sucursales = generar_sucursales()
    productos = generar_productos()
    campanas = generar_campanas()
    clientes = generar_clientes()

    guardar(canales, "canales.csv")
    guardar(sucursales, "sucursales.csv")
    guardar(productos, "productos.csv")
    guardar(campanas, "campanas.csv")

    # --- Lote 1: enero a junio de 2026 ---
    errores = []
    ventas_tienda = generar_ventas_tienda(productos, clientes, sucursales, campanas,
                                          "2026-01-01", "2026-06-30", cantidad_boletas=3000)
    ventas_online = generar_ventas_online(productos, clientes, campanas,
                                          "2026-01-01", "2026-06-30", cantidad_pedidos=1200)

    guardar(inyectar_errores_clientes(clientes, errores), "clientes.csv")
    guardar(inyectar_errores_tienda(ventas_tienda, errores), "ventas_tienda_lote1.csv")
    guardar(inyectar_errores_online(ventas_online, errores), "ventas_online_lote1.csv")

    # Registro de errores inyectados: queda FUERA de data/raw porque el ETL no debe verlo.
    # Sirve para comprobar en el informe que el ETL detectó todos los errores.
    df_errores = pd.DataFrame(errores, columns=["archivo", "registro", "linea", "tipo_error"])
    df_errores.to_csv(RAIZ / "data" / "errores_inyectados_lote1.csv", index=False, encoding="utf-8")
    print(f"[OK] errores_inyectados_lote1.csv: {len(df_errores)} errores anotados")
