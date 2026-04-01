from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

HIDDEN_SYMBOL = "■"

WordItem = Tuple[str, str]

@dataclass(frozen=True)
class RoundState:
    table: str
    lives: int
    used_letters: Tuple[str, ...]
    status: str

def create_word_bank() -> List[WordItem]:
    return [
        ("олень", "Животное с рогами, живёт в лесах и тундре"),
        ("носки", "Предмет одежды, который носят на ногах"),
        ("пальто", "Верхняя одежда для прохладной погоды"),
        ("самолёт", "Транспорт, который летает по воздуху"),
        ("планета", "Космическое тело, вращающееся вокруг звезды"),
    ]

def has_words(bank: List[WordItem]) -> bool:
    return len(bank) > 0

def pick_word_with_hint(bank: List[WordItem]) -> Tuple[str, str, List[WordItem]]:
    index = random.randrange(len(bank))
    word, hint = bank[index]
    remaining = remove_item_by_index(bank, index)
    return normalize_word(word), hint, remaining

def remove_item_by_index(bank: List[WordItem], index: int) -> List[WordItem]:
    return bank[:index] + bank[index + 1:]

def normalize_word(word: str) -> str:
    return word.strip().lower()

def init_round_state(secret_word: str) -> RoundState:
    table = create_table(secret_word)
    lives = get_lives(secret_word)
    return RoundState(table=table, lives=lives, used_letters=tuple(), status="playing")

def create_table(word: str) -> str:
    return " ".join(HIDDEN_SYMBOL for _ in word)

def get_lives(word: str) -> int:
    return len(word)

def show_round(state: RoundState, hint: str) -> None:
    print(f"{state.table} | ❤×{state.lives}")
    print(hint)
    used = format_used_letters(state.used_letters)
    if used:
        print(f"Уже были: {used}")

def format_used_letters(letters: Tuple[str, ...]) -> str:
    if not letters:
        return ""
    return ", ".join(letters)

def prompt_answer() -> str:
    return input("Назовите букву или слово целиком: ").strip().lower()

def process_turn(secret_word: str, state: RoundState, answer: str) -> RoundState:
    cleaned = normalize_answer(answer)
    if not cleaned:
        show_message("Пустой ввод. Введите букву или слово.")
        return state

    if is_full_word_guess(cleaned):
        if is_word_correct(secret_word, cleaned):
            return set_status(state, "win")
        show_message("Неправильно. Вы теряете жизнь.")
        return lose_one_life(state)

    letter = cleaned[:1]
    if not is_single_letter(letter):
        show_message("Введите одну букву или слово целиком.")
        return state

    if is_letter_used(state.used_letters, letter):
        show_message("Эту букву уже называли. Попробуйте другую.")
        return state

    new_used = add_used_letter(state.used_letters, letter)

    if is_letter_in_word(secret_word, letter):
        new_table = open_letter(secret_word, state.table, letter)
        new_state = RoundState(table=new_table, lives=state.lives, used_letters=new_used, status="playing")
        if is_word_opened(new_table):
            return set_status(new_state, "win")
        return new_state

    show_message("Неправильно. Вы теряете жизнь.")
    return lose_one_life(RoundState(table=state.table, lives=state.lives, used_letters=new_used, status="playing"))

def normalize_answer(text: str) -> str:
    return text.strip().lower()

def is_full_word_guess(text: str) -> bool:
    return len(text) > 1

def is_word_correct(secret_word: str, answer: str) -> bool:
    return answer == secret_word

def is_single_letter(ch: str) -> bool:
    return len(ch) == 1 and ch.isalpha()

def is_letter_used(used_letters: Tuple[str, ...], letter: str) -> bool:
    return letter in used_letters

def add_used_letter(used_letters: Tuple[str, ...], letter: str) -> Tuple[str, ...]:
    return used_letters + (letter,)

def is_letter_in_word(word: str, letter: str) -> bool:
    return letter in word

def open_letter(secret_word: str, table: str, letter: str) -> str:
    cells = table.split(" ")
    for i, ch in enumerate(secret_word):
        if ch == letter:
            cells[i] = letter
    return " ".join(cells)

def is_word_opened(table: str) -> bool:
    return HIDDEN_SYMBOL not in table

def lose_one_life(state: RoundState) -> RoundState:
    new_lives = state.lives - 1
    if new_lives <= 0:
        return RoundState(table=state.table, lives=0, used_letters=state.used_letters, status="lose")
    return RoundState(table=state.table, lives=new_lives, used_letters=state.used_letters, status="playing")

def set_status(state: RoundState, status: str) -> RoundState:
    return RoundState(table=state.table, lives=state.lives, used_letters=state.used_letters, status=status)

def is_round_over(state: RoundState) -> bool:
    return state.status in ("win", "lose")

def show_round_result(secret_word: str, state: RoundState) -> None:
    if state.status == "win":
        print(f"{secret_word}\nВы выиграли! Приз в студию!")
        return
    print(f"Жизни закончились. Было загадано слово: {secret_word}")

def ask_play_again() -> bool:
    answer = input("Сыграть ещё? (д/н): ").strip().lower()
    return is_yes(answer)

def is_yes(text: str) -> bool:
    return text in ("д", "да", "y", "yes")

def show_message(msg: str) -> None:
    print(msg)