import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

// Список папок, где мы будем искать файл сабмита
// process.cwd() в нашем случае — это папка 'back'
const SEARCH_PATHS = [
    path.resolve(process.cwd(), '../'),              // 1. Корень проекта
    path.resolve(process.cwd(), '../ml/data/raw'),   // 2. ML Data Raw
    path.resolve(process.cwd(), '../ml/reports')     // 3. ML Reports
];

interface SubmissionMap {
    [clientId: string]: number;
}

let submissionCache: SubmissionMap | null = null;

export const getSubmissionValue = (clientId: string): number | null => {
    // Если кэш пуст, пробуем загрузить (один раз при старте или первом запросе)
    if (!submissionCache) {
        submissionCache = loadSubmissions();
    }

    // Ищем клиента в кэше
    if (submissionCache && submissionCache[clientId] !== undefined) {
        return submissionCache[clientId];
    }

    return null;
};

const loadSubmissions = (): SubmissionMap => {
    const map: SubmissionMap = {};
    let foundFile = '';

    try {
        // Проходимся по всем папкам
        for (const dir of SEARCH_PATHS) {
            if (!fs.existsSync(dir)) continue;

            const files = fs.readdirSync(dir);
            // Ищем файл, содержащий 'submission' или 'submit'
            const submitFile = files.find(f =>
                (f.toLowerCase().includes('submission') || f.toLowerCase().includes('submit'))
                && f.endsWith('.csv')
            );

            if (submitFile) {
                foundFile = path.join(dir, submitFile);
                console.log(`✅ Found submission file: ${foundFile}`);
                break; // Нашли - выходим из цикла
            }
        }

        if (!foundFile) {
            console.log('⚠️ No submission files found in search paths.');
            return map;
        }

        // Читаем файл
        const content = fs.readFileSync(foundFile, 'utf-8');
        const records = parse(content, {
            columns: true,
            skip_empty_lines: true,
            delimiter: [',', ';', '\t'], // Поддержка запятой, точки с запятой и табов
            trim: true
        });

        // Парсим строки
        records.forEach((row: any) => {
            // Пытаемся найти ID под разными именами
            const idVal = row.id || row.client_id || row.Id || row.ID;

            // Пытаемся найти Target под разными именами
            const targetVal = row.target || row.predict || row.prediction || row.income || row.Target;

            if (idVal && targetVal) {
                // Очищаем от лишних символов (на случай "100,50")
                const cleanTarget = String(targetVal).replace(',', '.').replace(/\s/g, '');
                const val = parseFloat(cleanTarget);

                if (!isNaN(val)) {
                    map[String(idVal)] = val;
                }
            }
        });

        console.log(`📊 Loaded predictions for ${Object.keys(map).length} clients.`);

    } catch (e) {
        console.error('❌ Error loading submission file:', e);
    }

    return map;
};