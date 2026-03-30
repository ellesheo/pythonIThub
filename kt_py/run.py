from lib import (
    load,
    est,
    vybrat,
    start,
    max_os,
    show,
    ask,
    hod,
    kon,
    rez,
    esche,
    mes,
    create_papka,
    FL
)


def igra():
    print("\n" + "="*40)
    print("ВИСЕЛИЦА")
    print("="*40)
    print("Правила:")
    print("- Называйте буквы")
    print("- Можно угадать слово")
    print("- Ошибки рисуют виселицу")
    print("="*40 + "\n")
    
    create_papka()
    bank = load(FL)
    m = max_os()
    prod = True
    
    while prod and est(bank):
        sl, pod, bank = vybrat(bank)
        st = start(sl)
        
        print(f"\nОсталось: {len(bank)}")
        
        while not kon(st):
            show(st, pod, print)
            ot = ask("\nХод: ", input)
            st = hod(sl, st, ot, lambda msg: mes(msg, print))
        
        rez(sl, st, print)
        
        if est(bank):
            prod = esche(input)
        else:
            print("\nВсе слова!")
            prod = False
    
    print("\n" + "="*40)
    print("Спасибо!")
    print("="*40)


if __name__ == "__main__":
    igra()