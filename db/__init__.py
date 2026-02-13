from .models import Base, engine, Session
from .db_manage import create_data, get_all, get_by_id, update, delete

Base.metadata.create_all(engine)