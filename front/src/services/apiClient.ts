import axios from 'axios';

const API_URL = 'http://localhost:3000/api';

export interface PredictionResponse {
  client_id: string;
  prediction: {
    value: number;
    currency: string;
    confidence: number;
  };
  business_metrics: {
    pdn: number;
    segment: string;
    risk_level: string;
  };
  factors: Array<{
    name: string;
    value: number;
    desc: string;
  }>;
  offers: Array<{
    id: number;
    title: string;
    text: string;
    is_best?: boolean;
  }>;
}

export interface ClientListItem {
  id: string;
  name: string;
  segment: 'Premium' | 'Middle' | 'Mass';
  predicted_income: number;
  risk_level: 'high' | 'medium' | 'low';
  last_active: string;
}

export const apiClient = {
  async getPrediction(id: string): Promise<PredictionResponse> {
    // Делаем запрос на наш бэкенд
    const response = await axios.get(`${API_URL}/clients/${id}/predict`);
    return response.data;
  },

  async getClients(): Promise<ClientListItem[]> {
    const response = await axios.get(`${API_URL}/clients`);
    return response.data;
  }
};