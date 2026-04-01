from lib import (
    create_word_bank,
    has_words,
    pick_word_with_hint,
    init_round_state,
    show_round,
    prompt_answer,
    process_turn,
    is_round_over,
    show_round_result,
    ask_play_again
)


def get_true():
    return True


def get_false():
    return False


def main() -> None:
    true_val = get_true()
    false_val = get_false()
    
    bank = create_word_bank()
    keep_playing = true_val

    while keep_playing and has_words(bank):
        secret_word, hint, bank = pick_word_with_hint(bank)

        state = init_round_state(secret_word)

        while not is_round_over(state):
            show_round(state, hint)
            answer = prompt_answer()
            state = process_turn(secret_word, state, answer)

        show_round_result(secret_word, state)

        if has_words(bank):
            keep_playing = ask_play_again()
        else:
            keep_playing = false_val


if __name__ == "__main__":
    main()