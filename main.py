from distutils.util import split_quoted


def pattern_photo(image_old: str, name_new: str, orientation: bool, med_pomosch: bool, name: str,
                  yo: str, date: str, gender: bool, city: str,
                  signs=None, special_signs=None, clothes=None):
    """
    :param image_old: имя файла фото человека
    :param name_new: имя нового итогового файла, под которым нужно сохранить
    :param orientation: ореинтация объявления (True - книжная, False - альбомная)
    :param med_pomosch: нужна ли мед помощь (True - нужна, False - не нужна)
    :param name: ФИО человека
    :param yo: сколько лет
    :param date: когда пропал
    :param gender: пол пропавшего человека (1 - муж, 0 - жен)
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
        edge_pix_y = 0
        im2 = Image.open(image_old).resize((390, 480))
        im.paste(im2, (75, 75))
        image_draw = ImageDraw.Draw(im)

        # здесь задаются шрифты, ничего не трогать
        font_name = ImageFont.truetype('fonts/arial_bold.ttf', size=40)
        font_yo = ImageFont.truetype('fonts/arial.ttf', size=25)
        font_date = ImageFont.truetype('fonts/arial.ttf', size=25)
        font_warn = ImageFont.truetype('fonts/arial_bold.ttf', size=36)
        font_norm = ImageFont.truetype('fonts/arial.ttf', size=25)
        font_bold = ImageFont.truetype('fonts/arial_bold.ttf', size=25)

        # отрисовка имени человека
        name = textwrap.wrap(name, width=14)
        for i in range(len(name)):
            image_draw.text((475, 75 + 36 * i), name[i], font=font_name, fill=(0, 0, 0))
            edge_pix_y = 75 + 38 * i

        # отрисовка даты рождения человека
        yo_int = int(yo.split()[0])
        image_draw.text((475, edge_pix_y + 40), f'{yo} ({now - yo_int} г.р.)',
                        font=font_yo, fill=(0, 0, 0))
        edge_pix_y = edge_pix_y + 65

        # отрисовка города пропажи
        image_draw.text((475, edge_pix_y), city, font=font_date, fill=(0, 0, 0))
        edge_pix_y += 25

        # отрисовка даты пропажи человека
        date = (f'С {date} его местонахождение неизвестно' if gender
                else f'С {date} её местонахождение неизвестно')
        date = textwrap.wrap(date, width=26)
        for i in range(len(date)):
            image_draw.text((475, edge_pix_y), date[i], font=font_date, fill=(0, 0, 0))
            edge_pix_y += 25
        image_draw.line((475, edge_pix_y + 5, 825, edge_pix_y + 5), fill=(20, 97, 23), width=4)
        edge_pix_y += 5

        # отрисовка необходимости мед. помощи
        if med_pomosch:
            image_draw.text((68, 625), 'НУЖДАЕТСЯ В МЕДИЦИНСКОЙ ПОМОЩИ',
                            font=font_warn, fill=(255, 0, 0))

        # отрисовка примет
        if signs is not None:
            image_draw.text((475, edge_pix_y), 'Приметы:', font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 5
            signs = 'приметы:' + signs
            signs = textwrap.wrap(signs, width=23)
            for i in range(len(signs)):
                if i == 0:
                    image_draw.text((610, edge_pix_y), signs[0][signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((475, edge_pix_y), signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 27

        # отрисовка особых примет
        if special_signs is not None:
            image_draw.text((475, edge_pix_y), 'Особые приметы:', font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 5
            special_signs = 'особыеериметы: ' + special_signs
            special_signs = textwrap.wrap(special_signs, width=23)
            for i in range(len(special_signs)):
                if i == 0:
                    image_draw.text((710, edge_pix_y), special_signs[0][special_signs[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((475, edge_pix_y), special_signs[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 28

            # отрисовка одежды пропавшего
            text = 'Был одет:' if gender else 'Была одета:'
            image_draw.text((475, edge_pix_y), text, font=font_bold, fill=(0, 0, 0))
            edge_pix_y += 5
            text = 'Былоодет: ' if gender else 'Былааодета: '
            clothes = text + clothes
            clothes = textwrap.wrap(clothes, width=23)
            for i in range(len(clothes)):
                if i == 0:
                    image_draw.text((615, edge_pix_y), clothes[0][clothes[0].index(':') + 1:],
                                    font=font_norm, fill=(0, 0, 0))
                else:
                    image_draw.text((475, edge_pix_y), clothes[i], font=font_norm, fill=(0, 0, 0))
                edge_pix_y += 26

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

        # отрисовка необходимости мед. помощи
        if med_pomosch:
            image_draw.text((510, 690), 'НУЖДАЕТСЯ В МЕДИЦИНСКОЙ ПОМОЩИ',
                            font=font_warn, fill=(255, 0, 0))

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
        clothes = textwrap.wrap(clothes, width=45)
        for i in range(len(clothes)):
            if i == 0:
                image_draw.text((680, edge_pix_y), clothes[0][clothes[0].index(':') + 1:],
                                font=font_norm, fill=(0, 0, 0))
            else:
                image_draw.text((510, edge_pix_y), clothes[i], font=font_norm, fill=(0, 0, 0))
            edge_pix_y += 26
    im.save(name_new)