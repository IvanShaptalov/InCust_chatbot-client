import logging
from abc import abstractmethod
from copy import copy

from aiogram import types

import filters.filters
import keyboards.reply.r_snippets
from data import text_util, config
from data.bot_setup import client_bot
from models import db


class BaseSender:

    def __init__(self, event_id, sender_id):
        self.event_id = event_id
        self.sender_id = sender_id
        self.event, self._owner = self._get_event()
        self.sender = self._get_sender()

    def get_owner(self) -> db.User:
        return self._owner

    def _get_event(self):
        session = db.session
        with session:
            event = db.get_from_db_multiple_filter(table_class=db.Event,
                                                   identifier_to_value=[db.Event.id == self.event_id],
                                                   open_session=session)
            assert isinstance(event, db.Event)
            owner = copy(event.event_owner)
            return event, owner

    def _get_sender(self) -> db.User:
        sender = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == self.sender_id])
        assert isinstance(sender, db.User)
        return sender

    def prepare_to_send(self):
        text = text_util.NOTIFICATION.format(self.event.title, self.sender.user_fullname)
        return text

    @abstractmethod
    def forward_data(self, data):
        pass


class TextSender(BaseSender):
    def __init__(self, event_id, sender_id):
        super().__init__(event_id, sender_id)

    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        with client_bot.with_token(config.SERVICE_BOT_TOKEN):
            chat_id = self.get_owner().chat_id
            markup = None
            if not filters.filters.user_in_chat(chat_id):
                markup = keyboards.reply.r_snippets.main_menu()
            text = "{} {}".format(self.prepare_to_send(), data.text)
            try:
                await client_bot.send_message(chat_id=chat_id,
                                              text=text,
                                              reply_markup=markup)
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await client_bot.send_message(chat_id=self.sender_id,
                                          text=text_util.LINKER_TO_SERVICE)


class LocationSender(BaseSender):
    def __init__(self, event_id, sender_id):
        super().__init__(event_id, sender_id)

    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        with client_bot.with_token(config.SERVICE_BOT_TOKEN):
            chat_id = self.get_owner().chat_id
            markup = None
            if not filters.filters.user_in_chat(chat_id):
                markup = keyboards.reply.r_snippets.main_menu()

            text = "{}".format(self.prepare_to_send())
            try:
                await client_bot.send_message(chat_id=chat_id,
                                              text=text,
                                              reply_markup=markup)
                await client_bot.send_location(chat_id=chat_id,
                                               latitude=data.location.latitude,
                                               longitude=data.location.longitude)
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await client_bot.send_message(chat_id=self.sender_id,
                                          text=text_util.LINKER_TO_SERVICE)
