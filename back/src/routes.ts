import { Router } from 'express';
import { predictController } from './controllers/predictController';
import { analyticsController } from './controllers/analyticsController';

export const predictRouter = Router();

// Маршрут для получения прогноза
// Раньше тут была "лапша" кода, теперь чистый вызов контроллера
predictRouter.get('/clients/:id/predict', predictController.getPrediction);
predictRouter.get('/analytics', analyticsController.getStats);