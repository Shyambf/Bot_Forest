from webbrowser import get
from xml.dom.expatbuilder import ExpatBuilder
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, \
    ConversationHandler, Filters, CallbackQueryHandler
from src.main import pattern_photo
from os import remove, path, environ
from src.sql_api import Bd
from src.progress_msg import ProgressMsg
from dotenv import load_dotenv

class ST:
    keyboard = [[InlineKeyboardButton("закрыть это сообщение", callback_data='del')], [InlineKeyboardButton("Отмена", callback_data='chatcancel')]]
    id = int()
    adname = int()


class bot:
    def __init__(self):
        self.bot = Updater(environ.get("TOKEN"))
        self.dispatcher = self.bot.dispatcher
        self.sql = Bd()
        self.dicts = dict()
        self.chat = ConversationHandler(
            entry_points=[CommandHandler('new', self.new)],
            states={
                1: [MessageHandler(Filters.all, self.name)],
                3: [MessageHandler(Filters.all, self.year)],
                4: [MessageHandler(Filters.all, self.date)],
                6: [CallbackQueryHandler(Filters.all, self.city)],
                7: [MessageHandler(Filters.all, self.signs)],
                8: [MessageHandler(Filters.all, self.special_signs)],
                9: [MessageHandler(Filters.all, self.clothes)],
                10: [MessageHandler(Filters.all, self.med_pomosch)],
                11: [MessageHandler(Filters.all, self.end),],
            },
            fallbacks=[CallbackQueryHandler(self.chat_cancel, pattern=r'^chatcancel$')]
        )
        self.dispatcher.add_handler(self.chat)
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.newad = ConversationHandler(
            entry_points=[CommandHandler('new_admin', self.new_admin)],
            states={
                1: [MessageHandler(Filters.all, self.new_id)],
                2: [MessageHandler(Filters.all, self.new_name)],
            },
            fallbacks=[CallbackQueryHandler(self.chat_cancel, pattern=r'^chatcancel$')]
        )
        self.dispatcher.add_handler(self.newad)
        self.dispatcher.add_handler(CommandHandler('admins', self.list_ticher))
        self.dispatcher.add_handler(CallbackQueryHandler(self.list_ticher, pattern=r'^list_ticher \d*$'))
        self.dispatcher.add_handler(CallbackQueryHandler(self.delm, pattern=r'^del$'))
        self.dispatcher.add_handler(CallbackQueryHandler(self.user_info, pattern=r'^get_user_info \d* \d*$'))
        self.dispatcher.add_handler(CallbackQueryHandler(self.delete_ticher, pattern=r'^deltich \d* \d*$'))

    def delm(self, update: Update, context: CallbackContext):
        update.callback_query.message.delete()

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(f'Приветствуем Вас в боте Forest\nФункционал нашего бота доступен только админам, для\nполучения статуса админа пишите в лс @skylin37\nВаш ID: {update.message.chat_id}\n\n1) /new - создать новое объявление\n2) /admins - вывести список всех админов\n3) /new_admin - добавить нового админа')

    def new_admin(self, update: Update, context: CallbackContext):
        flag = False
        try:
            flag = self.sql.chek(update.message.chat_id)
        except:
            flag = self.sql.chek(update.callback_query.message.chat_id)
        if flag:
            update.message.reply_text('Начинаем добавлять админа\nВведите его id (его можно узнать через эту же команду от его имени)', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
            return 1
        else:
            update.message.reply_text(f'Вы не можете использовать данную команду\nВаш ID: {update.message.chat_id}')
        return ConversationHandler.END

    def delete_ticher(self, update:Update, context:CallbackContext):
        _, id, page = update.callback_query.data.split()
        self.sql.del_admin(id)
        keym = [
                [InlineKeyboardButton(f'назад', callback_data=f'list_ticher {page}')]
        ]
        update.callback_query.message.edit_text(f'Удалён')
        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keym, one_time_keyboard=False, resize_keyboard=True))

    def user_info(self, update:Update, context:CallbackContext):
        _, user_pk, page = update.callback_query.data.split()
        user_pk = int(user_pk)
        ticher = self.sql.get_one_admin(user_pk)
        id = ticher[0][0]
        name = ticher[0][1]
        keym = [
                [InlineKeyboardButton(f'удалить', callback_data=f'deltich {user_pk} {page}')],
                [InlineKeyboardButton(f'назад', callback_data=f'list_ticher {page}')]
        ]
        update.callback_query.message.edit_text(f'Администратор {name}\nid: {id}')
        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keym, one_time_keyboard=False, resize_keyboard=True))

    def list_ticher(self, update: Update, context: CallbackContext):
        flag = False
        try:
            flag = self.sql.chek(update.message.chat_id)
        except:
            flag = self.sql.chek(update.callback_query.message.chat_id)
        if flag:
            if update.callback_query:
                uid = update.callback_query.message.chat.id
            else:
                uid = update.message.chat.id
            list_bottuns = self.sql.get_admins()
            if list_bottuns:
                page = 0
                if update.callback_query:
                    try:
                        _, readpage = update.callback_query.data.split()
                        page = int(readpage)
                    except Exception:
                        pass
                object_in_page = 5
                ticher = []
                for i in list_bottuns[object_in_page*page:object_in_page*page + object_in_page]:
                    name = i[1]
                    pk = i[0]
                    ticher.append([InlineKeyboardButton(name, callback_data=f'get_user_info {pk} {page}')])
                prevnext = list()
                if page > 0:
                    prevnext.append(InlineKeyboardButton(f'{page} <<', callback_data=f'list_ticher {page-1}'))
                if len(list_bottuns) > object_in_page * (page + 1):
                    prevnext.append(InlineKeyboardButton(f'>> {page+2}', callback_data=f'list_ticher {page+1}'))
                if prevnext:
                    ticher.append(prevnext)
                ticher.append([InlineKeyboardButton(f'Закрыть', callback_data=f'del')])
                if update.callback_query:
                    update.callback_query.message.edit_text('Все администраторы:')
                    # ,reply_markup=InlineKeyboardMarkup(ST.page2,one_time_keyboard=False, resize_keyboard=True))
                    update.callback_query.message.edit_reply_markup(
                        reply_markup=InlineKeyboardMarkup(ticher, one_time_keyboard=False, resize_keyboard=True))
                else:
                    update.message.reply_text("Все администраторы:", reply_markup=InlineKeyboardMarkup(ticher,one_time_keyboard=False, resize_keyboard=True))
                    update.message.delete()

            else:
                if update.callback_query:
                    update.callback_query.message.edit_text('Администраторов нет')
                else:
                    update.message.reply_text('Администраторов нет')

        else:
            update.message.reply_text(f'Вы не можете использовать данную команду\nВаш ID: {update.message.chat_id}')

    def new_id(self, update: Update, context: CallbackContext):
        ST.id = int(update.message.text)
        update.message.reply_text('теперь его имя', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 2

    def new_name(self, update: Update, context: CallbackContext):
        ST.adname = update.message.text
        if self.sql.chek(ST.id):
            update.message.reply_text('данный пользователь уже есть', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
            return ConversationHandler.END
        else:
            self.sql.add_admin(ST.id, ST.adname)
            update.message.reply_text(f'{ST.adname} добавлен в базу', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
            return ConversationHandler.END

    def new(self, update: Update, context: CallbackContext):
        if self.sql.chek(update.message.chat_id):
            ST.image_old = str(update.message.chat_id) + '.png'
            update.message.reply_text('Вы приступили к созданию обьявлениея о пропаже.\nОтправьте пожалуйста фото того человека который пропал.\nв вертикальной ориентации документом', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
            return 1
        else:
            update.message.reply_text(f'вы не можете использовать данную команду\nВаш ID: {update.message.chat_id}')
        return ConversationHandler.END

    def name(self, update: Update, context: CallbackContext):
        try:
            f = context.bot.getFile(update.message.document.file_id)
            f.download(f'./{update.message.chat_id}.png')
        except:
            f = context.bot.getFile(update.message.photo[-1].file_id)
            f.download(f'./{update.message.chat_id}.png')
        update.message.reply_text(f'Ок\nТеперь введите ФИО пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 3

    def year(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid] = {}
        self.dicts[uid]['name'] = update.message.text
        
        update.message.reply_text('Теперь ввидите сколько лет пропавшему\nпример:"30 лет"', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 4
    
    def date(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['yo'] = update.message.text
        update.message.reply_text('Теперь дату когда пропал человек\nпример:"25.05.2022"', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 6

    def city(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['date'] = update.message.text
        update.message.reply_text(f'Город где потеряли человека. (В именительном падеже?)',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 7

    def signs(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['city'] = update.message.text
        update.message.reply_text(f'Введите приметы пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 8

    def special_signs(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['signs'] = update.message.text
        update.message.reply_text(f'Введите особые приметы пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 9
    
    def clothes(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['special_signs'] = update.message.text
        update.message.reply_text(f'Теперь одежду в которой видели пропавшего последний раз\nМожно описать или сказать, что как на фотографии',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 10

    def med_pomosch(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
        else:
            uid = update.message.chat.id
        self.dicts[uid]['clothes'] = update.message.text
        update.message.reply_text('Ведите то, что будет написанно красными буквами\nК примеру:\n"Нуждается в мед помощи"\nИли\n"Возможна потеря памяти"\n\nЕсли такая надпись не нужна оправть в сообщении "1"')
        
        return 11

    def end(self, update: Update, context: CallbackContext):
        if update.callback_query:
            uid = update.callback_query.message.chat.id
            up = update.callback_query.message
        else:
            uid = update.message.chat.id
            up = update.message
        update.message.reply_text('для отмены создания или при ошибке нажмите на кнопку', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        mess = ProgressMsg(up, 'создаем объявления')
        if update.message.text != '1':
               self.dicts[uid]['special_string_text'] = update.message.text
               self.dicts[uid]['special_string'] = True
        else:
            self.dicts[uid]['special_string_text'] = ' '
            self.dicts[uid]['special_string'] = False
        special_string_text = self.dicts[uid]['special_string_text']
        special_string = self.dicts[uid]['special_string']
        self.dicts[uid]['image_old'] = str(uid) + '.png'
        self.dicts[uid]['name_new1'] = str(uid) + '1_send.png'
        self.dicts[uid]['name_new2'] = str(uid) + '2_send.png'
        image_old = self.dicts[uid]['image_old']
        name_new1 = self.dicts[uid]['name_new1']
        name_new2 = self.dicts[uid]['name_new2']
        name = self.dicts[uid]['name']
        yo = self.dicts[uid]['yo']
        date = self.dicts[uid]['date']
        city = self.dicts[uid]['city']
        signs = self.dicts[uid]['signs']
        special_signs = self.dicts[uid]['special_signs']
        clothes = self.dicts[uid]['clothes']
        pattern_photo(image_old, name_new1, True, special_string, special_string_text, name,
                  yo, date, city,
                  signs, special_signs, clothes)
    
        pattern_photo(image_old, name_new2, False, special_string, special_string_text, name,
                  yo, date, city,
                  signs, special_signs, clothes)
        mess.finish()
        a = open(f'{name_new1}', 'rb')
        b = open(f'{name_new2}', 'rb')
        up.reply_document(a)
        up.reply_document(b)
        a.close()
        b.close()
        remove(f'{name_new1}')
        remove(f'{name_new2}')
        remove(f'{image_old}')
        self.dicts[uid] = None
        
        return ConversationHandler.END

    def chat_cancel(self, update: Update, context: CallbackContext):
        update.callback_query.message.reply_text(
            'Ок. Забыли. Это останется между нами...'
        )
        return ConversationHandler.END
    
    def run(self):
        self.bot.start_polling()
        self.bot.idle()


if __name__ == "__main__":
    bot = bot()
    dotenv_path = path.join(path.dirname(__file__), '.env')
    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    bot.run()

