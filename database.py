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
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                cliques INTEGER NOT NULL DEFAULT 0
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


def registrar_clique(codigo: str) -> None:
    with conectar() as conexao:
        conexao.execute(
            "UPDATE links SET cliques = cliques + 1 WHERE codigo = ?",
            (codigo,),
        )


def buscar_estatisticas(codigo: str) -> dict | None:
    with conectar() as conexao:
        linha = conexao.execute(
            "SELECT codigo, url_original, criado_em, cliques FROM links WHERE codigo = ?",
            (codigo,),
        ).fetchone()
    return dict(linha) if linha else None