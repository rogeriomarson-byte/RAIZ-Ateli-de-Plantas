"""Conexão com o banco SQLite."""
import os
import sqlite3
from contextlib import contextmanager
import config


@contextmanager
def conectar():
    """Abre a conexão, salva (commit) se deu certo e desfaz (rollback) se deu erro."""
    con = sqlite3.connect(config.BANCO)
    con.row_factory = sqlite3.Row                # permite usar linha["nome"]
    con.execute("PRAGMA foreign_keys = ON")      # ativa as chaves estrangeiras
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def iniciar():
    """Na primeira execução cria o banco a partir do banco.sql."""
    if os.path.exists(config.BANCO):
        return
    try:
        with open(config.SQL_INICIAL, encoding="utf-8") as f:
            with conectar() as con:
                con.executescript(f.read())
    except Exception:
        if os.path.exists(config.BANCO):
            os.remove(config.BANCO)
        raise
