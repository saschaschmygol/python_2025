# front

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
