# database.py
import sqlite3

DB_NAME = "cadastro.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datahora TEXT,
        nome TEXT,
        lote TEXT,
        placa TEXT,
        modelo TEXT,
        status TEXT,
        saidadatahora TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS encomendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datahora TEXT,
        destinatario TEXT,
        lote TEXT,
        codigo TEXT,
        status TEXT,
        horaentrega TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        lote TEXT,
        celular TEXT
    )
    """)

    conn.commit()
    conn.close()
