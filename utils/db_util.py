from typing import List
from icecream import ic
from sqlalchemy import Integer, Column, String, create_engine, BigInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import settings

path_alchemy_local = settings.alchemy_db_path
# test database
Base = declarative_base()


# region db engine
def create_db():
    engine_db = get_engine_by_path(engine_path=path_alchemy_local)
    Base.metadata.create_all(bind=engine_db)


def _get_session():
    engine_session = get_engine_by_path(engine_path=path_alchemy_local)
    session_creator = sessionmaker(bind=engine_session)
    return session_creator()


def get_engine_by_path(engine_path):
    """put db path to create orm engine"""
    # --echo back to true, show all sqlalchemy debug info
    engine_path = create_engine(engine_path, echo=False)
    return engine_path


session = _get_session()


# endregion


# region tables


class User(Base):
    __tablename__ = "user"

    chat_id = Column('chat_id', Integer, unique=True, primary_key=True, index=True)
    user_fullname = Column('username', String, unique=False)
    in_chat = Column('in_chat', Boolean, unique=False, default=False)
    events = relationship('Event', back_populates='event_owner')

    def __repr__(self):
        return '{}{}{}'.format(self.chat_id, self.statement, self.user_fullname)


class Event(Base):
    __tablename__ = 'event'

    id = Column('event_id', BigInteger, unique=True, primary_key=True, autoincrement=True, index=True)

    ev_name = Column('ev_name', String, unique=False)
    title = Column('title', String, unique=False)
    description = Column('description', String, unique=False)
    media = Column('media', String, unique=False)
    event_owner = relationship(User, back_populates="events")
    end_date = Column('end_date', DateTime, unique=False, nullable=True)

    # endregion


# region get_from_db methods


def get_from_db_multiple_filter(table_class, identifier_to_value: list, get_type='one',
                                all_objects: bool = None):
    """WARNING! DO NOT USE THIS OBJECT TO EDIT DATA IN DATABASE! IT ISN`T WORK!
    USE ONLY TO SHOW DATA...
    :param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one', return object or list of objects
    :param all_objects - return all rows from table"""
    many = 'many'
    one = 'one'
    with session:
        if all_objects is True:
            objects = session.query(table_class).all()

            return objects
        if get_type == one:
            obj = session.query(table_class).filter(*identifier_to_value).first()

            return obj
        elif get_type == many:
            objects = session.query(table_class).filter(*identifier_to_value).all()

            return objects


# endregion


# region abstract write


def write_obj_to_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    with session:
        is_new = False
        if identifier:
            tab_obj = session.query(table_class).filter(identifier == value).first()
        else:
            tab_obj = table_class()
            is_new = True

        # is obj not exist in db, we create them
        if not tab_obj:
            tab_obj = table_class()
            is_new = True
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
        # if obj created jet, we add his to db
        if is_new:
            session.add(tab_obj)
        # else just update
        session.commit()


def write_objects_to_table(table_class, object_list: List[dict], params_to_dict: list, params_to_db: list,
                           identifier_to_value: List):
    """column name to value must be exist in table class in columns write objects to db without close connection
    :param table_class - table class
    :param object_list
    :param params_to_dict - keys in object in objects_list
    :param params_to_db - names of attributes in database object
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute """
    # get obj
    with session:
        # is obj not exist in db, we create them
        for dict_obj in object_list:
            is_new = False
            tab_obj = get_from_db_multiple_filter(table_class=table_class, identifier_to_value=identifier_to_value)
            if not tab_obj:
                is_new = True
                tab_obj = table_class()
            for d_value, column in zip(params_to_dict, params_to_db):
                value = dict_obj[d_value]
                tab_obj.__setattr__(column, value)

            # if obj created jet, we add his to db
            if is_new:
                session.add(tab_obj)
                session.commit()
            else:
                # else just update
                session.commit()


# endregion


# region abstract edit
def edit_obj_in_table(table_class, identifier_to_value: list, **column_name_to_value):
    """edit object in selected table
    :param table_class - select table
    :param column_name_to_value to value must be exist in table class in columns
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    # get obj
    with session:
        tab_obj = session.query(table_class).filter(*identifier_to_value).first()

        if tab_obj:
            for col_name, val in column_name_to_value.items():
                tab_obj.__setattr__(col_name, val)
        session.commit()


# endregion


# region abstract delete from db
def delete_obj_from_table(table_class, identifier_to_value: list):
    """edit object in selected table
    :param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    with session:
        result = session.query(table_class).filter(*identifier_to_value).delete()
        ic('affected {} rows'.format(result))
        session.commit()


# endregion


# region arithmetics
def get_count(table_class, identifier_to_value: list = None):
    """get count of objects from custom table using filter (optional)
       :param table_class - select table
       :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
       note that UserStatements.statement is instrumented attribute"""
    with session:
        if identifier_to_value:
            rows = session.query(table_class).filter(*identifier_to_value).count()
        else:
            rows = session.query(table_class).count()

        return rows


def get_first(table_class):
    # work on func min
    with session:
        row = session.query(table_class).first()
        return row

# endregion
