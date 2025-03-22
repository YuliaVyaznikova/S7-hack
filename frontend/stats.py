import csv
from collections import Counter


def make_stats():
    data = {}
    lst = []
    try:
        with open('dataset.txt', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if len(row) < 2:
                    print('not enough information')
                    continue

                key = ''.join(i for i in row[1] if i.isalpha())
                value = ''.join(i for i in row[0] if i.isalpha())

                if key not in data:
                    data[key] = []

                data[key].append(value)

        for category in data.keys():
            if len(data[category]) == 0:
                print(f'no data for {category}')
                continue

            counts = Counter(data[category])
            total_comments = len(data[category])

            pos_comm = counts['positive'] / total_comments
            neg_comm = counts['negative'] / total_comments
            neut_comm = counts['neutral'] / total_comments
            lst.append((category, pos_comm, neut_comm, neg_comm))
    except FileNotFoundError:
        print(f"file is not found.")
    except Exception as e:
        print(f"error occurred: {e}")

    return lst

if __name__ == '__main__':
    lst = make_stats()
    for el in lst:
        print(el)
