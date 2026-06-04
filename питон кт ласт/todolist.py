from tkinter import Tk, Label, font
from datetime import date


def days_word(n):
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return "день"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "дня"
    return "дней"


task_list = []
with open("spisok.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 1)
        date_part, name = parts[0].strip(), parts[1].strip()
        y, m, d = map(int, date_part.split("-"))
        task_list.append((date(y, m, d), name))

task_list.sort(key=lambda x: x[0])

today = date.today()

window = Tk()
window.title("Мой планировщик задач")
window.geometry("800x550")
window.configure(bg="black")

title_font = font.Font(family="Arial", size=26, weight="bold", underline=True)
item_font = font.Font(family="Courier New", size=13)

title_label = Label(window, text="Список моих задач",
                    bg="black", fg="yellow", font=title_font)
title_label.pack(pady=(25, 25))

for task_date, name in task_list:
    delta = (task_date - today).days
    if delta < 0:
        count = -delta
        msg = f"Просрочено на {count} {days_word(count)}: {name}"
        clr = "red"
    elif delta == 0:
        msg = f"Сегодня: {name}"
        clr = "yellow"
    else:
        msg = f"До \"{name}\" осталось {delta} {days_word(delta)}"
        clr = "white"

    item = Label(window, text=msg, bg="black", fg=clr,
                 font=item_font, anchor="w")
    item.pack(fill="x", padx=50, pady=2)

window.mainloop()
