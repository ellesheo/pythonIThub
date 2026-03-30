from __future__ import annotations
import random
import os
from dataclasses import dataclass
from typing import List, Tuple


SK = "■"
PA = "v"
FL = "sl.txt"
MAX_OS = 7


Para = Tuple[str, str]


@dataclass(frozen=True)
class St:
    pole: str
    osh: int
    buk: Tuple[str, ...]
    st: str


def load(p: str) -> List[Para]:
    res = []
    with open(p, 'r', encoding='utf-8') as f:
        for s in f:
            s = s.strip()
            if s and not s.startswith('#'):
                r = s.split('|')
                if len(r) >= 2:
                    sl = r[0].strip()
                    pod = r[1].strip()
                    if sl and pod:
                        res.append((sl, pod))
    return res


def est(sp: List[Para]) -> bool:
    return len(sp) > 0


def vybrat(sp: List[Para]) -> Tuple[str, str, List[Para]]:
    i = random.randrange(len(sp))
    sl, pod = sp[i]
    ost = sp[:i] + sp[i + 1:]
    return norm(sl), pod, ost


def norm(sl: str) -> str:
    return sl.strip().lower()


def get_v(osh: int) -> str:
    """Читает фрагмент виселицы из отдельного файла"""
    f = os.path.join(PA, f"v_{osh}.txt")
    try:
        with open(f, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def create_papka() -> None:
    """Создаёт папку для фрагментов виселицы"""
    if not os.path.exists(PA):
        os.makedirs(PA)


def start(s: str) -> St:
    t = make_t(s)
    return St(pole=t, osh=0, buk=tuple(), st="playing")


def make_t(sl: str) -> str:
    return " ".join(SK for _ in sl)


def max_os() -> int:
    return MAX_OS


def show(st: St, pod: str, out) -> None:
    v = get_v(st.osh)
    out(v)
    out(f"\nСлово: {st.pole}")
    out(f"Подсказка: {pod}")
    
    if st.buk:
        s = ", ".join(st.buk)
        out(f"Буквы: {s}")
    out("")


def ask(p: str, inp) -> str:
    return inp(p).strip().lower()


def hod(t: str, st: St, ot: str, msg) -> St:
    ot = clean(ot)
    
    if not ot:
        msg("Пусто")
        return st
    
    if len(ot) > 1:
        if ot == t:
            msg("Верно!")
            return set_st(st, "win")
        msg("Не верно")
        return add_os(st, msg)
    
    b = ot[:1]
    if not (len(b) == 1 and b.isalpha()):
        msg("Букву")
        return st
    
    if b in st.buk:
        msg(f"{b} была")
        return st
    
    nov_buk = st.buk + (b,)
    
    if b in t:
        nov_pole = open_b(t, st.pole, b)
        nov = St(pole=nov_pole, osh=st.osh, buk=nov_buk, st="playing")
        if SK not in nov_pole:
            msg("Всё слово!")
            return set_st(nov, "win")
        msg(f"Есть {b}")
        return nov
    
    msg(f"Нет {b}")
    return add_os(
        St(pole=st.pole, osh=st.osh, buk=nov_buk, st="playing"),
        msg
    )


def clean(txt: str) -> str:
    return txt.strip().lower()


def open_b(t: str, pol: str, b: str) -> str:
    kl = pol.split(" ")
    for i, ch in enumerate(t):
        if ch == b:
            kl[i] = b
    return " ".join(kl)


def add_os(st: St, msg) -> St:
    nov = st.osh + 1
    
    if nov >= MAX_OS:
        msg("Проигрыш!")
        return St(pole=st.pole, osh=nov, buk=st.buk, st="lose")
    
    return St(pole=st.pole, osh=nov, buk=st.buk, st="playing")


def set_st(st: St, s: str) -> St:
    return St(pole=st.pole, osh=st.osh, buk=st.buk, st=s)


def kon(st: St) -> bool:
    return st.st in ("win", "lose")


def rez(t: str, st: St, out) -> None:
    if st.st == "win":
        out("\n" + "="*40)
        out("ВЫ ВЫИГРАЛИ!")
        out(f"Слово: {t.upper()}")
        out("="*40 + "\n")
    else:
        out("\n" + "="*40)
        out("ВЫ ПРОИГРАЛИ")
        out(f"Слово: {t.upper()}")
        out("="*40 + "\n")


def esche(inp) -> bool:
    ot = inp("\nЕщё? (д/н): ").strip().lower()
    return ot in ("д", "да", "y", "yes", "lf")


def mes(m: str, out) -> None:
    out(m)