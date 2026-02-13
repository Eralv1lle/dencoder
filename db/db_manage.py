from db.models import Data, Session, engine
from sqlalchemy import select, Sequence


def create_data(data: Data, session: Session) -> None:
    session.add(data)

def get_all(session: Session) -> Sequence:
    return session.scalars(select(Data)).all()

def get_by_id(data_id: int, session: Session) -> Data:
    statement = select(Data).where(Data.id == data_id)
    return session.scalars(statement).one()

def update(new_obj: Data, session: Session) -> None:
    session.merge(new_obj)

def delete(data_id: int, session: Session) -> Data:
    statement = select(Data).where(Data.id == data_id)
    db_obj = session.scalars(statement).one()

    session.delete(db_obj)
    return db_obj

