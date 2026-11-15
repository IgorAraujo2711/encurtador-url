# Encurtador de URL

Projeto acadêmico de um encurtador de URLs feito com Python e FastAPI, criado para estudar desenvolvimento de APIs, banco de dados e boas práticas de engenharia de software.

## Status

Em desenvolvimento. Hoje os links ficam guardados em memória, então são perdidos quando o servidor reinicia.

## Funcionalidades

- [x] Encurtar uma URL (`POST /shorten`)
- [x] Redirecionar pelo código curto (`GET /{codigo}`)
- [x] Validação da URL recebida
- [x] Persistência em banco de dados (SQLite)
- [ ] Contador de cliques
- [ ] Expiração de links
- [ ] Alias personalizado
- [ ] Testes automatizados
- [ ] Docker
- [ ] Deploy

## Tecnologias

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic

## Como rodar

```bash
git clone https://github.com/IgorAraujo2711/encurtador-url.git
cd encurtador-url
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows (PowerShell)
# source .venv/bin/activate     # macOS/Linux
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000` e a documentação interativa em `http://127.0.0.1:8000/docs`.

## Exemplo de uso

Criar um link curto:

```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.python.org"}'
```

Resposta:

```json
{
  "codigo": "aB3xK9",
  "url_curta": "http://127.0.0.1:8000/aB3xK9",
  "url_original": "https://www.python.org/"
}
```

Abrir `http://127.0.0.1:8000/aB3xK9` redireciona para a URL original.

## Decisões técnicas

- **Código curto:** 6 caracteres aleatórios (letras e números) gerados com o módulo `secrets`, verificando se o código já existe para evitar colisões.
- **Redirecionamento 302:** permite contar cliques depois, pois o navegador não guarda o redirecionamento em cache como faria com o 301.

## Autor

Igor de Araujo ([@IgorAraujo2711](https://github.com/IgorAraujo2711))