import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

# ==========================================
# 1. letter_grade branch coverage & edge cases
# ==========================================

def test_letter_grade_negative_marks():
    """Branch: marks < 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid marks"):
        letter_grade(-1)

def test_letter_grade_marks_above_100():
    """Branch: marks > 100 raises ValueError."""
    with pytest.raises(ValueError, match="invalid marks"):
        letter_grade(101)

def test_letter_grade_boundary_zero():
    """Boundary test: 0 marks yields grade F."""
    assert letter_grade(0) == "F"

def test_letter_grade_f():
    """Branch: marks < 40 yields grade F."""
    assert letter_grade(39) == "F"

def test_letter_grade_e_boundaries():
    """Branch: 40 <= marks < 50 yields grade E."""
    assert letter_grade(40) == "E"
    assert letter_grade(49) == "E"

def test_letter_grade_d_boundaries():
    """Branch: 50 <= marks < 60 yields grade D."""
    assert letter_grade(50) == "D"
    assert letter_grade(59) == "D"

def test_letter_grade_c_boundaries():
    """Branch: 60 <= marks < 70 yields grade C."""
    assert letter_grade(60) == "C"
    assert letter_grade(69) == "C"

def test_letter_grade_b_boundaries():
    """Branch: 70 <= marks < 80 yields grade B."""
    assert letter_grade(70) == "B"
    assert letter_grade(79) == "B"

def test_letter_grade_a_boundaries():
    """Branch: 80 <= marks < 90 yields grade A."""
    assert letter_grade(80) == "A"
    assert letter_grade(89) == "A"

def test_letter_grade_s_boundaries():
    """Branch: marks >= 90 yields grade S up to 100."""
    assert letter_grade(90) == "S"
    assert letter_grade(100) == "S"


# ==========================================
# 2. final_marks branch coverage & edge cases
# ==========================================

def test_final_marks_invalid_internal():
    """Branch: internal > 40 raises ValueError."""
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(41, 50, False)

def test_final_marks_invalid_external():
    """Branch: external > 60 raises ValueError."""
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(35, 61, False)

def test_final_marks_both_invalid():
    """Branch: internal > 40 and external > 60 raises ValueError."""
    with pytest.raises(ValueError, match="marks out of range"):
        final_marks(45, 65, True)

def test_final_marks_no_project():
    """Branch: has_project is False (branch 23->27)."""
    assert final_marks(35, 50, False) == 85

def test_final_marks_with_project_not_exceeding_100():
    """Branch: has_project is True, but total <= 100 (branch 25->27)."""
    # 30 + 40 + 5 = 75 <= 100
    assert final_marks(30, 40, True) == 75

def test_final_marks_with_project_clamped_to_100():
    """Branch: has_project is True and total > 100, clamped to 100."""
    # 40 + 60 + 5 = 105 > 100 -> clamped to 100
    assert final_marks(40, 60, True) == 100

def test_final_marks_with_project_exact_100():
    """Boundary test: 35 + 60 + 5 = 100 (boundary condition for total > 100)."""
    assert final_marks(35, 60, True) == 100


# ==========================================
# 3. exam_eligibility branch coverage & edge cases
# ==========================================

def test_exam_eligibility_fees_not_paid():
    """Branch: fees_paid is False returns 'blocked' regardless of attendance."""
    assert exam_eligibility(90, False, True) == "blocked"

def test_exam_eligibility_attendance_75_or_more():
    """Branch: fees_paid True and attendance >= 75 returns 'eligible'."""
    assert exam_eligibility(75, True, False) == "eligible"
    assert exam_eligibility(85, True, False) == "eligible"

def test_exam_eligibility_condonation_eligible():
    """Branch: 65 <= attendance < 75 AND has_medical True returns 'eligible'."""
    assert exam_eligibility(65, True, True) == "eligible"
    assert exam_eligibility(74, True, True) == "eligible"

def test_exam_eligibility_condonation_no_medical():
    """Branch: 65 <= attendance < 75 but has_medical is False returns 'detained'."""
    assert exam_eligibility(70, True, False) == "detained"

def test_exam_eligibility_attendance_below_65_with_medical():
    """Branch: attendance < 65 even with has_medical True returns 'detained'."""
    assert exam_eligibility(64, True, True) == "detained"

def test_exam_eligibility_attendance_below_65_without_medical():
    """Branch: attendance < 65 and has_medical False returns 'detained'."""
    assert exam_eligibility(50, True, False) == "detained"
