from fastapi.testclient import TestClient

from api import app
from database import get_session
from test_database import TestingSessionLocal
from models import User, Task

app.dependency_overrides[get_session] = lambda: TestingSessionLocal()

client = TestClient(app)


def test_get_tasks_requires_authentication():
    response = client.get("/tasks")

    assert response.status_code == 401

def test_user_gets_own_tasks():
    session = TestingSessionLocal()

    user = User(
        username="api_test_user",
        password="fake_password"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    task = Task(
        title="API Test Task",
        user=user
    )

    session.add(task)
    session.commit()

    # Create a token for this user
    from auth import create_access_token

    token = create_access_token(user.id)

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "API Test Task"

    session.close()


def test_user_cannot_see_other_users_tasks():
    session = TestingSessionLocal()

    user1 = User(
        username="api_user1",
        password="fake_password"
    )

    user2 = User(
        username="api_user2",
        password="fake_password"
    )

    session.add_all([user1, user2])
    session.commit()

    task1 = Task(
        title="User 1 Private Task",
        user=user1
    )

    task2 = Task(
        title="User 2 Private Task",
        user=user2
    )

    session.add_all([task1, task2])
    session.commit()

    from auth import create_access_token

    token = create_access_token(user1.id)

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "User 1 Private Task"

    session.close()


def test_user_cannot_update_other_users_task():
    session = TestingSessionLocal()

    user1 = User(
        username="update_user1",
        password="fake_password"
    )

    user2 = User(
        username="update_user2",
        password="fake_password"
    )

    session.add_all([user1, user2])
    session.commit()

    task = Task(
        title="User 2 Private Task",
        user=user2
    )

    session.add(task)
    session.commit()

    from auth import create_access_token

    token = create_access_token(user1.id)

    response = client.put(
        f"/tasks/{task.id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "completed": True
        }
    )

    assert response.status_code == 404

    session.close()


def test_user_cannot_delete_other_users_task():
    session = TestingSessionLocal()

    user1 = User(
        username="delete_user1",
        password="fake_password"
    )

    user2 = User(
        username="delete_user2",
        password="fake_password"
    )

    session.add_all([user1, user2])
    session.commit()

    task = Task(
        title="User 2 Private Task",
        user=user2
    )

    session.add(task)
    session.commit()

    from auth import create_access_token

    token = create_access_token(user1.id)

    response = client.delete(
        f"/tasks/{task.id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    session.close()

def test_user_can_create_task():
    session = TestingSessionLocal()

    user = User(
        username="create_task_user",
        password="fake_password"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    from auth import create_access_token

    token = create_access_token(user.id)

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "New API Task"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "New API Task"
    assert data["completed"] is False

    session.close()
