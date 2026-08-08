import re
import time
import random
import telebot
from telebot.apihelper import ApiTelegramException

TOKEN = "8814297533:AAFSt080DGkcPPs-p9c2s-RY-MFa1dmiE4c"
bot = telebot.TeleBot(TOKEN)

USER_MEMORY = {}

KEYBOARD_NEIGHBORS = {
    'а': ['п', 'р', 'ф', 'ы', 'я'], 'б': ['в', 'г', 'ь', 'ю'],
    'в': ['б', 'г', 'с', 'ы'], 'г': ['в', 'д', 'н', 'р'],
    'д': ['г', 'ж', 'л', 'о'], 'е': ['н', 'п', 'у'],
    'ж': ['д', 'з', 'э'], 'з': ['ж', 'х'],
    'и': ['м', 'т', 'ь'], 'к': ['л', 'е', 'у'],
    'л': ['к', 'д', 'о'], 'м': ['и', 'н', 'ь'],
    'н': ['е', 'г', 'г', 'р'], 'о': ['л', 'д', 'п'],
    'п': ['а', 'р', 'о'], 'р': ['п', 'о', 'т'],
    'с': ['в', 'м', 'ч'], 'т': ['р', 'и', 'е'],
    'у': ['к', 'е'], 'ф': ['а', 'ы'],
    'х': ['з', 'ъ'], 'ц': ['у', 'ы'],
    'ч': ['с', 'я'], 'ш': ['щ', 'л'],
    'щ': ['ш', 'д'], 'ы': ['ф', 'в', 'ц'],
    'ь': ['и', 'б', 'м'], 'э': ['ж', 'з'],
    'ю': ['б', 'ь'], 'я': ['ч', 'а']
}

PATTERNS = [
    (r"\b(привет|хай|салют|здарова|ку|хеллоу|добрый|здорово)\b", [
        "Привет-привет! Как делишки?",
        "О, салют! Кого я вижу)",
        "Приветствую! Чем майнишь настроение сегодня?",
        "Здарова) Как день проходит?"
    ]),
    (r"\b(как ты|как дела|как оно|как жизнь|чем занят|что делаешь)\b", [
        "Да потихоньку, музыку вот слушаю параллельно. Ты сам как?",
        "Да нормуль все, отдыхаю. Что у тебя нового?",
        "Всё гуд! Сижу в инете, залипаю. У тебя как успехи?",
        "Да нормально в целом) Чем сам занимаешься?"
    ]),
    (r"\b(кто ты|ты бот|ты ии|ты робот|ты настоящий|человек)\b", [
        "Хах, ну началось) Конечно живой человек. С чего бы мне ботом быть?",
        "Да ты чего, какой бот) Я тут чаи гоняю и сижу в чате, всё нормально.",
        "Обычный парень за компом) Не переживай, железяк тут нет."
    ]),
    (r"\b(игры|играешь|комп|кс|дота|пабг|стим|пс|playstation|xbox)\b", [
        "О, игроман в чате) Я тоже люблю побегать во что-нибудь на досуге.",
        "Игры — это тема! В последнее время правда времени маловато, но иногда засаживаюсь.",
        "Во что сам чаще всего катаешь сейчас?"
    ]),
    (r"\b(музыка|трек|песня|рок|рэп|поп|альбом|слушаешь)\b", [
        "Музыка — это вообще спасение) Я меломан, могу и рок, и электронщину погонять под настроение.",
        "Без музыки вообще день не проходит. Что из последнего у тебя на репите?"
    ]),
    (r"\b(фильм|кино|сериал|киноха|актер|смотрел)\b", [
        "Ооо, кино — это база! Я любитель хороших сюжетных сериалов или триллеров.",
        "Последнее время сложно найти реально годный фильм, одна штамповка... Есть что порекомендовать?"
    ]),
    (r"\b(код|прога|питон|python|программирование|разработка|айти|it)\b", [
        "IT тема — это моё уважение. За этим реально будущее, да и мозг прокачивает хорошо.",
        "Программирование — крутая штука, если вкатиться. Сам кодишь или так, интересуешься?"
    ]),
    (r"\b(скучно|грустно|устал|плохо|депрессия|задолбался|тоска)\b", [
        "Эй, ты чего расклеился? Бывают такие дни, надо просто дать себе отдохнуть.",
        "Понимаю тебя... Иногда прямо всё из рук валится. Включи что-то ненапряжное и просто расслабься."
    ]),
    (r"\b(хаха|ахах|лол|кек|рофл|смешно|хд|xd)\b", [
        "Ахахах, ну да, есть такое))",
        "Рад, что заценил) Юмор спасает мир!",
        "Лооол) Сам с этого угараю."
    ]),
    (r"\b(пока|бб|до связи|бай|спокойной|увидимся)\b", [
        "Давай, бро! На связи, если что — пиши!",
        "Пока-пока! Хорошего времени суток!",
        "Счастливо! Увидимся в сети!"
    ])
]

