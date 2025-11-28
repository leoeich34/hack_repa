import express from 'express';
import cors from 'cors';
import { predictRouter } from './routes';

const app = express();
const PORT = 3000;

app.use(cors()); // Разрешаем запросы с фронта
app.use(express.json());

// Логирование запросов
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// Подключаем маршруты
app.use('/api', predictRouter);

app.listen(PORT, () => {
    console.log(`🚀 Backend running on http://localhost:${PORT}`);
});