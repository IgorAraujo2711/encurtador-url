import secrets
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

import database

app = FastAPI()

ALFABETO = string.ascii_letters + string.digits


@app.on_event("startup")
def iniciar() -> None:
    database.criar_tabelas()


class UrlEntrada(BaseModel):
    url: HttpUrl


def gerar_codigo(tamanho: int = 6) -> str:
    while True:
        codigo = "".join(secrets.choice(ALFABETO) for _ in range(tamanho))
        if database.buscar_link(codigo) is None:
            return codigo


@app.get("/")
def raiz():
    return {"mensagem": "Encurtador de URL funcionando!"}


@app.post("/shorten")
def encurtar(entrada: UrlEntrada):
    codigo = gerar_codigo()
    database.salvar_link(codigo, str(entrada.url))
    return {
        "codigo": codigo,
        "url_curta": f"http://127.0.0.1:8000/{codigo}",
        "url_original": str(entrada.url),
    }


@app.get("/{codigo}")
def redirecionar(codigo: str):
    url = database.buscar_link(codigo)
    if url is None:
        raise HTTPException(status_code=404, detail="Código não encontrado")
    return RedirectResponse(url=url, status_code=302)