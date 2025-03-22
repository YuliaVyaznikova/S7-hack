from flask import Flask, render_template, jsonify
import ast
from collections import Counter
import os

app = Flask(__name__)

def get_data_path():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.dirname(base_dir)
    return os.path.join(project_dir, "dataset.txt")

def load_data():
    try:
        with open(get_data_path(), "r", encoding="utf-8") as file:
            lines = file.readlines()
        data = []
        for line in lines:
            try:
                # Каждая строка в формате (tune, category, text)
                tune, category, text = ast.literal_eval(line.strip())
                data.append({"tune": tune, "category": category, "text": text})
            except:
                continue
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def calculate_heatmap(data):
    # Подсчитываем статистику по каждой категории
    stats = {}
    for item in data:
        category = item['category']
        tune = item['tune']
        
        if category not in stats:
            stats[category] = {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0}
        
        stats[category][tune] += 1
        stats[category]['total'] += 1
    
    # Преобразуем в проценты
    result = []
    for category, counts in stats.items():
        total = counts['total']
        if total > 0:
            result.append({
                'category': category,
                'positive': counts['positive'] / total,
                'neutral': counts['neutral'] / total,
                'negative': counts['negative'] / total
            })
    
    return result

@app.route('/api/data')
def get_data():
    try:
        data = load_data()
        if not data:
            return jsonify({
                'categories': {},
                'heatmap': [],
                'error': 'No data available'
            })

        categories = [item['category'] for item in data]
        category_counts = Counter(categories)
        
        heatmap_data = calculate_heatmap(data)
        
        return jsonify({
            'categories': dict(category_counts),
            'heatmap': heatmap_data
        })
    except Exception as e:
        return jsonify({
            'categories': {},
            'heatmap': [],
            'error': str(e)
        }), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)