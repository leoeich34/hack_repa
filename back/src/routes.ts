import { Router } from 'express';

export const predictRouter = Router();

predictRouter.get('/clients/:id/predict', async (req, res) => {
    const { id } = req.params;

    // Имитация задержки
    await new Promise(r => setTimeout(r, 600));

    // Генерация случайных чисел на основе ID, чтобы было интересно переключаться
    const baseIncome = 45000 + (parseInt(id) || 1) * 1234 % 400000;
    const pdnValue = 10 + (parseInt(id) || 1) * 7 % 80;

    res.json({
        client_id: id,
        prediction: {
            value: baseIncome,
            currency: 'RUB',
            confidence: 85 + (parseInt(id) % 15) // Точность от 85% до 99%
        },
        // ВАЖНО: Исправленное название поля
        business_metrics: {
            pdn: pdnValue,
            segment: baseIncome > 150000 ? 'Premium' : 'Mass',
            risk_level: pdnValue > 50 ? 'high' : 'low'
        },
        factors: [
            { name: 'Уровень дохода (ФОТ)', value: 15.4, desc: 'Высокая белая зарплата' },
            { name: 'Кредитная нагрузка', value: -8.2, desc: 'Наличие 2 кредитов' },
            { name: 'Возраст', value: 4.1, desc: 'Группа 30-40 лет' },
            { name: 'Транзакции A-Pay', value: 2.3, desc: 'Активное использование' }
        ],
        offers: [
            {
                id: 1,
                title: 'Кредит наличными',
                text: 'Ваш лимит рассчитан: 1 500 000 ₽',
                is_best: true
            },
            {
                id: 2,
                title: 'Alfa Travel',
                text: 'Кэшбэк милями за полеты',
                is_best: false
            }
        ]
    });
});