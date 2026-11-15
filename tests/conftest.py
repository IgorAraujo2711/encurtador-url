import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Cada teste usa um banco temporário, separado do encurtador.db real
    monkeypatch.setattr(database, "NOME_BANCO", str(tmp_path / "teste.db"))
    database.criar_tabelas()
    return TestClient(app)