import api from './client';

export interface Macrocycle {
    id: number;
    name: string;
    plan_id: number;
}

export const getMacrocycles = async (planId: number): Promise<Macrocycle[]> => {
    const response = await api.get(`/macrocycles/${planId}/`);
    return response.data;
};

export const createMacrocycle = async (planId: number, name: string): Promise<Macrocycle> => {
    const response = await api.post(`/macrocycles/${planId}/`, { name });
    return response.data;
};
