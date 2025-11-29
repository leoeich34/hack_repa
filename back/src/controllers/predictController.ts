import { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';
import { mlService } from '../services/mlService';
import { getSubmissionValue } from '../utils/submissionLoader';

// Путь к реальному датасету для обогащения данных
const CSV_PATH = path.resolve(process.cwd(), '../ml/data/raw/income_test_clean.csv');
let csvCache: any[] | null = null;

// --- 1. ПОЛУЧЕНИЕ ДАННЫХ ИЗ CSV ---
const getRealClientData = (id: string) => {
    try {
        if (!csvCache && fs.existsSync(CSV_PATH)) {
            console.log('Loading CSV cache for predictions...');
            const content = fs.readFileSync(CSV_PATH, 'utf-8');
            csvCache = parse(content, {
                columns: true,
                delimiter: ';',
                skip_empty_lines: true
            });
        }

        if (csvCache) {
            // Ищем строгое совпадение ID
            const found = csvCache.find((row: any) => row.id == id);
            if (found) {
                console.log(`Found real data for client ${id}`);
                return found;
            }
        }
    } catch (e) {
        console.error('CSV Read Error:', e);
    }
    return null;
};

// --- РАСШИРЕННЫЙ КАТАЛОГ ПРОДУКТОВ (18 шт) ---
const PRODUCT_CATALOG = [
    // === PREMIUM ===
    {
        id: 'alfa_only', type: 'INVEST', title: 'Alfa Only',
        text: 'Премиальное обслуживание, бизнес-залы, консьерж и кэшбэк до 100%.',
        rules: (inc: number, pdn: number) => (inc > 250000 ? 150 : -1)
    },
    {
        id: 'invest_private', type: 'INVEST', title: 'А-Инвестиции Private',
        text: 'Персональный брокер и стратегии для капитала от 5 млн ₽.',
        rules: (inc: number, pdn: number) => (inc > 300000 ? 120 : -1)
    },

    // === ИПОТЕКА И НЕДВИЖИМОСТЬ ===
    {
        id: 'mortgage_priv', type: 'MORTGAGE', title: 'Ипотека с господдержкой',
        text: 'Ставка от 6%. Лимит до 30 млн ₽. Оформление онлайн.',
        rules: (inc: number, pdn: number) => (inc > 100000 && pdn < 50 ? 85 : 0)
    },
    {
        id: 'mortgage_it', type: 'MORTGAGE', title: 'IT-Ипотека',
        text: 'Специальная ставка 5% для сотрудников IT-компаний.',
        rules: (inc: number, pdn: number) => (inc > 150000 && pdn < 45 ? 95 : 0)
    },

    // === АВТО ===
    {
        id: 'auto_new', type: 'CASH_LOAN', title: 'Автокредит на новое',
        text: 'Без первоначального взноса. Ставка от 14%. Машина сразу ваша.',
        rules: (inc: number, pdn: number) => (inc > 80000 && pdn < 60 ? 75 : 0)
    },
    {
        id: 'auto_used', type: 'CASH_LOAN', title: 'Кредит на авто с пробегом',
        text: 'Покупка у частного лица или дилера. Проверка авто бесплатно.',
        rules: (inc: number, pdn: number) => (inc > 50000 && inc < 120000 && pdn < 55 ? 65 : 0)
    },

    // === КРЕДИТНЫЕ КАРТЫ ===
    {
        id: 'credit_365', type: 'CREDIT_CARD', title: 'Год без %',
        text: 'Главная кредитка страны. 365 дней без процентов на покупки.',
        rules: (inc: number, pdn: number) => (inc > 30000 && pdn < 70 ? 90 : 10) // Масс-маркет хит
    },
    {
        id: 'travel_credit', type: 'CREDIT_CARD', title: 'Alfa Travel Credit',
        text: 'Милли за покупки. Бесплатная страховка для путешественников.',
        rules: (inc: number, pdn: number) => (inc > 100000 ? 70 : 0)
    },

    // === КРЕДИТЫ НАЛИЧНЫМИ И РЕФИНАНС ===
    {
        id: 'cash_loan', type: 'CASH_LOAN', title: 'Кредит наличными',
        text: 'Деньги на любые цели. Решение за 2 минуты. Доставка курьером.',
        rules: (inc: number, pdn: number) => (pdn < 50 && inc > 40000 ? 80 : -10)
    },
    {
        id: 'refinance', type: 'REFINANCE', title: 'Рефинансирование',
        text: 'Объедините кредиты в один. Уменьшите платеж на 30%.',
        rules: (inc: number, pdn: number) => (pdn > 50 ? 250 : 0) // Топ-приоритет при высокой нагрузке
    },
    {
        id: 'installment', type: 'INSTALLMENT', title: 'Карта рассрочки',
        text: 'Покупки сейчас, оплата частями 0-0-12.',
        rules: (inc: number, pdn: number) => (inc < 60000 && pdn < 60 ? 60 : 20)
    },

    // === ДЕБЕТОВЫЕ И ПОВСЕДНЕВНЫЕ ===
    {
        id: 'kids_card', type: 'DEBIT', title: 'Детская карта',
        text: 'Приложение для ребенка, кэшбэк в кафе и контроль трат.',
        rules: (inc: number, pdn: number) => (inc > 70000 && pdn < 40 ? 45 : 0)
    },
    {
        id: 'alfa_pay', type: 'DEBIT', title: 'Платежное кольцо',
        text: 'Оплата касанием. Керамика, водонепроницаемое.',
        rules: (inc: number, pdn: number) => (inc > 180000 ? 50 : -100)
    },
    {
        id: 'sticker', type: 'DEBIT', title: 'Платежный стикер',
        text: 'Клейте на смартфон и платите как раньше. Бесплатно.',
        rules: (inc: number, pdn: number) => (inc > 40000 ? 40 : 10)
    },

    // === ИНВЕСТИЦИИ И ВКЛАДЫ ===
    {
        id: 'invest_shares', type: 'INVEST', title: 'Инвестиции: Акции',
        text: 'Готовые портфели российских акций с потенциалом роста.',
        rules: (inc: number, pdn: number) => (inc > 90000 && pdn < 35 ? 60 : 0)
    },
    {
        id: 'alfa_vklad', type: 'DEBIT', title: 'Альфа-Вклад',
        text: 'Максимальная ставка до 16% годовых с капитализацией.',
        rules: (inc: number, pdn: number) => (inc > 50000 ? 35 : 25)
    },

    // === СТРАХОВАНИЕ И БИЗНЕС ===
    {
        id: 'ins_life', type: 'DEBIT', title: 'Страхование жизни',
        text: 'Защита здоровья и финансовая безопасность семьи.',
        rules: (inc: number, pdn: number) => (inc > 80000 && pdn > 40 ? 55 : 0)
    },
    {
        id: 'base_card', type: 'DEBIT', title: 'Альфа-Карта',
        text: 'Суперкэшбэк каждый месяц. Бесплатное обслуживание навсегда.',
        rules: (inc: number, pdn: number) => 5 // Всегда доступна, но низкий приоритет, если есть что-то лучше
    }
];

// Функция скоринга продуктов
const getSmartOffers = (income: number, pdn: number) => {
    return PRODUCT_CATALOG
        .map(p => ({ ...p, score: p.rules(income, pdn) })) // Считаем скор для каждого
        .filter(p => p.score > 0) // Убираем неподходящие
        .sort((a, b) => b.score - a.score) // Сортируем: самые важные сверху
        .slice(0, 4) // Берем топ-4
        .map(({ score, rules, ...rest }) => rest); // Убираем служебные поля
};

// --- 2. ГЕНЕРАТОР ЗАГЛУШЕК (Если клиента нет в базе) ---
const generateClientData = (id: string) => ({
    id: id,
    // Генерируем правдоподобный профиль, чтобы ML не падал
    age: 25 + Math.floor(Math.random() * 40),
    gender: Math.random() > 0.5 ? 1 : 0,

    // Финансовые показатели (для корректной работы ML)
    salary_6to12m_avg: 60000 + Math.random() * 150000,
    incomeValue: 0,

    // БКИ (Кредитная история)
    bki_total_max_limit: 100000 + Math.random() * 1000000,
    hdb_bki_total_products: 1 + Math.floor(Math.random() * 10),
    hdb_bki_total_max_limit: 200000 + Math.random() * 500000,
    hdb_bki_active_cc_max_limit: 50000 + Math.random() * 200000,

    // Обороты
    avg_cur_cr_turn: 50000 + Math.random() * 100000,
    avg_cur_db_turn: 40000 + Math.random() * 90000,

    // Гео
    adminarea: 'Москва',
    city_smart_name: 'Москва'
});


// --- КОНТРОЛЛЕР ---
export const predictController = {
    async getPrediction(req: Request, res: Response) {
        try {
            const { id } = req.params;
            let clientData = getRealClientData(id);
            if (!clientData) clientData = generateClientData(id);

            const mlResult = await mlService.predictIncome(clientData);
            const submissionValue = getSubmissionValue(id);
            const income = submissionValue !== null ? submissionValue : mlResult.predicted_income;

            const limit = parseFloat(clientData.bki_total_max_limit || clientData.hdb_bki_total_max_limit || 0);
            // ПДН не может быть отрицательным
            const pdn = income > 0 ? Math.max(0, ((limit * 0.05) / income) * 100) : 0;

            res.json({
                client_id: id,
                prediction: { value: income, currency: 'RUB', confidence: 0 },
                business_metrics: {
                    pdn: Math.min(100, Math.round(pdn)),
                    segment: income > 150000 ? 'Premium' : (income > 80000 ? 'Middle' : 'Mass'),
                    risk_level: pdn > 50 ? 'high' : (pdn > 30 ? 'medium' : 'low')
                },
                factors: mlResult.shap_values,
                // Используем новую умную систему
                offers: getSmartOffers(income, pdn)
            });

        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
};