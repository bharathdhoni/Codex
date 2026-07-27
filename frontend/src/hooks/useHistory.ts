import { useEffect, useState } from 'react';
import type { HistoryItem } from '../types';
import { getHistory, clearHistory } from '../services/api';

interface UseHistoryReturn {
  history: HistoryItem[];
  isLoading: boolean;
  error: string | null;
  refreshHistory: () => Promise<void>;
  clearAll: () => Promise<void>;
}

export const useHistory = (): UseHistoryReturn => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshHistory = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const items = await getHistory();
      setHistory(items);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load history';
      setError(errorMessage);
      setHistory([]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearAll = async () => {
    try {
      await clearHistory();
      await refreshHistory();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to clear history';
      setError(errorMessage);
    }
  };

  useEffect(() => {
    refreshHistory();
  }, []);

  return { history, isLoading, error, refreshHistory, clearAll };
};
