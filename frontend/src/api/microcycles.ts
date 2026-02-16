import api from './client';

export interface Microcycle {
    id: number;
    name: string;
    macrocycle_id: number;
}

export const getMicrocycles = async (macrocycleId: number): Promise<Microcycle[]> => {
    const response = await api.get(`/microcycles/${macrocycleId}/`);
    return response.data;
};

export const createMicrocycle = async (macrocycleId: number, name: string): Promise<Microcycle> => {
    const response = await api.post(`/microcycles/${macrocycleId}/`, { name });
    return response.data;
};
