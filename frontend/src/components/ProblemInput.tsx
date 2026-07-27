import React, { useState } from 'react';
import type { SolveRequest } from '../../types';

interface ProblemInputProps {
  onSubmit: (request: SolveRequest) => void;
  isLoading: boolean;
}

const PROBLEM_TYPES = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'algebra', label: 'Algebra' },
  { value: 'equation', label: 'Equation' },
  { value: 'derivative', label: 'Derivative' },
  { value: 'integral', label: 'Integral' },
  { value: 'limit', label: 'Limit' },
] as const;

/**
 * Main input component for entering math problems
 * Supports text input with LaTeX-style syntax
 */
export const ProblemInput: React.FC<ProblemInputProps> = ({ onSubmit, isLoading }) => {
  const [expression, setExpression] = useState('');
  const [problemType, setProblemType] = useState<SolveRequest['problem_type']>('auto');
  const [detailed, setDetailed] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!expression.trim()) {
      return;
    }

    onSubmit({
      expression: expression.trim(),
      problem_type: problemType,
      detailed,
    });
  };

  const handleQuickInsert = (text: string) => {
    setExpression(prev => prev + text);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="bg-white rounded-lg shadow-md p-6">
        <label htmlFor="expression" className="block text-sm font-medium text-gray-700 mb-2">
          Enter your math problem
        </label>
        
        <textarea
          id="expression"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
          placeholder="e.g., x^2 + 2*x + 1 or d/dx(x^3) or integral x^2"
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all resize-none text-lg font-mono"
          rows={3}
          disabled={isLoading}
        />

        {/* Quick insert buttons for common symbols */}
        <div className="flex flex-wrap gap-2 mt-3">
          <button
            type="button"
            onClick={() => handleQuickInsert('^')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
            title="Power/Exponent"
          >
            x^n
          </button>
          <button
            type="button"
            onClick={() => handleQuickInsert('sqrt(')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
            title="Square root"
          >
            √
          </button>
          <button
            type="button"
            onClick={() => handleQuickInsert('sin(')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
          >
            sin
          </button>
          <button
            type="button"
            onClick={() => handleQuickInsert('cos(')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
          >
            cos
          </button>
          <button
            type="button"
            onClick={() => handleQuickInsert('integrate ')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
          >
            ∫
          </button>
          <button
            type="button"
            onClick={() => handleQuickInsert('d/dx(')}
            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm font-mono transition-colors"
          >
            d/dx
          </button>
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Problem type selector */}
          <div>
            <label htmlFor="problemType" className="block text-sm font-medium text-gray-700 mb-2">
              Problem Type
            </label>
            <select
              id="problemType"
              value={problemType}
              onChange={(e) => setProblemType(e.target.value as SolveRequest['problem_type'])}
              className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              disabled={isLoading}
            >
              {PROBLEM_TYPES.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {/* Detailed mode toggle */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Solution Mode
            </label>
            <label className="flex items-center cursor-pointer">
              <div className="relative">
                <input
                  type="checkbox"
                  checked={detailed}
                  onChange={(e) => setDetailed(e.target.checked)}
                  className="sr-only"
                  disabled={isLoading}
                />
                <div className={`block w-14 h-8 rounded-full transition-colors ${
                  detailed ? 'bg-blue-500' : 'bg-gray-300'
                }`}></div>
                <div className={`absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform ${
                  detailed ? 'transform translate-x-6' : ''
                }`}></div>
              </div>
              <span className="ml-3 text-sm text-gray-600">
                {detailed ? 'Detailed Steps' : 'Quick Answer'}
              </span>
            </label>
          </div>
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={!expression.trim() || isLoading}
          className={`w-full mt-6 py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            !expression.trim() || isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-md hover:shadow-lg'
          }`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Solving...
            </span>
          ) : (
            'Solve Problem'
          )}
        </button>
      </div>

      {/* Help text */}
      <div className="text-xs text-gray-500 bg-blue-50 p-3 rounded-lg">
        <strong>Examples:</strong>
        <ul className="list-disc list-inside mt-1 space-y-1">
          <li>Algebra: <code className="bg-white px-1 rounded">x^2 + 5*x + 6</code></li>
          <li>Equation: <code className="bg-white px-1 rounded">2*x + 3 = 7</code></li>
          <li>Derivative: <code className="bg-white px-1 rounded">d/dx(x^3)</code></li>
          <li>Integral: <code className="bg-white px-1 rounded">integral x^2</code></li>
        </ul>
      </div>
    </form>
  );
};

export default ProblemInput;
