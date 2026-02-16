import api from './client';

export interface Profile {
    id: number;
    username: string;
}

export const createProfile = async (username: string, password: string): Promise<Profile> => {
    const response = await api.post('/profiles/', { username, password });
    return response.data;
};

export const getProfile = async (id: number): Promise<Profile> => {
    const response = await api.get(`/profiles/${id}`);
    return response.data;
};

export const getProfileByUsername = async (username: string): Promise<Profile> => {
    const response = await api.get(`/profiles/by-username/${username}`);
    return response.data;
};

export const exportProfileData = async (id: number): Promise<any> => {
    const response = await api.get(`/profiles/${id}/export`);
    return response.data;
};
