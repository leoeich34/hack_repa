import { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';
import { generateIdentity } from '../utils/nameGenerator';

// Путь к реальным данным (выходим из src/controllers -> project -> ml/data/raw)
// Если структура папок другая, путь нужно поправить
const CSV_PATH = path.resolve(process.cwd(), '../ml/data/raw/income_test_clean.csv');

export const clientsController = {
    async getList(req: Request, res: Response) {
        try {
            let clientsRaw = [];

            // 1. Пытаемся прочитать реальный CSV
            if (fs.existsSync(CSV_PATH)) {
                console.log('Reading real data from:', CSV_PATH);
                const fileContent = fs.readFileSync(CSV_PATH, 'utf-8');

                // Читаем только первые 50 строк для скорости
                // Важно: разделитель в ваших файлах - точка с запятой (;)
                const records = parse(fileContent, {
                    columns: true,
                    skip_empty_lines: true,
                    delimiter: ';',
                    to: 50
                });

                clientsRaw = records;
            } else {
                console.warn('CSV file not found, using mocks. Path:', CSV_PATH);
                // Фолбек: генерируем заглушки, если файла нет
                clientsRaw = Array.from({ length: 20 }).map((_, i) => ({
                    id: (1000200 + i).toString(),
                    incomeValue: 50000 + Math.random() * 150000, // Фейковый доход для мока
                    bki_total_max_limit: Math.random() * 1000000
                }));
            }

            // 2. Обогащаем данные для фронтенда
            const clients = clientsRaw.map((row: any) => {
                const id = row.id || Math.floor(Math.random() * 100000).toString();
                const identity = generateIdentity(id);

                // Пытаемся достать доход (в тесте его может не быть, тогда генерируем "предварительный")
                // Либо берем из incomeValue, если это train
                let income = parseFloat(row.target || row.incomeValue || 0);

                // Если дохода нет (это тест), генерируем "предварительный" на основе хеша ID
                // чтобы он был стабильным для этого клиента
                if (!income || isNaN(income)) {
                    const seed = parseInt(id.replace(/\D/g, '').substring(0, 5)) || 123;
                    income = 45000 + (seed % 400000);
                }

                // Расчет риска (на основе дохода)
                const limit = parseFloat(row.bki_total_max_limit || row.hdb_bki_total_max_limit || 0);
                const debtLoad = limit > 0 ? (limit * 0.3 / income) : 0.4;

                let risk: 'low' | 'medium' | 'high' = 'medium';
                if (income > 150000 && debtLoad < 0.5) risk = 'low';
                if (income < 50000 || debtLoad > 0.8) risk = 'high';

                // Сегмент
                let segment: 'Premium' | 'Middle' | 'Mass' = 'Mass';
                if (income > 150000) segment = 'Premium';
                else if (income > 80000) segment = 'Middle';

                return {
                    id: id,
                    name: identity.fullName,
                    initials: identity.initials,
                    gender: identity.gender,
                    segment: segment,
                    predicted_income: Math.round(income),
                    risk_level: risk,
                    last_active: 'Недавно'
                };
            });

            res.json(clients);

        } catch (error) {
            console.error('Error fetching clients:', error);
            res.status(500).json({ error: 'Failed to fetch clients' });
        }
    }
};