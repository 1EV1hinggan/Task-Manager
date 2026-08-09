from sqlalchemy import select

from models import Task



def get_tasks(session):
    statement = select(Task).order_by(Task.id)
    return session.scalars(statement).all()



def get_task(session, task_id):
    return session.get(Task, task_id)



def create_task(session, title):
    task = Task(title=title)

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