from sqlalchemy import select

from models import Task



def get_task(session, task_id, user_id):
    statement = (
        select(Task)
        .where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )

    return session.scalars(statement).first()

def get_tasks(session, user_id):
    statement = (
        select(Task)
        .where(
            Task.user_id == user_id
        )
    )

    return session.scalars(statement).all()


def create_task(session, title, user_id):
    task = Task(
        title=title,
        user_id=user_id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task



def update_task(session, task, completed):
    task.completed = completed

    session.commit()
    session.refresh(task)

    return task



def delete_task(session, task):
    session.delete(task)
    session.commit()