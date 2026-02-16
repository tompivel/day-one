import api from './client';

export interface Session {
    id: number;
    description: string;
    sport: string;
    duration_minutes: number;
    date_start: string;
    perceived_exertion: number;
    microcycle_id: number;
}

export const getSessions = async (microcycleId: number): Promise<Session[]> => {
    const response = await api.get(`/sessions/${microcycleId}/`);
    return response.data;
};

export interface SessionCreate {
    description: string;
    sport: string;
    duration_minutes: number;
    date_start: string;
    perceived_exertion: number;
}

export const createSession = async (microcycleId: number, session: SessionCreate): Promise<Session> => {
    const response = await api.post(`/sessions/${microcycleId}/`, session);
    return response.data;
};
