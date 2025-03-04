from flask import Flask, request, render_template_string
import requests
import json
import os

app = Flask(__name__)

# Чтение конфигурации
config_path = os.path.join(os.getcwd(), 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
github_token = config['github_token']
github_username = config['github_username']

# Функция для получения данных из GitHub API
def get_github_data():
    url = f"https://api.github.com/users/{github_username}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка API: {response.status_code}")
        return None

# Функция для рендеринга страницы
def render_page(data):
    if not isinstance(data, dict):
        return '<h1>Ошибка: данные не получены</h1>'
    template = "Hello, {{name}}!"
    page = template.replace('{{name}}', str(data.get('name') or 'Не указано'))
    return page

# Инициализация страницы при запуске
data = get_github_data()
if data:
    page = render_page(data)
else:
    page = '<h1>Ошибка загрузки данных</h1>'

# Маршрут главной страницы
@app.route('/')
def index():
    return page

# Маршрут для обновления данных
@app.route('/refresh')
def refresh():
    global page
    data = get_github_data()
    if data:
        page = render_page(data)
        return 'Страница обновлена'
    else:
        return 'Ошибка обновления', 500

if __name__ == '__main__':
    app.run(port=3000)