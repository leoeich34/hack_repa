import { Router } from 'express';

export const predictRouter = Router();

// MOCK: GET /api/clients/:id/predict
// Эмулируем работу ML и возврат данных
predictRouter.get('/clients/:id/predict', async (req, res) => {
    const { id } = req.params;

    // Имитация задержки (как будто ML думает)
    await new Promise(r => setTimeout(r, 800));

    // Эти данные потом будет возвращать реальный ML + твоя обработка
    const mockResponse = {
        client_id: id,
        prediction: {
            value: 145000, // Прогноз дохода
            currency: 'RUB',
            confidence: 92 // Уверенность модели
        },
        business_info: {
            pdn: 24.5, // Долговая нагрузка
            segment: 'Middle+',
            risk_level: 'low'
        },
        // SHAP значения (почему такой прогноз)
        factors: [
            { name: 'Возраст', value: 15, desc: 'Возраст 35 лет (+ к доходу)' },
            { name: 'Стаж', value: 20, desc: 'Стаж > 5 лет' },
            { name: 'Кредиты', value: -10, desc: 'Наличие ипотеки' }
        ],
        // Рекомендации
        offers: [
            {
                id: 1,
                title: 'Альфа-Карта Premium',
                text: 'Кэшбэк до 100% на категорию',
                is_best: true
            },
            {
                id: 2,
                title: 'Кредит наличными',
                text: 'Вам одобрено 1.5 млн ₽'
            }
        ]
    };

    res.json(mockResponse);
});