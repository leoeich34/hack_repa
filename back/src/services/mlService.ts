import axios from 'axios';

// Адрес твоего Python ML-сервиса
const ML_URL = 'http://127.0.0.1:8000';

export interface MLResponse {
    client_id: string;
    predicted_income: number;
    model_version: string;
    shap_values: Array<{ name: string; value: number; desc: string }>;
}

export const mlService = {
    async predictIncome(clientData: any): Promise<MLResponse> {
        try {
            console.log('Sending data to ML:', ML_URL);

            // Отправляем POST запрос на Python FastAPI
            const response = await axios.post(`${ML_URL}/predict`, {
                client_id: clientData.id || "unknown",
                features: clientData // Передаем все данные клиента
            });

            return response.data;

        } catch (error: any) { // <--- ИСПРАВЛЕНИЕ: Добавили : any
            console.error('ML Service Error:', error.message || error);

            // Если ML недоступен, возвращаем запасной вариант (чтобы сайт не упал)
            return {
                client_id: clientData.id || "unknown",
                predicted_income: 60000, // Дефолтное значение
                model_version: "fallback_mock",
                shap_values: [
                    { name: 'Ошибка соединения', value: 0, desc: 'ML сервис недоступен' }
                ]
            };
        }
    }
};