"""
SymPy-based math solver with step-by-step solution generation.
Supports algebra (simplification, factoring, equations) and calculus (derivatives, integrals, limits).
"""

from sympy import (
    symbols, sympify, simplify, factor, expand, solve, Eq, 
    diff, integrate, limit, Symbol, S,
    Pow, Add, Mul, MatAdd, MatMul
)
from sympy.parsing.latex import parse_latex
from sympy.printing.latex import latex
from typing import List, Dict, Any, Optional, Tuple
import re


class MathSolver:
    """Core math solving engine using SymPy"""
    
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.t, self.n = symbols('t n')
        self.all_symbols = [self.x, self.y, self.z, self.t, self.n]
    
    def parse_expression(self, expr_str: str) -> Any:
        """Parse a string expression into a SymPy object"""
        try:
            # Try parsing as LaTeX first
            if '\\frac' in expr_str or '\\sqrt' in expr_str or '^' in expr_str:
                try:
                    return parse_latex(expr_str)
                except:
                    pass
            
            # Parse as standard SymPy expression
            # Replace common user input patterns
            expr_str = expr_str.replace('^', '**')
            expr_str = expr_str.replace('sqrt', 'sqrt')
            
            # Auto-detect variables if not present
            expr = sympify(expr_str, locals={
                'x': self.x, 'y': self.y, 'z': self.z,
                't': self.t, 'n': self.n,
                'sin': __import__('sympy').sin,
                'cos': __import__('sympy').cos,
                'tan': __import__('sympy').tan,
                'exp': __import__('sympy').exp,
                'log': __import__('sympy').log,
                'ln': __import__('sympy').log,
                'pi': __import__('sympy').pi,
                'E': __import__('sympy').E,
                'I': __import__('sympy').I,
            })
            return expr
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def detect_problem_type(self, expr_str: str) -> str:
        """Auto-detect the type of problem from the expression"""
        expr_lower = expr_str.lower()
        
        # Check for calculus keywords
        if any(kw in expr_lower for kw in ['d/dx', 'derivative', '∂']):
            return 'derivative'
        if any(kw in expr_lower for kw in ['integral', '∫', 'integrate']):
            return 'integral'
        if 'limit' in expr_lower or 'lim' in expr_lower:
            return 'limit'
        
        # Check for equation (contains =)
        if '=' in expr_str and not '==' in expr_str:
            return 'equation'
        
        # Try to parse and analyze
        try:
            expr = self.parse_expression(expr_str)
            
            # Check if it's an equality
            if isinstance(expr, Eq):
                return 'equation'
            
            # Check for derivatives/integrals in parsed form
            expr_type = str(type(expr))
            if 'Derivative' in expr_type:
                return 'derivative'
            if 'Integral' in expr_type:
                return 'integral'
            
            # Default to algebra
            return 'algebra'
        except:
            return 'algebra'
    
    def simplify_expression(self, expr: Any) -> List[Dict[str, str]]:
        """Generate steps for simplifying an expression"""
        steps = []
        
        original_latex = latex(expr)
        steps.append({
            "step_number": 1,
            "description": "Original expression",
            "expression": str(expr),
            "latex": original_latex
        })
        
        # Step 1: Expand if it's a product
        if isinstance(expr, Mul):
            expanded = expand(expr)
            if expanded != expr:
                steps.append({
                    "step_number": len(steps) + 1,
                    "description": "Expand the expression using distributive property",
                    "expression": str(expanded),
                    "latex": latex(expanded)
                })
                expr = expanded
        
        # Step 2: Combine like terms
        simplified = simplify(expr)
        if simplified != expr:
            steps.append({
                "step_number": len(steps) + 1,
                "description": "Combine like terms and simplify",
                "expression": str(simplified),
                "latex": latex(simplified)
            })
        
        # Step 3: Factor if possible
        factored = factor(simplified)
        if factored != simplified and factored != expr:
            steps.append({
                "step_number": len(steps) + 1,
                "description": "Factor the expression to find common factors",
                "expression": str(factored),
                "latex": latex(factored)
            })
        
        return steps
    
    def solve_equation(self, expr: Any) -> List[Dict[str, str]]:
        """Generate steps for solving an equation"""
        steps = []
        
        # Ensure it's an equality
        if not isinstance(expr, Eq):
            if '=' in str(expr):
                parts = str(expr).split('=')
                expr = Eq(self.parse_expression(parts[0]), self.parse_expression(parts[1]))
            else:
                expr = Eq(expr, 0)
        
        lhs_latex = latex(expr.lhs)
        rhs_latex = latex(expr.rhs)
        
        steps.append({
            "step_number": 1,
            "description": f"Given equation: {lhs_latex} = {rhs_latex}",
            "expression": str(expr),
            "latex": f"{lhs_latex} = {rhs_latex}"
        })
        
        # Move all terms to one side
        moved = expr.lhs - expr.rhs
        moved_simplified = simplify(moved)
        
        steps.append({
            "step_number": 2,
            "description": "Move all terms to one side to set equation to zero",
            "expression": str(moved_simplified),
            "latex": f"{latex(moved_simplified)} = 0"
        })
        
        # Try factoring
        factored = factor(moved_simplified)
        if factored != moved_simplified:
            steps.append({
                "step_number": 3,
                "description": "Factor the expression",
                "expression": str(factored),
                "latex": latex(factored)
            })
        
        # Solve
        solutions = solve(expr, dict=True)
        
        if solutions:
            for i, sol in enumerate(solutions):
                var = list(sol.keys())[0]
                val = sol[var]
                steps.append({
                    "step_number": len(steps) + 1,
                    "description": f"Solve for {var}",
                    "expression": f"{var} = {val}",
                    "latex": f"{latex(var)} = {latex(val)}"
                })
        
        return steps
    
    def compute_derivative(self, expr: Any, var: Optional[Symbol] = None) -> List[Dict[str, str]]:
        """Generate steps for computing a derivative"""
        steps = []
        
        if var is None:
            var = self.x
        
        original_latex = latex(expr)
        steps.append({
            "step_number": 1,
            "description": f"Find the derivative with respect to {var}",
            "expression": f"d/d{var}({expr})",
            "latex": f"\\frac{{d}}{{d{var}}}\\left({original_latex}\\right)"
        })
        
        # Apply differentiation rules based on expression type
        result = diff(expr, var)
        
        if isinstance(expr, Pow):
            base = expr.base
            exp = expr.exp
            steps.append({
                "step_number": 2,
                "description": "Apply the power rule: d/dx(x^n) = n·x^(n-1)",
                "expression": str(result),
                "latex": latex(result)
            })
        elif isinstance(expr, Mul):
            steps.append({
                "step_number": 2,
                "description": "Apply the product rule: d/dx(f·g) = f'·g + f·g'",
                "expression": str(result),
                "latex": latex(result)
            })
        elif isinstance(expr, Add):
            steps.append({
                "step_number": 2,
                "description": "Apply the sum rule: differentiate each term separately",
                "expression": str(result),
                "latex": latex(result)
            })
        else:
            steps.append({
                "step_number": 2,
                "description": "Compute the derivative",
                "expression": str(result),
                "latex": latex(result)
            })
        
        # Simplify if needed
        simplified_result = simplify(result)
        if simplified_result != result:
            steps.append({
                "step_number": len(steps) + 1,
                "description": "Simplify the result",
                "expression": str(simplified_result),
                "latex": latex(simplified_result)
            })
        
        return steps
    
    def compute_integral(self, expr: Any, var: Optional[Symbol] = None) -> List[Dict[str, str]]:
        """Generate steps for computing an integral"""
        steps = []
        
        if var is None:
            var = self.x
        
        original_latex = latex(expr)
        steps.append({
            "step_number": 1,
            "description": f"Find the indefinite integral with respect to {var}",
            "expression": f"∫{expr} d{var}",
            "latex": f"\\int {original_latex} \\, d{var}"
        })
        
        # Try to compute the integral
        try:
            result = integrate(expr, var)
            
            if isinstance(expr, Pow) and expr.exp != -1:
                steps.append({
                    "step_number": 2,
                    "description": "Apply the power rule for integration: ∫x^n dx = x^(n+1)/(n+1) + C",
                    "expression": str(result),
                    "latex": latex(result)
                })
            elif isinstance(expr, Add):
                steps.append({
                    "step_number": 2,
                    "description": "Apply the sum rule: integrate each term separately",
                    "expression": str(result),
                    "latex": latex(result)
                })
            else:
                steps.append({
                    "step_number": 2,
                    "description": "Compute the antiderivative",
                    "expression": str(result),
                    "latex": latex(result)
                })
            
            # Add constant of integration
            steps.append({
                "step_number": len(steps) + 1,
                "description": "Add the constant of integration",
                "expression": f"{result} + C",
                "latex": f"{latex(result)} + C"
            })
            
        except Exception as e:
            steps.append({
                "step_number": 2,
                "description": f"Integral could not be computed in closed form: {str(e)}",
                "expression": str(expr),
                "latex": original_latex
            })
        
        return steps
    
    def compute_limit(self, expr: Any, var: Symbol, point: Any) -> List[Dict[str, str]]:
        """Generate steps for computing a limit"""
        steps = []
        
        original_latex = latex(expr)
        point_latex = latex(point)
        
        steps.append({
            "step_number": 1,
            "description": f"Find the limit as {var} approaches {point_latex}",
            "expression": f"lim({var}→{point}) {expr}",
            "latex": f"\\lim_{{{var} \\to {point_latex}}} {original_latex}"
        })
        
        # Try direct substitution
        try:
            direct_sub = expr.subs(var, point)
            if direct_sub.is_number:
                steps.append({
                    "step_number": 2,
                    "description": "Try direct substitution",
                    "expression": str(direct_sub),
                    "latex": latex(direct_sub)
                })
                result = direct_sub
            else:
                result = limit(expr, var, point)
                steps.append({
                    "step_number": 2,
                    "description": "Apply limit laws and simplify",
                    "expression": str(result),
                    "latex": latex(result)
                })
        except:
            result = limit(expr, var, point)
            steps.append({
                "step_number": 2,
                "description": "Evaluate the limit",
                "expression": str(result),
                "latex": latex(result)
            })
        
        return steps
    
    def solve(self, expression: str, problem_type: str = "auto") -> Dict[str, Any]:
        """
        Main solving method that routes to appropriate solver
        Returns a dictionary with success status, answer, and steps
        """
        try:
            # Auto-detect problem type if needed
            if problem_type == "auto":
                problem_type = self.detect_problem_type(expression)
            
            # Parse the expression
            expr = self.parse_expression(expression)
            
            # Route to appropriate solver
            if problem_type in ['algebra', 'simplify']:
                steps = self.simplify_expression(expr)
                final_answer = steps[-1]['expression'] if steps else str(expr)
                final_answer_latex = steps[-1]['latex'] if steps else latex(expr)
            
            elif problem_type == 'equation':
                steps = self.solve_equation(expr)
                solutions = solve(expr, dict=True)
                if solutions:
                    final_answer = ', '.join([f"{list(s.keys())[0]} = {list(s.values())[0]}" for s in solutions])
                    final_answer_latex = ', '.join([f"{latex(list(s.keys())[0])} = {latex(list(s.values())[0])}" for s in solutions])
                else:
                    final_answer = "No solution found"
                    final_answer_latex = "\\text{No solution found}"
            
            elif problem_type == 'derivative':
                # Extract variable if specified
                var = self.x
                steps = self.compute_derivative(expr, var)
                final_answer = steps[-1]['expression'] if steps else str(diff(expr, var))
                final_answer_latex = steps[-1]['latex'] if steps else latex(diff(expr, var))
            
            elif problem_type == 'integral':
                var = self.x
                steps = self.compute_integral(expr, var)
                final_answer = steps[-1]['expression'] if steps else str(integrate(expr, var)) + " + C"
                final_answer_latex = steps[-1]['latex'] if steps else latex(integrate(expr, var)) + " + C"
            
            elif problem_type == 'limit':
                # Default limit as x->0
                var = self.x
                point = 0
                steps = self.compute_limit(expr, var, point)
                final_answer = steps[-1]['expression'] if steps else str(limit(expr, var, point))
                final_answer_latex = steps[-1]['latex'] if steps else latex(limit(expr, var, point))
            
            else:
                # Default to simplification
                steps = self.simplify_expression(expr)
                final_answer = steps[-1]['expression'] if steps else str(simplify(expr))
                final_answer_latex = steps[-1]['latex'] if steps else latex(simplify(expr))
            
            return {
                "success": True,
                "final_answer": final_answer,
                "final_answer_latex": final_answer_latex,
                "steps": steps,
                "problem_type_detected": problem_type,
                "error_message": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "final_answer": "",
                "final_answer_latex": "",
                "steps": [],
                "problem_type_detected": problem_type,
                "error_message": str(e)
            }
