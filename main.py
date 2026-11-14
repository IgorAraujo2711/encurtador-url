import secrets
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI()

# "Banco de dados" temporário: código curto -> URL original
urls: dict[str, str] = {}

ALFABETO = string.ascii_letters + string.digits


class UrlEntrada(BaseModel):
    url: HttpUrl


def gerar_codigo(tamanho: int = 6) -> str:
    while True:
        codigo = "".join(secrets.choice(ALFABETO) for _ in range(tamanho))
        if codigo not in urls:
            return codigo


@app.get("/")
def raiz():
    return {"mensagem": "Encurtador de URL funcionando!"}


@app.post("/shorten")
def encurtar(entrada: UrlEntrada):
    codigo = gerar_codigo()
    urls[codigo] = str(entrada.url)
    return {
        "codigo": codigo,
        "url_curta": f"http://127.0.0.1:8000/{codigo}",
        "url_original": str(entrada.url),
    }


@app.get("/{codigo}")
def redirecionar(codigo: str):
    url = urls.get(codigo)
    if url is None:
        raise HTTPException(status_code=404, detail="Código não encontrado")
    return RedirectResponse(url=url, status_code=302)