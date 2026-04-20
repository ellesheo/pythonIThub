#1
def get_books(filename):
    with open(filename, encoding='utf-8', newline='') as file:
        csv_content = csv.reader(file, delimiter='|')
        next(csv_content)
        return list(map(lambda x: [x[0], x[1], x[2], int(x[3]), float(x[4])], csv_content))

#2
def filtered_books(books, substring):
    lowered = substring.lower()
    return list(map(lambda item: [item[0], f"{item[1]}, {item[2]}", item[3], item[4]], 
               filter(lambda item: lowered in item[1].lower(), books)))

#3
def get_total_cost(books):
    return list(map(lambda item: (item[0], item[2] * item[3]), books))

result1 = get_books("books.csv")
print("задание 1:\n", result1)
result2 = filtered_books(result1, "python")
print("задание 2:\n", result2)
result3 = get_total_cost(result2)
print("задание 3:\n", result3)