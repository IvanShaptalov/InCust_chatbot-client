from data import config

# event creating
EVENT_CREATING_OPENED = f'Создание нового события:\nВведите имя'

OK_FOR_HANDLE_NAME = '✅, Введите заголовок'

OK_FOR_HANDLE_TITLE = '✅, Введите описание'

OK_FOR_HANDLE_DESCRIPTION = '✅, Выберите фото события'

SMALLER_THAT_3_SYMBOLS = '❌ Введите больше 3 символов.'

ERROR_WITH_MEDIA = '❌ Отправьте фото'

PHOTO_SAVED = '✅, Фото успешно добавлено!\nВведите дату в следующем формате:'

PHOTO_NOT_SAVED = '✅, При обработке фото произошла ошибка!'

DATE_INVALID = '❌ Вы ввели неправильно дату или дату окончания события правильный формат:\n'

LINKER_TO_SERVICE = f'Для того, чтобы получать уведомления о сообщениях перейдите в \n{config.SERVICE_BOT_LINK}\nи напишите /start'

EVENT_CREATED = f'Вы создали событие\n{LINKER_TO_SERVICE}'

# catalog
CATALOG_OPENED = f'Каталог'
SHOW_MORE = 'Показать больше'

DELETE_EVENT = 'Удалить событие'
SURE_DELETE = 'Вы уверены что хотите удалить событие?'
CONNECT_EVENT = 'Связаться'
EVENT_DELETED = 'Событие удалено'
DELETE_CANCELLED = 'Вы точно хотите удалить событие?'
EVENT_NOT_EXISTS = 'Событие удалено'

PLUS = '+{}'
"""{} - must be a number"""
# main menu

MAIN_MENU_OPENED = 'Добро пожаловать {}!'
"""{} - user fullname"""
# chat

ENTER_IN_CHAT = 'Вы вошли в чат с владельцем события {}'
"""{} - event_title"""
# service bot

NOTIFICATION = 'Сообщение "{}"\n{}: '
""" 1{} event title 2{} user_fullname(sender)"""
