import axios from 'axios';
import type { SolveRequest, SolveResponse, HistoryItem } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const solveProblem = async (request: SolveRequest): Promise<SolveResponse> => {
  try {
    const response = await api.post<SolveResponse>('/solve', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to solve problem');
    }
    throw error;
  }
};

export const getHistory = async (limit: number = 20): Promise<HistoryItem[]> => {
  try {
    const response = await api.get<HistoryItem[]>(`/history?limit=${limit}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch history');
    }
    throw error;
  }
};

export const clearHistory = async (): Promise<void> => {
  try {
    await api.delete('/history');
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to clear history');
    }
    throw error;
  }
};
