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

def salvar_link(codigo: str, url_original: str) -> None:
    with conectar() as conexao:
        conexao.execute(
            "INSERT INTO links (codigo, url_original) VALUES (?, ?)",
            (codigo, url_original),
        )


def buscar_link(codigo: str) -> str | None:
    with conectar() as conexao:
        linha = conexao.execute(
            "SELECT url_original FROM links WHERE codigo = ?",
            (codigo,),
        ).fetchone()
    return linha["url_original"] if linha else None