"""Configurações do sistema RAIZ."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE, "database", "raiz.db")      # arquivo do banco SQLite
SQL_INICIAL = os.path.join(BASE, "database", "banco.sql")  # script que cria as tabelas
SECRET_KEY = "raiz-troque-esta-chave"                   # usada para proteger a sessão
