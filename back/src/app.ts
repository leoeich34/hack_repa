import express from 'express';
import cors from 'cors';
import { predictRouter } from './routes';
import { authController } from './controllers/authController';
import { clientsController } from './controllers/clientsController';

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// --- ЛОГИРОВАНИЕ ---
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// --- МАРШРУТЫ (ROUTES) ---
// 1. ML Прогнозы
app.use('/api', predictRouter);

// 2. Авторизация
app.post('/api/auth/register', authController.register);
app.post('/api/auth/login', authController.login);

// 3. Профиль
app.put('/api/users/me', authController.updateProfile);

// 4. Другие вкладки
app.get('/api/clients', clientsController.getList);


// --- ЗАПУСК ---
app.listen(PORT, () => {
    console.log(`🚀 Backend running on http://localhost:${PORT}`);
});