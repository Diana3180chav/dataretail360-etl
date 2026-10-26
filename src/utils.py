"""
utils.py
--------
Funciones comunes que usan todos los notebooks del pipeline:
logging, conexión a la base de datos y registro de control de cargas.
"""

import logging
import sys
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Connection, Engine

import config


def configurar_logging(nombre: str) -> logging.Logger:
    """Crea un logger que escribe en consola y en logs/etl_AAAAMMDD.log."""
    config.CARPETA_LOGS.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(nombre)

    # Si la celda se ejecuta dos veces, no agregamos los "handlers" de nuevo
    # (si no, cada mensaje aparecería repetido).
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    archivo = logging.FileHandler(
        config.CARPETA_LOGS / f"etl_{datetime.now():%Y%m%d}.log", encoding="utf-8"
    )
    consola = logging.StreamHandler(sys.stdout)
    for handler in (archivo, consola):
        handler.setFormatter(formato)
        logger.addHandler(handler)
    return logger


def obtener_motor() -> Engine:
    """Devuelve el 'motor' de SQLAlchemy conectado a la base SQLite del proyecto."""
    config.RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(config.URL_BD)


def tabla_existe(motor: Engine, nombre_tabla: str) -> bool:
    """Indica si una tabla ya existe en la base de datos."""
    return inspect(motor).has_table(nombre_tabla)


def registrar_control(conexion: Connection, id_lote: int, capa: str, tabla: str,
                      origen: str, filas: int, estado: str) -> None:
    """Agrega una fila a etl_control: la bitácora de cada carga realizada."""
    registro = pd.DataFrame([{
        "id_lote": id_lote,
        "capa": capa,
        "tabla": tabla,
        "origen": origen,
        "filas": filas,
        "estado": estado,
        "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])
    registro.to_sql("etl_control", conexion, if_exists="append", index=False)


def cargar_por_lote(motor: Engine, df: pd.DataFrame, tabla: str, id_lote: int,
                    capa: str, origen: str, logger: logging.Logger) -> int:
    """
    Carga un DataFrame en 'tabla' con recarga controlada:
    borra las filas del mismo lote y luego inserta las nuevas, en una sola transacción.
    """
    with motor.begin() as conexion:
        if tabla_existe(motor, tabla):
            resultado = conexion.execute(
                text(f"DELETE FROM {tabla} WHERE _id_lote = :lote"), {"lote": id_lote}
            )
            if resultado.rowcount > 0:
                logger.warning(f"{tabla}: el lote {id_lote} ya existía; "
                               f"se borraron {resultado.rowcount} filas antes de recargar")
        df.to_sql(tabla, conexion, if_exists="append", index=False)
        registrar_control(conexion, id_lote, capa, tabla, origen, len(df), "OK")
    logger.info(f"Cargado {tabla}: {len(df)} filas")
    return len(df)
