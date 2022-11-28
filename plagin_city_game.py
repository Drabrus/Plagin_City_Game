# Игра в города
# author: Drabr

from vacore import VACore
import random
import os


# загружаем списки городов из файлов
def townsload():
    towns = []
    for filename in os.listdir("cities"):
        with open(os.path.join("cities", filename), 'r') as f:
            while True:
                # считываем строку
                line = f.readline()
                # прерываем цикл, если строка пустая
                if not line:
                    break
                towns.append(line)
        # закрываем файл
            f.close
            towns = [i.strip() for i in towns]
        print(towns)
    return towns


# обработчик последней буквы
def letterlast(town):
    letter = town[-1]
    if letter == 'ь':
        letter = town[-2]
    elif letter == 'й':
        letter = 'и'
    return letter.upper()


# выбор случайного  города
def randomchoose(townlist):
    if len(townlist) == 1:
        return townlist[0]
    else:
        num = random.randint(0, (len(townlist)-1))
        return townlist[num]


# функция на старте
def start(core: VACore):
    manifest = {"name": "Игра в города", "version": "1.0",
                "require_online": False,
                "commands": {"игра в города": play_game_start}
                }
    return manifest


def play_game_start(core: VACore, phrase: str):
    core.play_voice_assistant_speech("Скажи правила или начать")
    core.context_set(play_1)


def play_1(core: VACore, phrase: str):
    if phrase == "правила":
        core.play_voice_assistant_speech("Играют города россии."
                                         "Я загадываю город. "
                                         "Ты называешь город,"
                                         " на последнюю букву. "
                                         "Я называю город на последнюю букву"
                                         "и так далее.")
        core.context_set(play_1)
        return
    if phrase == "начать" or phrase == "скачать" or phrase == "повторить":
        core.play_voice_assistant_speech("Я начинаю.")
        core.context_set(play_2)
        return
    if phrase == "сдаюсь":
        core.say("Ты проиграл")
        return
    core.play_voice_assistant_speech("Не поняла...")
    core.context_set(play_1)


def play_2(core: VACore, phrase: str):
    towns = townsload()
    # Список еще не использованных городов
    towns_non_use = towns.copy()
    # Выбираем первый город
    town_choose = randomchoose(towns_non_use)
    while True:
        core.play_voice_assistant_speech(town_choose)
        # Удаляем город из списка не использованных городов
        towns_non_use.remove(town_choose)
        lett = letterlast(town_choose)
        if lett == 'И':
            core.play_voice_assistant_speech('Тебе на И или Й')
        else:
            core.play_voice_assistant_speech('Тебе на: ', lett)
        # Ввод нашего города
        while True:
            town_my = phrase
            town_my = town_my.capitalize()
            if (town_my[0] != lett and town_my[0] != 'Й') or (town_my[0] == 'Й'
                                                              and lett != 'И'):
                core.play_voice_assistant_speech('Не с той буквы')
                continue
            if town_my in towns and town_my not in towns_non_use:
                core.play_voice_assistant_speech('Уже было')
                continue
            try:
                towns_non_use.remove(town_my)
            except ValueError:
                core.play_voice_assistant_speech('Не знаю такого города')
                continue
            break
        # Ход компа
        lett = letterlast(town_my)
        # Список годных городов
        towns_ok = []
        for i in towns_non_use:
            if i[0] == lett:
                towns_ok.append(i)
        if len(towns_ok) == 0:
            core.play_voice_assistant_speech('Сдаюсь, ты выиграл')
            exit()
        town_choose = randomchoose(towns_ok)
    core.context_set(play_2)
