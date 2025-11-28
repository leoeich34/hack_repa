# Alfa AI Service

Решение задачи предсказания доходов для Альфа-Банка.
Веб-интерфейс для менеджеров с визуализацией ML-прогнозов и генерацией офферов.

## Структура
- `/front` — Vue 3 + Tailwind CSS (Интерфейс)
- `/back` — Node.js + Express (API Gateway & Business Logic)
- `/ml` — Python ML Service (FastAPI + Models)
- `/docs` — Документация и контракты API

## Быстрый старт (Dev)

### Backend
```bash
cd back
npm install
npm run dev
```

### Frontend
```bash
cd front
npm install
npm run dev
```