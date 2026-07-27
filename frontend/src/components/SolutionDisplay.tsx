import React from 'react';
import type { SolveResponse } from '../../types';
import MathDisplay from './MathDisplay';

interface SolutionDisplayProps {
  result: SolveResponse;
}

/**
 * Component to display the solution result
 */
export const SolutionDisplay: React.FC<SolutionDisplayProps> = ({ result }) => {
  if (!result) {
    return null;
  }

  if (!result.success) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <p className="mt-1 text-sm text-red-700">{result.error_message}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* Header with problem type */}
      <div className="bg-gradient-to-r from-green-400 to-blue-500 px-6 py-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Solution</h2>
          <span className="px-3 py-1 bg-white/20 text-white text-sm rounded-full font-medium uppercase">
            {result.problem_type_detected}
          </span>
        </div>
      </div>

      <div className="p-6">
        {/* Final Answer */}
        <div className="mb-6 pb-6 border-b-2 border-gray-100">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Final Answer
          </h3>
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border-2 border-blue-200">
            <MathDisplay latex={result.final_answer_latex} block />
          </div>
        </div>

        {/* Steps will be rendered by parent component if detailed mode */}
      </div>
    </div>
  );
};

export default SolutionDisplay;
