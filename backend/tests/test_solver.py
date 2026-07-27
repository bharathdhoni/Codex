"""
Unit tests for the SymPy-based math solver
"""

import pytest
from app.services.solver import MathSolver


@pytest.fixture
def solver():
    """Create a solver instance for testing"""
    return MathSolver()


class TestMathSolver:
    """Test cases for the MathSolver class"""
    
    def test_simplify_basic_expression(self, solver):
        """Test simplifying a basic algebraic expression"""
        result = solver.solve("x^2 + 2*x + x^2", "algebra")
        assert result["success"] is True
        assert result["problem_type_detected"] == "algebra"
        assert len(result["steps"]) > 0
    
    def test_solve_linear_equation(self, solver):
        """Test solving a linear equation"""
        result = solver.solve("2*x + 3 = 7", "equation")
        assert result["success"] is True
        assert result["problem_type_detected"] == "equation"
        assert "x =" in result["final_answer"]
    
    def test_solve_quadratic_equation(self, solver):
        """Test solving a quadratic equation"""
        result = solver.solve("x^2 - 5*x + 6 = 0", "equation")
        assert result["success"] is True
        # Should find solutions x=2 and x=3
        assert "2" in result["final_answer"] or "3" in result["final_answer"]
    
    def test_compute_derivative_power_rule(self, solver):
        """Test computing derivative using power rule"""
        result = solver.solve("d/dx(x^3)", "derivative")
        assert result["success"] is True
        assert result["problem_type_detected"] == "derivative"
        # Derivative of x^3 should be 3*x^2
        assert "3" in result["final_answer"]
    
    def test_compute_derivative_product_rule(self, solver):
        """Test computing derivative using product rule"""
        result = solver.solve("d/dx(x^2 * sin(x))", "derivative")
        assert result["success"] is True
    
    def test_compute_integral_power_rule(self, solver):
        """Test computing integral using power rule"""
        result = solver.solve("integral x^2", "integral")
        assert result["success"] is True
        assert result["problem_type_detected"] == "integral"
        # Should include constant of integration
        assert "C" in result["final_answer"]
    
    def test_auto_detect_equation(self, solver):
        """Test auto-detection of equation type"""
        result = solver.solve("x + 5 = 10", "auto")
        assert result["problem_type_detected"] == "equation"
    
    def test_auto_detect_algebra(self, solver):
        """Test auto-detection of algebra type"""
        result = solver.solve("x^2 + 2*x + 1", "auto")
        assert result["problem_type_detected"] == "algebra"
    
    def test_invalid_expression(self, solver):
        """Test handling of invalid expressions"""
        result = solver.solve("invalid+++expression", "auto")
        # Should handle gracefully
        assert isinstance(result, dict)
    
    def test_factor_expression(self, solver):
        """Test factoring an expression"""
        result = solver.solve("x^2 + 5*x + 6", "algebra")
        assert result["success"] is True
        # Should factor to (x+2)(x+3)
        steps_text = str(result["steps"])
        assert len(result["steps"]) > 0
    
    def test_steps_have_required_fields(self, solver):
        """Test that each step has required fields"""
        result = solver.solve("x^2 + 2*x", "algebra")
        assert result["success"] is True
        
        for step in result["steps"]:
            assert "step_number" in step
            assert "description" in step
            assert "expression" in step
            assert "latex" in step
    
    def test_latex_output(self, solver):
        """Test that LaTeX output is generated"""
        result = solver.solve("x^2", "algebra")
        assert result["success"] is True
        assert result["final_answer_latex"] != ""
        assert "x" in result["final_answer_latex"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
