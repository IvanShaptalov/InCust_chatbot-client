import logging
from typing import List
from icecream import ic
from sqlalchemy import Column, String, create_engine, BigInteger, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from data import config

path_alchemy_local = config.ALCHEMY_DB_PATH

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

    chat_id = Column('chat_id', BigInteger, unique=True, primary_key=True, index=True)
    user_fullname = Column('username', String, unique=False)
    in_chat_client = Column('in_chat_client', Boolean, unique=False, default=False)
    in_chat_service = Column('in_chat_service', Boolean, unique=False, default=False)
    event = relationship('Event', back_populates='event_owner')

    def __str__(self):
        return f'{self.user_fullname} {self.chat_id} in_chat_client:{self.in_chat_client}, in_chat_service: {self.in_chat_service}'

    def save(self):
        user = get_from_db_multiple_filter(User,
                                           identifier_to_value=[User.chat_id == self.chat_id])
        if user is None:
            with session:
                user = write_obj_to_table(session_p=session,
                                          table_class=User,
                                          identifier_to_value=[User.chat_id == self.chat_id],
                                          chat_id=self.chat_id,
                                          user_fullname=self.user_fullname,
                                          in_chat_client=self.in_chat_client,
                                          in_chat_service=self.in_chat_service)

    @staticmethod
    def set_in_chat(chat_id, in_chat: bool, service_or_client: str = 'client'):
        """
        set user in chat
        :param chat_id: user chat id
        :param in_chat: set True if user enter in chat
        :param service_or_client: select chat, 'service' to service, 'client' to client
        :return:
        """
        client = 'client'
        service = 'service'
        assert service_or_client == client or service_or_client == service

        with session:
            if service_or_client == service:
                edit_obj_in_table(session_p=session,
                                  table_class=User,
                                  identifier_to_value=[User.chat_id == chat_id],
                                  in_chat_service=in_chat)
                return
            elif service_or_client == client:
                edit_obj_in_table(session_p=session,
                                  table_class=User,
                                  identifier_to_value=[User.chat_id == chat_id],
                                  in_chat_client=in_chat)


class Event(Base):
    __tablename__ = 'event'

    id = Column('event_id', BigInteger, unique=True, primary_key=True, index=True)
    previous_event_id = Column('previous_event_id', BigInteger, unique=False)
    next_event_id = Column('next_event_id', BigInteger, unique=False)
    ev_name = Column('ev_name', String, unique=False)
    title = Column('title', String, unique=False)
    description = Column('description', String, unique=False)
    media = Column('media', String, unique=False)
    event_owner_id = Column('event_owner_id', BigInteger, ForeignKey('user.chat_id'), unique=False)
    event_owner = relationship(User, back_populates='event')
    end_date = Column('end_date', DateTime, unique=False, nullable=True)

    def delete(self):
        with session:
            edit_obj_in_table(session, Event, [Event.id == self.previous_event_id],
                              next_event_id=self.next_event_id)
            edit_obj_in_table(session, Event, [Event.id == self.next_event_id],
                              previous_event_id=self.previous_event_id)
            session.commit()
            delete_obj_from_table(session, Event, [Event.id == self.id])

    def get_owner(self) -> User:
        return self.event_owner

    def save(self):
        with session:
            # get prev_event to link to new event
            prev_event = get_by_max(Event, Event.id)
            self.event_owner.save()
            obj = write_obj_to_table(session_p=session,
                                     table_class=Event,
                                     ev_name=self.ev_name,
                                     title=self.title,
                                     description=self.description,
                                     media=self.media,
                                     end_date=self.end_date,
                                     event_owner_id=self.event_owner_id)
            assert isinstance(obj, Event)
            # get previous id from event or get 0 if previous event not exists
            event_prev_id = None
            if isinstance(prev_event, Event):
                event_prev_id = prev_event.id
            edit_obj_in_table(session, Event, [Event.id == obj.id],
                              next_event_id=obj.id + 1,  # next user id
                              previous_event_id=event_prev_id if event_prev_id else -1)  # previous user id
            logging.info('event saved')

    @staticmethod
    def get_next_event(start_event_id: int, count_of_events: int = 1) -> list:
        events = []
        event = None
        for c in range(count_of_events):
            if len(events) == 0:
                event = get_from_db_multiple_filter(Event, [Event.id == start_event_id])
                events.append(event)
                continue
            if event:
                event = get_from_db_multiple_filter(Event, [Event.id == event.previous_event_id])
                if isinstance(event, Event):
                    events.append(event)
                else:
                    break
        return events

    def stringify(self):
        return f'{self.title}\n\n' \
               f'{self.description}\n\n'

    def get_media(self):
        return self.media

    def __str__(self):
        return f'{self.ev_name} {self.title} {self.event_owner.user_fullname}'

    # endregion


# region get_from_db methods


def get_from_db_multiple_filter(table_class, identifier_to_value: list = None, get_type='one',
                                all_objects: bool = None, open_session=None):
    """:param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one', return object or list of objects
    :param all_objects - return all rows from table\
    :param open_session - leave session open , must be a session"""
    many = 'many'
    one = 'one'
    is_open = False
    if open_session:
        inner_session = open_session
    else:
        inner_session = session
    try:
        objects = None
        if all_objects is True:
            objects = inner_session.query(table_class).all()

            return objects
        if get_type == one:
            obj = inner_session.query(table_class).filter(*identifier_to_value).first()

            return obj
        elif get_type == many:
            objects = inner_session.query(table_class).filter(*identifier_to_value).all()
    finally:
        if open_session is None:
            inner_session.close()
    return objects


# endregion


# region abstract write


def write_obj_to_table(session_p, table_class, identifier_to_value: List = None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    is_new = False
    if identifier_to_value:
        tab_obj = session_p.query(table_class).filter(*identifier_to_value).first()
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
        session_p.add(tab_obj)
    # else just update
    session_p.commit()
    return tab_obj


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
def edit_obj_in_table(session_p, table_class, identifier_to_value: list, **column_name_to_value):
    """edit object in selected table
    :param table_class: select table
    :param column_name_to_value: to value must be exist in table class in columns
    :param session_p: connection to database
    :param identifier_to_value: select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    # get obj
    tab_obj = session_p.query(table_class).filter(*identifier_to_value).first()

    if tab_obj:
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
    session_p.commit()


# endregion


# region abstract delete from db
def delete_obj_from_table(session_p, table_class, identifier_to_value: list):
    """edit object in selected table
    :param table_class: select table
    :param session_p: connection to database
    :param identifier_to_value:  select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute"""
    result = session_p.query(table_class).filter(*identifier_to_value).delete()
    ic('affected {} rows'.format(result))
    session_p.commit()


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


def get_by_max(table_class, column):
    # work on func min
    with session:
        max_id = session.query(func.max(column)).scalar()
        if not isinstance(max_id, int):
            max_id = 0
        assert isinstance(max_id, int)
        row = session.query(table_class).filter(column == max_id).first()
        # row = session.query(table_class).filter(func.max(column)).first()
        return row

# endregion
