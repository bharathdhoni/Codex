import { useState, useCallback } from 'react';
import type { SolveRequest, SolveResponse } from '../types';
import { solveProblem } from '../services/api';

interface UseSolverReturn {
  result: SolveResponse | null;
  isLoading: boolean;
  error: string | null;
  solve: (request: SolveRequest) => Promise<void>;
  clearResult: () => void;
}

export const useSolver = (): UseSolverReturn => {
  const [result, setResult] = useState<SolveResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const solve = useCallback(async (request: SolveRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await solveProblem(request);
      setResult(response);
      
      if (!response.success) {
        setError(response.error_message || 'Failed to solve problem');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { result, isLoading, error, solve, clearResult };
};
