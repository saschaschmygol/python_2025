# Front

## Установка и запуск

Установка зависимостей

```bash
npm install
```

Запуск в режиме разработки

```bash
npm run dev
# Откроется по адресу: http://localhost:5173/
```

Сборка для продакшена

```bash
npm run build
# Готовый билд будет в /dist
```

## Настройка API URL

Фронтенд использует собственный axios-клиент:

```bash
src/services/api.ts
```

Чтобы изменить адрес backend, отредактируй:

```typescript
//src/services/api.ts
export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // ← Изменить здесь
  withCredentials: true,
});
```

## Структура проекта

```bash
src/
  services/       # Axios клиент и API
  pages/          # Страницы
  assets/         # Статический контент
  App.tsx         # Маршрутизация
  main.tsx        # Точка входа
```

# Backend

## Установка

1. **Установите зависимости  `pip install -r requirements.txt`**

2. **Создайте файл `.env`** в директории `./communication`:  
   Создайте файл `.env` и заполните его своими значениями переменных окружения по шаблону .env.example:  
   ```
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password

   POSTGRES_DB=your_database_name
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```  
   - `POSTGRES_HOST`: Хост PostgreSQL (по умолчанию `localhost` для локальной БД).  
   - `POSTGRES_PORT`: Порт PostgreSQL (по умолчанию `5432`).  
   - `POSTGRES_USER`: Имя пользователя БД.  
   - `POSTGRES_PASSWORD`: Пароль пользователя БД.  
   - `POSTGRES_DB`: Имя базы данных.  
   - `TELEGRAM_BOT_TOKEN`: Токен вашего Telegram-бота (получите у @BotFather).


## Запуск базы данных

3. **Запустите PostgreSQL в Docker-контейнере**:  
   В директории с `docker-compose.yml` выполните:  
   ```
   docker-compose up db
   ```  
   Это запустит контейнер с PostgreSQL. Оставьте его работать в фоне (или используйте `-d` для detached mode).

## Миграции

4. **Примените миграции Django**:  
   Из директории `./communication`:  
   ```
   python manage.py makemigrations comm_app
   python manage.py migrate
   ```  
   - `makemigrations comm_app`: Создает миграции для приложения `comm_app`.  
   - `migrate`: Применяет миграции к БД.

## Запуск приложения

5. **Запустите сервер и Telegram-бот**:  
   Из директории `./communication` (с активированным виртуальным окружением):  
   - В одном терминале запустите Django-сервер:  
     ```
     python manage.py runserver
     ```  
     Сервер будет доступен по `http://localhost:8000`.  
   - В другом терминале запустите polling для Telegram-бота:  
     ```
     python manage.py poll_telegram
     ```  
     Это обеспечит обработку обновлений от Telegram.
  ## Миграции

5. **Тесты**:  
   Из директории `./communication`:  
   ```
   pytest ./comm_app/tests/test_auth.py -v

   ```  
   - Запустит 3 теста из test_auth.py.  
