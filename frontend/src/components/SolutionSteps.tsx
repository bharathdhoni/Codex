import React from 'react';
import type { SolutionStep } from '../../types';
import MathDisplay from './MathDisplay';

interface SolutionStepsProps {
  steps: SolutionStep[];
}

/**
 * Component to display step-by-step solution breakdown
 */
export const SolutionSteps: React.FC<SolutionStepsProps> = ({ steps }) => {
  if (!steps || steps.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No steps available
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Step-by-Step Solution</h3>
      
      {steps.map((step, index) => (
        <div 
          key={step.step_number}
          className="math-step"
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
              {step.step_number}
            </div>
            <div className="flex-1 min-w-0">
              <p className="math-step-description">{step.description}</p>
              <div className="math-expression">
                <MathDisplay latex={step.latex} block />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SolutionSteps;
