import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';

interface MathDisplayProps {
  latex: string;
  block?: boolean;
  className?: string;
}

/**
 * Component to render LaTeX math expressions using KaTeX
 * Automatically handles inline vs block rendering
 */
export const MathDisplay: React.FC<MathDisplayProps> = ({ 
  latex, 
  block = false,
  className = ''
}) => {
  if (!latex) {
    return <span className="text-gray-400 italic">No expression</span>;
  }

  try {
    if (block) {
      return <BlockMath math={latex} className={`my-2 ${className}`} />;
    } else {
      return <InlineMath math={latex} className={className} />;
    }
  } catch (error) {
    // Fallback for invalid LaTeX
    console.warn('KaTeX rendering error:', error);
    return <span className="text-red-500 text-sm">Invalid LaTeX: {latex}</span>;
  }
};

export default MathDisplay;
