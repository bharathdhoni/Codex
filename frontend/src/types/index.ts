export interface SolutionStep {
  step_number: number;
  description: string;
  expression: string;
  latex: string;
}

export interface SolveRequest {
  expression: string;
  problem_type?: 'algebra' | 'calculus' | 'derivative' | 'integral' | 'limit' | 'equation' | 'auto';
  detailed?: boolean;
}

export interface SolveResponse {
  success: boolean;
  final_answer: string;
  final_answer_latex: string;
  steps: SolutionStep[];
  problem_type_detected: string;
  error_message?: string | null;
}

export interface HistoryItem {
  id: number;
  expression: string;
  problem_type: string;
  final_answer: string;
  created_at: string;
}
