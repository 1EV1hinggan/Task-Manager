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


def create_task(session, title, user):
    try:
        task = Task(
            title=title,
            user=user
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    except:
        session.rollback()
        raise



def update_task(session, task, completed):
    try:
        task.completed = completed

        session.commit()
        session.refresh(task)

        return task
    except:
        session.rollback()
        raise


def delete_task(session, task):
    try:
        session.delete(task)
        session.commit()
    except:
        session.rollback()
        raise
