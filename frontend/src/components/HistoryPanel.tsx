import React, { useState } from 'react';
import type { HistoryItem } from '../../types';
import MathDisplay from './MathDisplay';

interface HistoryPanelProps {
  history: HistoryItem[];
  isLoading: boolean;
  onSelectItem?: (item: HistoryItem) => void;
  onClear?: () => void;
}

/**
 * Component to display problem solving history
 */
export const HistoryPanel: React.FC<HistoryPanelProps> = ({ 
  history, 
  isLoading,
  onSelectItem,
  onClear 
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="animate-pulse space-y-3">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div 
        className="bg-gradient-to-r from-purple-500 to-indigo-600 px-4 py-3 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">
            History ({history.length})
          </h2>
          <button
            className="text-white hover:text-gray-200 transition-colors"
            aria-label={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? '▼' : '▲'}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="p-4 max-h-96 overflow-y-auto">
          {history.length === 0 ? (
            <p className="text-gray-500 text-center py-4">
              No problems solved yet. Try solving one!
            </p>
          ) : (
            <>
              <div className="space-y-2">
                {history.map((item) => (
                  <div
                    key={item.id}
                    className={`p-3 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                      onSelectItem ? 'hover:border-blue-400 border-gray-200' : 'border-gray-200'
                    }`}
                    onClick={() => onSelectItem?.(item)}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full font-medium uppercase">
                            {item.problem_type}
                          </span>
                          <span className="text-xs text-gray-500">
                            {new Date(item.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="text-sm truncate">
                          <MathDisplay latex={item.expression} />
                        </div>
                        <div className="text-xs text-gray-500 mt-1 truncate">
                          = <MathDisplay latex={item.final_answer} />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {onClear && history.length > 0 && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onClear();
                  }}
                  className="mt-4 w-full py-2 px-4 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
                >
                  Clear History
                </button>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default HistoryPanel;
