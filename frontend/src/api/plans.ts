import api from './client';

export interface Plan {
    id: number;
    title: string;
    description?: string;
    profile_id: number;
}

export const getPlans = async (): Promise<Plan[]> => {
    const response = await api.get('/plans/');
    return response.data;
};

export const createPlan = async (userId: number, title: string, description?: string): Promise<Plan> => {
    const response = await api.post(`/plans/${userId}/`, { title, description });
    return response.data;
};
