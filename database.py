import sqlite3

NOME_BANCO = "encurtador.db"


def conectar() -> sqlite3.Connection:
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conexao


def criar_tabelas() -> None:
    with conectar() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                codigo TEXT PRIMARY KEY,
                url_original TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )