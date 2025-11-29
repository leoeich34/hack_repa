import { Request, Response } from 'express';
import { mlService } from '../services/mlService';
import { parse } from 'csv-parse/sync';
import fs from 'fs';
import path from 'path';

const CSV_PATH = path.resolve(process.cwd(), '../ml/data/raw/income_test_clean.csv');

let csvCache: any[] | null = null;

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
            const found = csvCache.find((row: any) => row.id == id);
            if (found) {
                console.log(`Found real data for client ${id}`);
                // Превращаем строки в числа, где надо
                return {
                    ...found,
                    // Гарантируем наличие полей, которые мог сгенерировать рандом раньше
                    age: parseInt(found.age || '30'),
                    gender: found.gender === '1' ? 1 : 0
                };
            }
        }
    } catch (e) {
        console.error('CSV Read Error:', e);
    }
    return null; // Не нашли
};

// Генерируем "жирный" объект с данными, чтобы ML не падал
const generateClientData = (id: string) => ({
    id: id,
    // Основные
    age: 25 + Math.floor(Math.random() * 40),
    gender: Math.random() > 0.5 ? 1 : 0, // Модель ждет число или строку (см. конфиг), лучше 1/0 или 'M'/'F'

    // Доходы и ЗП (чтобы модель видела деньги)
    salary_6to12m_avg: 60000 + Math.random() * 150000,
    incomeValue: 0, // Целевая (иногда нужна для формата)

    // БКИ (Кредитная история) - критически важно для банковских моделей
    bki_total_max_limit: 100000 + Math.random() * 1000000,
    hdb_bki_total_products: 1 + Math.floor(Math.random() * 10),
    hdb_bki_total_max_limit: 200000 + Math.random() * 500000,
    hdb_bki_active_cc_max_limit: 50000 + Math.random() * 200000,

    // Обороты (транзакции)
    avg_cur_cr_turn: 50000 + Math.random() * 100000,
    avg_cur_db_turn: 40000 + Math.random() * 90000,

    // Регион (заглушки)
    adminarea: "Москва",
    city_smart_name: "Москва"
});

export const predictController = {
    async getPrediction(req: Request, res: Response) {
        try {
            const { id } = req.params;

            let clientData = getRealClientData(id);

            // 1. Подготавливаем данные клиента
            if (!clientData) {
                console.log(`Client ${id} not found in CSV, using mock generator`);
                clientData = generateClientData(id); // Твоя старая функция-генератор
            }

            // 2. Вызываем ML Сервис (вот теперь он стал "активным")
            const mlResult = await mlService.predictIncome(clientData);

            // 3. Считаем бизнес-метрики на Node.js
            const income = mlResult.predicted_income;

            // Расчет ПДН (фейковый для примера)
            const currentDebt = clientData.bki_total_max_limit * 0.1;
            const pdn = income > 0 ? (currentDebt / income) * 100 : 0;

            // Генерация офферов на основе предсказания
            const offers = [];
            if (income > 150000) {
                offers.push({
                    id: 99,
                    title: 'Alfa Only',
                    text: 'Премиальное обслуживание',
                    is_best: true
                });
            }
            offers.push({
                id: 1,
                title: 'Кредит наличными',
                text: `Одобрено до ${Math.floor(income * 10).toLocaleString()} ₽`,
                is_best: false
            });

            // 4. Отдаем ответ Фронтенду
            res.json({
                client_id: id,
                prediction: {
                    value: income,
                    currency: 'RUB',
                    confidence: 85 + (Math.random() * 10) // Имитация уверенности
                },
                business_metrics: {
                    pdn: Math.round(pdn),
                    segment: income > 120000 ? 'Premium' : 'Mass',
                    risk_level: pdn > 50 ? 'high' : 'low'
                },
                factors: mlResult.shap_values, // Реальные факторы из Python
                offers: offers
            });

        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
};