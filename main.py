from distutils.util import split_quoted


def pattern_photo(image_old: str, name_new: str, orientation: bool, special_string: bool,
                  text_of_ss: str, name: str, yo: str, date: str, city: str,
                  signs=None, special_signs=None, clothes=None):
    """
    :param image_old: имя файла фото человека
    :param name_new: имя нового итогового файла, под которым нужно сохранить
    :param orientation: ореинтация объявления (True - книжная, False - альбомная)
    :param special_string: нужна ли специальная надпись (True - нужна, False - не нужна)
    :param text_of_ss: текст специальной надписи
    :param name: ФИО человека
    :param yo: сколько лет
    :param date: когда пропал
    :param city: город, где пропал человек
    :param signs: приметы
    :param special_signs: особые приметы
    :param clothes: одежда на нём
    :return: отредактированное фото
    """
    import textwrap
    import datetime
    from PIL import Image, ImageDraw, ImageFont

    now = int(datetime.datetime.now().year)
    im = Image.open('templates/book.png') if orientation else Image.open('templates/album.png')

    # книжная ориентация
    if orientation:
        im2 = Image.open(image_old).resize((800, 950))
        im.paste(im2, (150, 155))
        image_draw = ImageDraw.Draw(im)

        # здесь задаются шрифты, ничего не трогать
        font_firstname = ImageFont.truetype('arial_bold.ttf', size=80)
        font_name = ImageFont.truetype('arial_bold.ttf', size=60)
        font_norm = ImageFont.truetype('arial.ttf', size=45)
        font_bold = ImageFont.truetype('arial_bold.ttf', size=45)
        font_warn = ImageFont.truetype('arial_bold.ttf', size=65)

        # отрисовка фамилии человека
        firstname = name.split()[0]
        image_draw.text((980, 155), firstname, font=font_firstname, fill=(0, 0, 0))

        # отрисвока имени человека
        name = textwrap.wrap(' '.join(name.split()[1:]), width=20)
        edge_pix_y = 190
        for i in range(len(name)):
            edge_pix_y += 38
            image_draw.text((980, edge_pix_y + 10 * i), name[i], font=font_name, fill=(0, 0, 0))

        # отрисовка даты рождения человека
        yo_int = int(yo.split()[0])
        image_draw.text((980, edge_pix_y + 75), f'{yo} ({now - yo_int} г.р.)',
                        font=font_norm, fill=(0, 0, 0))
        edge_pix_y = edge_pix_y + 120

        # отрисовка города пропажи
        city = textwrap.wrap(city, width=26)
        for i in range(len(city)):
            image_draw.text((980, edge_pix_y), city[i], font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 40
        edge_pix_y += 10

        # отрисовка даты пропажи человека
        date = f'С {date} местонахождение неизвестно'
        date = textwrap.wrap(date, width=26)
        for i in range(len(date)):
            image_draw.text((970, edge_pix_y), date[i], font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 40
        image_draw.line((970, edge_pix_y + 15, 1665, edge_pix_y + 15), fill=(20, 97, 23), width=10)
        edge_pix_y += 20

        # отрисовка специальной надписи
        if special_string:
            text_of_ss = textwrap.wrap(text_of_ss, width=43)
            if len(text_of_ss) == 1:
                count = len(text_of_ss[0]) // 2
                image_draw.text((452 - count * 21, 590), text_of_ss[0], font=font_warn, width=4, fill=(255, 0, 0))
            else:
                for text in text_of_ss:
                    if text == text_of_ss[-1]:
                        count = len(text) // 2
                        image_draw.text((650 - count * 22, 1180 + text_of_ss.index(text) * 50),
                                        text, font=font_warn, width=4, fill=(255, 0, 0))
                    else:
                        image_draw.text((150, 1180 + text_of_ss.index(text) * 50),
                                        text, font=font_warn, width=4, fill=(255, 0, 0))

        # отрисовка примет
        if signs is not None:
            image_draw.text((980, edge_pix_y), 'Приметы: ', font=font_bold, fill=(0, 0, 0))
            signs = 'приметы:' + signs
            edge_pix_y += 9
            signs = textwrap.wrap(signs, width=28)
            for i in range(len(signs)):
                if i == 0:
                    image_draw.text((1230, edge_pix_y), signs[0][signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((980, edge_pix_y), signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 40

        # отрисовка особых примет
        if special_signs is not None:
            image_draw.text((980, edge_pix_y), 'Особые приметы:', font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 9
            special_signs = 'особыееприметы: ' + special_signs
            special_signs = textwrap.wrap(special_signs, width=30)
            for i in range(len(special_signs)):
                if i == 0:
                    image_draw.text((1390, edge_pix_y), special_signs[0][special_signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((980, edge_pix_y), special_signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 40

        # отрисовка одежды пропавшего
        if clothes is not None:
            text = 'Был(а) одет(а): '
            image_draw.text((980, edge_pix_y), text, font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 9
            clothes = text + clothes
            clothes = textwrap.wrap(clothes, width=30)
            for i in range(len(clothes)):
                if i == 0:
                    image_draw.text((1330, edge_pix_y), clothes[0][clothes[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((980, edge_pix_y), clothes[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 40

    # альбомная ориентация
    else:
        edge_pix_y = 0
        im2 = Image.open(image_old).resize((410, 545))
        im.paste(im2, (75, 75))
        image_draw = ImageDraw.Draw(im)

        # здесь задаются шрифты, ничего не трогать
        font_name = ImageFont.truetype('fonts/arial_bold.ttf', size=60)
        font_yo = ImageFont.truetype('fonts/arial.ttf', size=35)
        font_town = ImageFont.truetype('fonts/arial_bold.ttf', size=35)
        font_date = ImageFont.truetype('fonts/arial_bold.ttf', size=35)
        font_warn = ImageFont.truetype('fonts/arial_bold.ttf', size=33)
        font_norm = ImageFont.truetype('fonts/arial.ttf', size=30)
        font_bold = ImageFont.truetype('fonts/arial_bold.ttf', size=30)

        # отрисовка имени человека
        name = textwrap.wrap(name, width=18)
        for i in range(len(name)):
            image_draw.text((510, 75 + 70 * i), name[i], font=font_name, fill=(0, 0, 0))
            edge_pix_y = 100 + 70 * i

        # отрисовка даты рождения человека
        yo_int = int(yo.split()[0])
        image_draw.text((510, edge_pix_y + 40), f'{yo} ({now - yo_int} г.р.)',
                        font=font_yo, fill=(0, 0, 0))
        edge_pix_y = edge_pix_y + 77

        # отрисовка города пропажи
        image_draw.text((510, edge_pix_y), city, font=font_town, fill=(0, 0, 0))
        edge_pix_y += 50

        # отрисовка даты пропажи человека
        date = (f'С {date} его местонахождение неизвестно' if gender
                else f'С {date} её местонахождение неизвестно')
        date = textwrap.wrap(date, width=35)
        for i in range(len(date)):
            image_draw.text((510, edge_pix_y), date[i], font=font_date, fill=(0, 0, 0))
            edge_pix_y += 40

        # отрисовка специальной надписи
        if special_string:
            text_of_ss = textwrap.wrap(text_of_ss, width=35)
            if len(text_of_ss) == 1:
                count = len(text_of_ss[0]) // 2
                image_draw.text((860 - count * 21, 670), text_of_ss[0], font=font_warn, width=4, fill=(255, 0, 0))
            else:
                for text in text_of_ss:
                    if text == text_of_ss[-1]:
                        count = len(text) // 2
                        image_draw.text((860 - count * 21, 670 + text_of_ss.index(text) * 30),
                                        text, font=font_warn, width=4, fill=(255, 0, 0))
                    else:
                        image_draw.text((510, 670 + text_of_ss.index(text) * 25),
                                        text, font=font_warn, width=4, fill=(255, 0, 0))

        # отрисовка примет
        if signs is not None:
            image_draw.text((510, edge_pix_y), 'Приметы:', font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 5
            signs = 'приметы:' + signs
            signs = textwrap.wrap(signs, width=40)
            for i in range(len(signs)):
                if i == 0:
                    image_draw.text((670, edge_pix_y), signs[0][signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((510, edge_pix_y), signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 28

        # отрисовка особых примет
        if special_signs is not None:
            image_draw.text((510, edge_pix_y), 'Особые приметы:', font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 5
            special_signs = 'особыееприметы: ' + special_signs
            special_signs = textwrap.wrap(special_signs, width=36)
            for i in range(len(special_signs)):
                if i == 0:
                    image_draw.text((800, edge_pix_y), special_signs[0][special_signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((510, edge_pix_y), special_signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 28

        # отрисовка одежды пропавшего
        text = 'Был одет:' if gender else 'Была одета:'
        image_draw.text((510, edge_pix_y), text, font=font_bold, fill=(0, 0, 0))
        edge_pix_y += 5
        text = 'Былоодет: ' if gender else 'Былааодета: '
        clothes = text + clothes
        clothes = textwrap.wrap(clothes, width=44)
        for i in range(len(clothes)):
            if i == 0:
                if gender:
                    image_draw.text((680, edge_pix_y), clothes[0][clothes[0].index(':') + 1:],
                                font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((710, edge_pix_y), clothes[0][clothes[0].index(':') + 1:],
                                font=font_norm, fill=(0, 0, 0))
            else:
                image_draw.text((510, edge_pix_y), clothes[i], font=font_norm, fill=(0, 0, 0))
            edge_pix_y += 26
    im.save(name_new)
