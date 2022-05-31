from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters, \
    CallbackQueryHandler
from main import pattern_photo
from os import remove
from sql_api import Bd

class ST:
    keyboard = [[InlineKeyboardButton("закрыть это сообщение", callback_data='del')], [InlineKeyboardButton("Отмена", callback_data='chatcancel')]]
    image_old = str()
    name_new = str()
    orientation = bool()
    name = str()
    yo = str()
    date = str()
    gender = bool()
    city = str()
    signs = str()
    special_signs = str()
    clothes = str()
    med_pomosch = bool()
    id = int()
    adname = int()


class bot:
    def __init__(self):
        self.bot = Updater('5346956073:AAE6rTcK0YTs9FGz2bqlJQqLDSA3IUNhqUo')
        self.dispatcher = self.bot.dispatcher
        self.sql = Bd()
        self.chat = ConversationHandler(
            entry_points=[CommandHandler('new', self.new)],
            states={
                1: [MessageHandler(Filters.all, self.orentation)],
                2: [CallbackQueryHandler(self.name, pattern=r'^.$')],
                3: [MessageHandler(Filters.all, self.year)],
                4: [MessageHandler(Filters.all, self.date)],
                5: [MessageHandler(Filters.all, self.gender)],
                6: [CallbackQueryHandler(self.city, pattern=r'^.$')],
                7: [MessageHandler(Filters.all, self.signs)],
                8: [MessageHandler(Filters.all, self.special_signs)],
                9: [MessageHandler(Filters.all, self.clothes)],
                10: [MessageHandler(Filters.all, self.med_pomosch)],
                11: [CallbackQueryHandler(self.end, pattern=r'^.$')],
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
                    update.message.reply_text('Администраторов нема')  # убрать

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
    
    def orentation(self, update: Update, context: CallbackContext):
        print(update.message)
        try:
            f = context.bot.getFile(update.message.document.file_id)
            f.download(f'./{update.message.chat_id}.png')
        except:
            f = context.bot.getFile(update.message.photo[-1].file_id)
            f.download(f'./{update.message.chat_id}.png')
        kboard = [[InlineKeyboardButton("✓", callback_data='0')], [InlineKeyboardButton("Отмена", callback_data='chatcancel')]]
        update.message.reply_text('Фаил загружен\nНажмите на галочку', reply_markup=InlineKeyboardMarkup(kboard, one_time_keyboard=False))
        return 2

    def name(self, update: Update, context: CallbackContext):
        update.callback_query.delete_message()
        
        update.callback_query.message.reply_text(f'Ок\nТеперь введите ФИО пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 3

    def year(self, update: Update, context: CallbackContext):
        ST.name = update.message.text
        update.message.reply_text('Теперь ввидите сколько лет пропавшему\nпример:"30 лет"', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 4
    
    def date(self, update: Update, context: CallbackContext):
        ST.yo = update.message.text
        update.message.reply_text('Теперь дату когда пропал человек\nпример:"25.05.2022"', reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 5

    def gender(self, update: Update, context: CallbackContext):
        ST.date = update.message.text
        kboard = [[InlineKeyboardButton("женский", callback_data='0')], [InlineKeyboardButton("мужской", callback_data='1')], [InlineKeyboardButton("Отмена", callback_data='chatcancel')]]
        update.message.reply_text('теперь пол', reply_markup=InlineKeyboardMarkup(kboard, one_time_keyboard=False))
        return 6

    def city(self, update: Update, context: CallbackContext):
        ST.gender = update.callback_query.data
        update.callback_query.delete_message()
        
        update.callback_query.message.reply_text(f'Город где потеряли человека. (В именительном падеже?)',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 7

    def signs(self, update: Update, context: CallbackContext):
        ST.city = update.message.text
        update.message.reply_text(f'Введите приметы пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 8

    def special_signs(self, update: Update, context: CallbackContext):
        ST.signs = update.message.text
        update.message.reply_text(f'Введите особые приметы пропавшего',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 9
    
    def clothes(self, update: Update, context: CallbackContext):
        ST.special_signs = update.message.text
        update.message.reply_text(f'Теперь одежду в которой видели пропавшего последний раз\nМожно описать или сказать, что как на фотографии',
                                  reply_markup=InlineKeyboardMarkup(ST.keyboard, one_time_keyboard=False))
        return 10

    def med_pomosch(self, update: Update, context: CallbackContext):
        ST.clothes = update.message.text
        kboard = [[InlineKeyboardButton("нет", callback_data='0')], [InlineKeyboardButton("да", callback_data='1')], [InlineKeyboardButton("Отмена", callback_data='chatcancel')]]
        update.message.reply_text(f'нужна ли человеку мед помощь',
                                  reply_markup=InlineKeyboardMarkup(kboard, one_time_keyboard=False))
        return 11

    def end(self, update: Update, context: CallbackContext):
        ST.med_pomosch = update.callback_query.data
        uid = update.callback_query.message.chat_id
        ST.name_new = str(uid) + '_send.png'
        pattern_photo(ST.image_old, ST.name_new, True, int(ST.med_pomosch), ST.name,
                  ST.yo, ST.date, int(ST.gender), ST.city,
                  ST.signs, ST.special_signs, ST.clothes)
        
        a = open(f'{ST.name_new}', 'rb')
        update.callback_query.message.reply_document(a)
        a.close()
        remove(ST.name_new)
        pattern_photo(ST.image_old, ST.name_new, False, int(ST.med_pomosch), ST.name,
                  ST.yo, ST.date, int(ST.gender), ST.city,
                  ST.signs, ST.special_signs, ST.clothes)
        a = open(f'{ST.name_new}', 'rb')
        update.callback_query.message.reply_document(a)
        a.close()
        remove(f'{ST.name_new}')
        remove(f'{ST.image_old}')
        
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
    bot.run()