# Використовуємо офіційний образ Python
FROM python:3.9

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли з локальної системи у контейнер
COPY requirements.txt .

# Встановлюємо необхідні бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код проекту у контейнер
COPY . .

# Збір статичних файлів
RUN python manage.py collectstatic --noinput

# Відкриваємо порт для Django
EXPOSE 8000

# Команда для запуску з gunicorn (для продакшн)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_weather_reminder.wsgi:application"]
