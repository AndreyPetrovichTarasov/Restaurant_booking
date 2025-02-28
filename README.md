# Restaurant Booking - система бронирования столиков в ресторане

## 📌 Описание проекта  
**Restaurant Booking** — это веб-приложение для бронирования столиков в ресторане.  
Пользователи могут выбирать дату, временной интервал и доступные столики, а также управлять своими бронями через личный кабинет.  
Администратор может управлять бронированиями и контентом сайта через Django Admin.

---

## 📂 Структура проекта  

```
Restaurant_booking/
│── reservations/       # Приложение для управления бронированием
│   ├── migrations/     # Миграции базы данных
│   ├── templates/      # Шаблоны HTML
│   ├── static/         # Статические файлы (CSS, JS, изображения)
│   ├── forms.py        # Формы для бронирования
│   ├── models.py       # Модели базы данных
│   ├── views.py        # Представления (CBV)
│   ├── urls.py         # Маршруты приложения
│   ├── tasks.py        # Фоновые задачи Celery
│── users/              # Приложение для управления пользователями
│── templates/          # Глобальные шаблоны
│── static/             # Глобальные статические файлы
│── media/              # Загружаемые пользователями файлы (аватары, изображения)
│── Restaurant_booking/ # Основная конфигурация Django
│   ├── settings.py     # Основные настройки проекта
│   ├── urls.py         # Основные маршруты
│   ├── celery.py       # Конфигурация Celery
│── docker/             # Файлы Docker для контейнеризации
│── docker-compose.yml  # Файл для запуска контейнеров
│── manage.py           # Django CLI
│── requirements.txt    # Список зависимостей
│── README.md           # Документация проекта
```

---

## 🎯 Функциональность  

### 🔹 Для пользователей:
- Регистрация и авторизация
- Просмотр доступных столиков
- Бронирование с выбором времени
- Управление своими бронями (изменение, удаление)
- Личный кабинет с историей броней

### 🔹 Для администратора:
- Управление пользователями
- Просмотр и редактирование броней
- Управление контентом сайта через Django Admin

---

## 🚀 Установка и запуск проекта  

### 1️⃣ Установка зависимостей  
Проект использует **Python 3.12** и **PostgreSQL**.  

#### 🔹 Клонируем репозиторий  
```bash
git clone https://github.com/yourusername/restaurant-booking.git
cd restaurant-booking
```

#### 🔹 Создаем и активируем виртуальное окружение  
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

#### 🔹 Устанавливаем зависимости  
```bash
pip install -r requirements.txt
```

---

### 2️⃣ Настройка базы данных  

1. В файле `Restaurant_booking/settings.py` указываем параметры подключения к **PostgreSQL**:  
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'restaurant_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
2. **Применяем миграции**  
```bash
python manage.py migrate
```

3. **Создаем суперпользователя для входа в админку**  
```bash
python manage.py createsuperuser
```

---

### 3️⃣ Запуск сервиса  

#### 🔹 Запускаем сервер Django  
```bash
python manage.py runserver
```

#### 🔹 Запускаем Celery (для фоновых задач)  
```bash
celery -A Restaurant_booking worker --loglevel=info
```

#### 🔹 Запускаем планировщик Celery Beat  
```bash
celery -A Restaurant_booking beat --loglevel=info
```

---

## 🐳 Запуск с помощью Docker  

1. **Запускаем контейнеры**  
```bash
docker-compose up --build
```

2. **Открываем сайт**  
```
http://127.0.0.1:8000
```

3. **Открываем админку**  
```
http://127.0.0.1:8000/admin
```

## 🔧 Дополнительные команды  

- **Создать тестовые данные:**  
  ```bash
  python manage.py loaddata fixtures.json
  ```

- **Очистить базу данных (⚠️ опасно!):**  
  ```bash
  python manage.py flush
  ```

- **Запустить тесты:**  
  ```bash
  pytest --cov=.
  ```

---

## 📞 Контакты  
Если у вас есть вопросы, пишите на email:  
📧 `support@restaurant-booking.com`  
