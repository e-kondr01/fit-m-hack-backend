from operator import itemgetter

import numpy as np
from app.config import ROOT_DIR
from navec import Navec

list_of_topics = [
    "Спорт",
    "ЗОЖ",
    "Сон",
    "Питание",
    "Травма",
    "Лечение",
    "Профилактика",
    "Режим сна",
    "Тренировки",
    "Контрацепция",
    "Половая жизнь",
    "Половое воспитание",
    "Диарея",
    "Гастроэнтерит",
    "Зарядка",
    "Вредные привычки",
    "Утро",
    "Мигрень",
    "Геморрой",
    "Насморк",
    "Простуда",
    "Боль в горле",
    "Гигиена",
    "Грипп",
    "Пандемия",
    "Движение",
    "Зрение",
    "Вакцинация",
    "Закаливание",
    "Фарингит",
    "Ларингит",
    "Ангина",
    "Тонзиллит",
    "Боль в горле",
    "Усталость",
    "Ушиб",
    "Озноб",
    "Волдыри",
    "Прыщи",
    "Диабет",
    "Сладкое",
    "Ринит",
    "Кровотечение",
    "Заложенность носа",
    "Сухость носа",
    "Кандидоз",
]


def load_embeddings_model(path_to_model):
    """
    Просто загружаем предобученную модель с
    :param path_to_model:
    :return:
    """
    return Navec.load(path_to_model)


def cosine(u, v):
    """
    Расчёт расстояния (косинусового) между двумя векторами
    :param u:
    :param v:
    :return:
    """
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def get_embed_vector(text, model):
    """
    Получаем вектор фразы/словосочетания, состоящего из нескольких слов.
    (Каждое слово - это вектор), этой функцией мы из нескольких слов получаем один вектор.
    :param text:
    :param model:
    :return:
    """
    res = []

    tokens = text.lower().split()

    for token in tokens:
        if token in model:
            res.append(model[token])

    if not res:
        res.append(model["<unk>"])

    return np.mean(res, axis=0)


def find_n_closest_topics(text, model, show_similarity_values=False, n_topics=3):
    """
    Получение топ-n ближайших тем к заданной теме
    :param text: Слово или фраза, к которой мы хотим подобрать похожие значения
    :param show_similarity_values: Показывать ли значение близости вектора. По умолчанию False. Измеряется [0, 1]
    :param n_topics: Количество предложенных тем. По умолчанию 3
    :return:
    """
    cosines = {
        cur_text: cosine(
            get_embed_vector(cur_text.lower(), model),
            get_embed_vector(text.lower(), model),
        )
        for cur_text in list_of_topics
        if cur_text.lower() != text.lower()
    }
    res = dict(sorted(cosines.items(), key=itemgetter(1), reverse=True)[:n_topics])
    if show_similarity_values:
        return res
    return list(res.keys())


navec_model = load_embeddings_model(
    ROOT_DIR / "utils" / "navec_hudlit_v1_12B_500K_300d_100q.tar"
)
