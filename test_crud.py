from models import User, Task
from crud import get_tasks, get_task


def test_real_user_ownership(session):
    user1 = User(
        username="pytest_user1",
        password="fake_password"
    )

    user2 = User(
        username="pytest_user2",
        password="fake_password"
    )

    session.add_all([user1, user2])
    session.commit()

    task1 = Task(
        title="User 1 Task",
        user=user1
    )

    task2 = Task(
        title="User 2 Task",
        user=user2
    )

    session.add_all([task1, task2])
    session.commit()

    tasks = get_tasks(session, user1.id)

    assert len(tasks) == 1
    assert tasks[0].title == "User 1 Task"
    assert tasks[0].user_id == user1.id


def test_user_cannot_access_other_users_task(session):
    user1 = User(
        username="owner",
        password="fake_password"
    )

    user2 = User(
        username="other_user",
        password="fake_password"
    )

    session.add_all([user1, user2])
    session.commit()

    task = Task(
        title="Private Task",
        user=user2
    )

    session.add(task)
    session.commit()

    result = get_task(
        session,
        task.id,
        user1.id
    )

    assert result is None
