import { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

const CSV_PATH = path.resolve(process.cwd(), '../ml/data/raw/income_test_clean.csv');

export const analyticsController = {
    async getStats(req: Request, res: Response) {
        try {
            let records: any[] = [];

            // 1. Читаем реальный файл
            if (fs.existsSync(CSV_PATH)) {
                const content = fs.readFileSync(CSV_PATH, 'utf-8');
                // Читаем до 5000 строк для скорости (этого хватит для статистики)
                records = parse(content, {
                    columns: true,
                    delimiter: ';',
                    skip_empty_lines: true,
                    to: 5000
                });
            } else {
                // Если файла нет - генерируем мок
                records = Array.from({ length: 100 }).map(() => ({
                    incomeValue: Math.random() * 200000 + 30000,
                    adminarea: 'Москва'
                }));
            }

            // 2. Считаем метрики
            let totalIncome = 0;
            const segments = { Mass: 0, Middle: 0, Premium: 0 };
            const risks = { Low: 0, Medium: 0, High: 0 };
            const regions: Record<string, number> = {};

            // Гистограмма доходов (bins)
            const incomeDist = { '<50k': 0, '50-100k': 0, '100-150k': 0, '150-250k': 0, '>250k': 0 };

            records.forEach(row => {
                // Пытаемся найти доход в разных полях
                let inc = parseFloat(row.target || row.incomeValue || row.predict || 0);
                if (!inc || isNaN(inc)) inc = 50000; // Fallback

                totalIncome += inc;

                // Сегмент
                if (inc > 150000) segments.Premium++;
                else if (inc > 80000) segments.Middle++;
                else segments.Mass++;

                // Риск (Упрощенно по доходу, т.к. нет кредитов в сыром CSV часто)
                if (inc < 40000) risks.High++;
                else if (inc > 120000) risks.Low++;
                else risks.Medium++;

                // Регион
                const reg = row.adminarea || 'Неизвестно';
                regions[reg] = (regions[reg] || 0) + 1;

                // Гистограмма
                if (inc < 50000) incomeDist['<50k']++;
                else if (inc < 100000) incomeDist['50-100k']++;
                else if (inc < 150000) incomeDist['100-150k']++;
                else if (inc < 250000) incomeDist['150-250k']++;
                else incomeDist['>250k']++;
            });

            const totalClients = records.length;
            const avgIncome = totalClients > 0 ? Math.round(totalIncome / totalClients) : 0;

            // Сортировка регионов (Топ-5)
            const topRegions = Object.entries(regions)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([name, count]) => ({ name, count }));

            res.json({
                totalClients,
                avgIncome,
                totalPortfolio: totalIncome,
                segments,
                risks,
                incomeDist,
                topRegions
            });

        } catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Analytics Error' });
        }
    }
};