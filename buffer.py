from random import randint

"""
Gêne :
    Nom str (len(nom) == 2) Non null
    Alelles : [int, ...] (Le dominant étant le plus grand) Non null len == 2
    Bonus vs : [[str, ...], ...] len(bonus) == len(alelles)
"""


def azerty(pere: dict, mere: dict):
    bebe = {}
    for key in pere:
        p_index = randint(0, len(pere[key]) - 1)
        m_index = randint(0, len(mere[key]) - 1)
        if key in mere:
            bebe[key] = [pere[key][p_index], mere[key][m_index]]
        else:
            if randint(0, 1) == 0:
                bebe[key] = pere[key][p_index]
    for key in mere:
        p_index = randint(0, len(pere[key]) - 1)
        m_index = randint(0, len(mere[key]) - 1)
        if key in pere:
            bebe[key] = [pere[key][p_index], mere[key][m_index]]
        else:
            if randint(0, 1) == 0:
                bebe[key] = pere[key][p_index]
    return bebe
