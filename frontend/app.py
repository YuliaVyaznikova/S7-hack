from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import ast
from collections import Counter
import os
import sys

# Добавляем родительскую директорию в путь для импорта users.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from users import USERS

app = Flask(__name__)
app.secret_key = 'your-secret-key-replace-in-production'  # Замените на реальный секретный ключ в продакшене

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

class User(UserMixin):
    def __init__(self, email, name):
        self.id = email
        self.name = name

@login_manager.user_loader
def load_user(email):
    if email not in USERS:
        return None
    return User(email, USERS[email]['name'])

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in USERS and check_password_hash(USERS[email]['password'], password):
            user = User(email, USERS[email]['name'])
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверный email или пароль')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/data')
@login_required
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
@login_required
def index():
    return render_template('index.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)