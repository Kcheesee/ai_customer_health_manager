import axios from 'axios';
import type { LLMConfig, LLMConfigUpdate } from '../types/llm';

const API_URL = 'http://localhost:8000/api/v1/settings/llm';

export const llmService = {
    getConfig: async (): Promise<LLMConfig> => {
        const response = await axios.get(`${API_URL}/`);
        return response.data;
    },

    updateConfig: async (config: LLMConfigUpdate): Promise<LLMConfig> => {
        const response = await axios.put(`${API_URL}/`, config);
        return response.data;
    },

    testConnection: async (config: LLMConfigUpdate): Promise<{ status: string; response: string }> => {
        const response = await axios.post(`${API_URL}/test`, config);
        return response.data;
    }
};
