def criar_link(client, url="https://www.python.org"):
    resposta = client.post("/shorten", json={"url": url})
    assert resposta.status_code == 200
    return resposta.json()


def test_raiz(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()


def test_encurtar_url_valida(client):
    dados = criar_link(client)
    assert len(dados["codigo"]) == 6
    assert dados["url_original"] == "https://www.python.org/"


def test_encurtar_url_invalida(client):
    resposta = client.post("/shorten", json={"url": "banana"})
    assert resposta.status_code == 422


def test_redireciona_para_url_original(client):
    dados = criar_link(client)
    resposta = client.get(f"/{dados['codigo']}", follow_redirects=False)
    assert resposta.status_code == 302
    assert resposta.headers["location"] == "https://www.python.org/"


def test_codigo_inexistente_retorna_404(client):
    resposta = client.get("/naoexiste", follow_redirects=False)
    assert resposta.status_code == 404


def test_contador_de_cliques(client):
    dados = criar_link(client)
    for _ in range(3):
        client.get(f"/{dados['codigo']}", follow_redirects=False)

    resposta = client.get(f"/stats/{dados['codigo']}")
    assert resposta.status_code == 200
    assert resposta.json()["cliques"] == 3


def test_stats_de_codigo_inexistente_retorna_404(client):
    resposta = client.get("/stats/naoexiste")
    assert resposta.status_code == 404