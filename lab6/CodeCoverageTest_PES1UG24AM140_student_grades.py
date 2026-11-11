import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

# --- Initial starter test cases ---
def test_s_grade():
    assert letter_grade(95) == "S"

def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"

# --- Additional test cases to achieve 100% statement / code coverage ---
def test_letter_grade_invalid_negative():
    with pytest.raises(ValueError, match="invalid marks"):
        letter_grade(-5)

def test_letter_grade_a():
    assert letter_grade(85) == "A"

def test_letter_grade_b():
    assert letter_grade(75) == "B"

def test_letter_grade_c():
    assert letter_grade(65) == "C"

def test_letter_grade_d():
    assert letter_grade(55) == "D"

def test_letter_grade_e():
    assert letter_grade(45) == "E"

def test_letter_grade_f():
    assert letter_grade(30) == "F"

def test_final_marks_invalid_internal():
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(45, 50, False)

def test_final_marks_with_project_cap():
    # Covers internal+external+project > 100 capped to 100
    assert final_marks(40, 60, True) == 100

def test_exam_eligibility_fees_unpaid():
    assert exam_eligibility(90, False, False) == "blocked"

def test_exam_eligibility_medical_condonation():
    assert exam_eligibility(70, True, True) == "eligible"

def test_exam_eligibility_detained():
    assert exam_eligibility(50, True, False) == "detained"
