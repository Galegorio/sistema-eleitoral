import sqlite3

NOME_BANCO = "eleicoes.db"


def conectar():
    return sqlite3.connect(NOME_BANCO)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eleitores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificacao TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleitor_id INTEGER NOT NULL,
            candidato_numero TEXT,
            tipo TEXT NOT NULL,

            FOREIGN KEY (eleitor_id)
                REFERENCES eleitores(id)
        )
    """)

    conexao.commit()
    conexao.close()

def inserir_candidatos():
    conexao = conectar()
    cursor = conexao.cursor()

    candidatos = {
        "13": "Lula",
        "22": "Flavio",
        "33": "Manoel Gomes",
        "10": "Amado Batista"
    }

    for numero, nome in candidatos.items():
        cursor.execute("""
            INSERT OR IGNORE INTO candidatos (numero, nome)
            VALUES (?, ?)
        """, (numero, nome))

    conexao.commit()
    conexao.close()

def buscar_candidatos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT numero, nome
        FROM candidatos
    """)

    candidatos = dict(cursor.fetchall())

    conexao.close()

    return candidatos

def eleitor_ja_votou(identificacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id
        FROM eleitores
        WHERE identificacao = ?
    """, (identificacao,))

    eleitor = cursor.fetchone()

    conexao.close()

    return eleitor is not None

def inserir_eleitor(identificacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO eleitores (identificacao)
        VALUES (?)
    """, (identificacao,))

    conexao.commit()

    eleitor_id = cursor.lastrowid

    conexao.close()

    return eleitor_id

def registrar_voto(eleitor_id, candidato_numero, tipo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO votos (eleitor_id, candidato_numero, tipo)
        VALUES (?, ?, ?)
    """, (eleitor_id, candidato_numero, tipo))

    conexao.commit()
    conexao.close()

def contar_votos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT candidato_numero, COUNT(*)
        FROM votos
        WHERE tipo = 'candidato'
        GROUP BY candidato_numero
    """)

    votos = dict(cursor.fetchall())

    conexao.close()

    return votos

def contar_votos_especiais():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT tipo, COUNT(*)
        FROM votos
        WHERE tipo IN ('branco', 'nulo')
        GROUP BY tipo
    """)

    resultados = dict(cursor.fetchall())

    conexao.close()

    return resultados