DEFAULT_RESPONSES = [
    "Хмм, надо подумать... С одной стороны согласен, но тут всё неоднозначно.",
    "Ого, ничего себе повороты) А подробнее можешь рассказать?",
    "Слушай, даже не знаю что сказать на это) А ты сам к чему склоняешься?",
    "Интересная тема конечно. Я обычно про такое даже не задумывался.",
    "Да уж... В жизни вообще много странных вещей происходит)",
    "Хм, ну в этом есть доля правды. Расскажи ещё!"
]


def safe_send_message(chat_id, text):
    try:
        return bot.send_message(chat_id, text)
    except ApiTelegramException:
        return None


def make_typo(text):
    if len(text) < 10 or random.random() > 0.18:
        return text, None

    words = text.split()
    eligible_indices = [i for i, w in enumerate(words) if len(w) >= 4 and w.isalpha()]

    if not eligible_indices:
        return text, None

    idx = random.choice(eligible_indices)
    word = words[idx]
    char_idx = random.randint(1, len(word) - 2)
    char = word[char_idx].lower()

    if char in KEYBOARD_NEIGHBORS:
        wrong_char = random.choice(KEYBOARD_NEIGHBORS[char])
        broken_word = word[:char_idx] + wrong_char + word[char_idx + 1:]
        words[idx] = broken_word

        fix = f"*{word}" if random.random() > 0.3 else f"ой, {word}"
        return " ".join(words), fix

    return text, None


def get_response(user_id, message_text, first_name):
    lowered = message_text.lower()

    if user_id not in USER_MEMORY:
        USER_MEMORY[user_id] = {"name": first_name, "last_ans": ""}

    memory = USER_MEMORY[user_id]

    for pattern, responses in PATTERNS:
        if re.search(pattern, lowered):
            filtered = [r for r in responses if r != memory["last_ans"]]
            chosen = random.choice(filtered if filtered else responses)
            memory["last_ans"] = chosen
            return chosen

    filtered_default = [r for r in DEFAULT_RESPONSES if r != memory["last_ans"]]
    chosen = random.choice(filtered_default if filtered_default else DEFAULT_RESPONSES)
    memory["last_ans"] = chosen
    return chosen


def simulate_reading_and_typing(chat_id, incoming_text, response_text):
    reading_time = len(incoming_text) * 0.03 + random.uniform(0.6, 1.8)
    time.sleep(min(reading_time, 4.0))

    chars = len(response_text)
    cps = random.uniform(5.0, 8.0)
    typing_time = chars / cps + random.uniform(0.5, 1.5)
    typing_time = min(max(typing_time, 1.0), 10.0)

    start = time.time()
    while time.time() - start < typing_time:
        try:
            bot.send_chat_action(chat_id, 'typing')
        except Exception:
            break
        rem = typing_time - (time.time() - start)
        if rem > 0:
            time.sleep(min(3.0, rem))


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "друг"

    response = get_response(user_id, message.text, first_name)

    if random.random() < 0.15 and len(response) > 35 and " " in response:
        parts = response.split(" ", maxsplit=1)

        simulate_reading_and_typing(chat_id, message.text, parts[0])
        if safe_send_message(chat_id, parts[0]) is None:
            return

        time.sleep(random.uniform(0.8, 2.0))

        simulate_reading_and_typing(chat_id, "", parts[1])
        safe_send_message(chat_id, parts[1])
    else:
        final_text, correction = make_typo(response)

        simulate_reading_and_typing(chat_id, message.text, final_text)
        if safe_send_message(chat_id, final_text) is None:
            return

        if correction:
            time.sleep(random.uniform(1.0, 2.5))
            try:
                bot.send_chat_action(chat_id, 'typing')
            except Exception:
                pass
            time.sleep(random.uniform(0.6, 1.2))
            safe_send_message(chat_id, correction)


if __name__ == '__main__':
    bot.infinity_polling()