from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_buscar_tarefa_inexistente(override_db):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    

def test_criar_usuario(override_db):
    response = client.post(
        "/users",
        json={"name": "Usuario Teste"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Usuario Teste"


def test_criar_tarefa(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario da Tarefa"}
    )

    assert usuario.status_code == 200

    user_id = usuario.json()["id"]

    response = client.post(
        "/tasks",
        json={
            "title": "Estudar pytest",
            "description": "Aprender testes automatizados",
            "priority": 1,
            "user_id": user_id
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Estudar pytest"
    assert response.json()["user_id"] == user_id

def test_criar_tarefa_prioridade_invalida(override_db):
    response = client.post(
        "/tasks",
        json={
            "title": "Tarefa inválida",
            "description": "Prioridade fora do intervalo",
            "priority": 5,
            "user_id": 1
        }
    )

    assert response.status_code == 422

def test_criar_tarefa_usuario_inexistente(override_db):
    response = client.post(
        "/tasks",
        json={
            "title": "Tarefa sem usuário",
            "description": "Teste de usuário inexistente",
            "priority": 1,
            "user_id": 999999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"

def test_atualizar_tarefa(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario Atualizacao"}
    )

    user_id = usuario.json()["id"]

    tarefa = client.post(
        "/tasks",
        json={
            "title": "Tarefa original",
            "description": "Antes da atualização",
            "priority": 0,
            "user_id": user_id
        }
    )

    task_id = tarefa.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarefa atualizada",
            "description": "Depois da atualização",
            "completed": True,
            "priority": 2
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa atualizada"
    assert response.json()["completed"] is True
    assert response.json()["priority"] == 2

def test_excluir_tarefa(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario Exclusao"}
    )

    user_id = usuario.json()["id"]

    tarefa = client.post(
        "/tasks",
        json={
            "title": "Tarefa para excluir",
            "description": "Teste de exclusão",
            "priority": 1,
            "user_id": user_id
        }
    )

    task_id = tarefa.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Tarefa removida com sucesso"

    consulta = client.get(f"/tasks/{task_id}")

    assert consulta.status_code == 404

def test_listar_usuarios(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario Listagem"}
    )

    assert usuario.status_code == 200

    user_id = usuario.json()["id"]

    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert any(
        item["id"] == user_id
        and item["name"] == "Usuario Listagem"
        for item in response.json()
    )

def test_listar_tarefas(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario Listagem Tarefas"}
    )

    assert usuario.status_code == 200
    user_id = usuario.json()["id"]

    tarefa = client.post(
        "/tasks",
        json={
            "title": "Tarefa para listagem",
            "description": "Testando GET tasks",
            "priority": 1,
            "user_id": user_id
        }
    )

    assert tarefa.status_code == 200
    task_id = tarefa.json()["id"]

    response = client.get("/tasks", params={"limit": 100})

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert any(
        item["id"] == task_id
        and item["title"] == "Tarefa para listagem"
        for item in response.json()
    )

def test_filtrar_tarefas_pendentes(override_db):
    usuario = client.post(
        "/users",
        json={"name": "Usuario Filtro"}
    )

    user_id = usuario.json()["id"]

    tarefa = client.post(
        "/tasks",
        json={
            "title": "Tarefa pendente para filtro",
            "description": "Testar filtro completed",
            "priority": 1,
            "user_id": user_id
        }
    )

    assert tarefa.status_code == 200
    task_id = tarefa.json()["id"]

    response = client.get(
        "/tasks",
        params={"completed": False, "limit": 100}
    )

    assert response.status_code == 200

    assert any(
        item["id"] == task_id
        for item in response.json()
    )

    assert all(
        item["completed"] is False
        for item in response.json()
    )