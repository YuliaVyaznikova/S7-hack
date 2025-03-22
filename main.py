import pandas as pd
import matplotlib.pyplot as plt
import ast

with open("dataset.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

data = [ast.literal_eval(line.strip()) for line in lines]

df = pd.DataFrame(data, columns=["tune", "category", "re"])

a = len(df)
print("Всего", a, "отзывов:", '\n')

category_counts = df['category'].value_counts()
percents = (category_counts / len(df) * 100).round(1).astype(str) + '%'

sumup = pd.DataFrame({
    'Категория': category_counts.index,
    'Количество': category_counts.values,
    'Процент': percents.values
})

print(sumup)

fig1 = plt.figure()
category_counts.plot(kind='bar')
plt.title('Распределение отзывов по категориям')
plt.xlabel('Категория')
plt.ylabel('Количество')
plt.xticks(rotation=90)
plt.tight_layout()

fig2 = plt.figure(figsize=(7.5,7.5))
category_counts.plot(kind='pie', autopct='%1.1f%%', startangle=10)
plt.title('Распределение отзывов по категориям')
plt.ylabel('')
plt.tight_layout()

plt.show()
