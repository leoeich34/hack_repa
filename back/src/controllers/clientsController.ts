import { Request, Response } from 'express';

// Генерируем фейковых людей
const firstNames = ['Александр', 'Мария', 'Дмитрий', 'Елена', 'Андрей', 'Ольга', 'Сергей', 'Анна'];
const lastNames = ['Иванов(а)', 'Смирнов(а)', 'Кузнецов(а)', 'Попов(а)', 'Соколов(а)', 'Лебедев(а)'];

const getRandom = (arr: any[]) => arr[Math.floor(Math.random() * arr.length)];

export const clientsController = {
    async getList(req: Request, res: Response) {
        // Имитация базы данных
        const clients = Array.from({ length: 15 }).map((_, index) => {
            const id = 1000 + index;
            const income = Math.floor(40000 + Math.random() * 300000);
            const pdn = Math.floor(Math.random() * 60);

            return {
                id: id.toString(),
                name: `${getRandom(lastNames)} ${getRandom(firstNames)}`,
                avatar_seed: `client_${id}`, // Для генерации аватарки
                segment: income > 150000 ? 'Premium' : (income > 80000 ? 'Middle' : 'Mass'),
                predicted_income: income,
                risk_level: pdn > 50 ? 'high' : (pdn > 30 ? 'medium' : 'low'),
                last_active: 'Сегодня'
            };
        });

        // Имитация задержки сети
        await new Promise(r => setTimeout(r, 500));

        res.json(clients);
    }
};