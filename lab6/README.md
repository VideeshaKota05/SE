# Lab 6: Code and Branch Coverage Analysis

**Student ID:** PES1UG24AM140  
**Course:** Software Engineering Lab  
**Assigned Repository:** `SETAPESU26/L6_L7_16_student_grades`

---

## 1. Overview & Objectives

The goal of this lab is to understand, measure, and improve test coverage using Python's `coverage` tool and `pytest`. Specifically, this experiment analyzes:
- The distinction between **Line (Statement) Coverage** and **Branch Coverage**.
- How achieving 100% line coverage can still leave logical pathways untested.
- Systematic testing methodologies (boundary value analysis and decision-to-decision path testing) to achieve 100% branch and statement coverage.

---

## 2. Software Requirements & Setup

Install required tools:
```powershell
pip install coverage pytest
```

Verify installation:
```powershell
python -m coverage --version
python -m pytest --version
```

---

## 3. Application Under Test (`student_grades.py`)

The application consists of three functions:
1. `letter_grade(marks)`: Validates marks in range `[0, 100]` and maps numeric score to letter grades (`S`, `A`, `B`, `C`, `D`, `E`, `F`). Raises `ValueError` for negative values or values exceeding 100.
2. `final_marks(internal, external, has_project)`: Validates `internal <= 40` and `external <= 60`. If `has_project` is True, awards a 5-mark bonus, capped at 100. Raises `ValueError` for out-of-range inputs.
3. `exam_eligibility(attendance, fees_paid, has_medical)`: Determines student exam eligibility (`"blocked"`, `"eligible"`, or `"detained"`) based on fee clearance and attendance criteria (>= 75% normally, or >= 65% with approved medical leave).

---

## 4. Coverage Analysis Progression

### Phase 1: Baseline (Initial Starter Tests)
- **Test File:** `test_student_grades.py` (2 starter test cases: `test_s_grade` and `test_eligible`)
- **Commands:**
  ```powershell
  coverage run -m pytest test_student_grades.py
  coverage report -m
  coverage run --branch -m pytest test_student_grades.py
  coverage report -m
  ```
- **Results:**
  - **Statement Coverage:** **27%** (24 of 33 statements missed: lines 3, 6-16, 20-27, 32, 35-37)
  - **Branch Coverage:** **22%** (4 partial branches executed out of 26)

---

### Phase 2: Code Coverage Suite (>90% target, 100% achieved)
- **Deliverables:** `CodeCoverageTest_student_grades.py` / `CodeCoverageTest_PES1UG24AM140_student_grades.py`
- **Screenshot:** `screenshots/code_coverage_100.png`
- **Report Output:** `code_coverage_report.txt`
- **Result:**
  - **Statement Coverage:** **100%** (33/33 statements executed, 0 missed)
  - **Branch Coverage:** **97%** (2 branches partial: `23->27` when `has_project` is False, `25->27` when `total <= 100`)
- **Key Observation:**
  Even though 100% statement coverage was reached because every line executed at least once, branches were still missing. For example, `final_marks` always ran with `has_project=True` and `total > 100`, leaving the alternate decisions unexercised.

---

### Phase 3: Branch Coverage Suite (>90% target, 100% achieved)
- **Deliverables:** `BranchCoverageTest_student_grades.py` / `BranchCoverageTest_PES1UG24AM140_student_grades.py`
- **Screenshot:** `screenshots/branch_coverage_100.png`
- **Report Output:** `branch_coverage_report.txt`
- **Result:**
  - **Statement Coverage:** **100%** (33/33 statements executed, 0 missed)
  - **Branch Coverage:** **100%** (26/26 branches executed, 0 partial, 0 missed)

#### Comprehensive Branch Coverage Test Matrix

| Function | Decision / Branch Condition | Test Input | Expected Result / Path |
|---|---|---|---|
| `letter_grade` | `marks < 0` (True) | `marks = -1` | Raises `ValueError("invalid marks")` |
| `letter_grade` | `marks > 100` (True) | `marks = 101` | Raises `ValueError("invalid marks")` |
| `letter_grade` | `marks >= 90` (True) | `marks = 90`, `marks = 100` | `"S"` |
| `letter_grade` | `marks >= 80` (True) | `marks = 80`, `marks = 89` | `"A"` |
| `letter_grade` | `marks >= 70` (True) | `marks = 70`, `marks = 79` | `"B"` |
| `letter_grade` | `marks >= 60` (True) | `marks = 60`, `marks = 69` | `"C"` |
| `letter_grade` | `marks >= 50` (True) | `marks = 50`, `marks = 59` | `"D"` |
| `letter_grade` | `marks >= 40` (True) | `marks = 40`, `marks = 49` | `"E"` |
| `letter_grade` | `marks < 40` (Fallthrough) | `marks = 0`, `marks = 39` | `"F"` |
| `final_marks` | `internal > 40` (True) | `internal = 41, external = 50` | Raises `ValueError("marks out of range")` |
| `final_marks` | `external > 60` (True) | `internal = 35, external = 61` | Raises `ValueError("marks out of range")` |
| `final_marks` | Both invalid | `internal = 45, external = 65` | Raises `ValueError("marks out of range")` |
| `final_marks` | `has_project` (False) | `35, 50, False` | `85` (skips project bonus) |
| `final_marks` | `has_project` (True), `total <= 100` | `30, 40, True` | `75` (bonus added, no clamp) |
| `final_marks` | `has_project` (True), `total > 100` | `40, 60, True` | `100` (bonus added, clamped to 100) |
| `final_marks` | `total == 100` exactly | `35, 60, True` | `100` (boundary test) |
| `exam_eligibility` | `not fees_paid` (True) | `attendance = 90, fees_paid = False, has_medical = True` | `"blocked"` |
| `exam_eligibility` | `attendance >= 75` (True) | `attendance = 75, 85, fees_paid = True, has_medical = False` | `"eligible"` |
| `exam_eligibility` | `65 <= attendance < 75` and `has_medical` (True) | `attendance = 65, 74, fees_paid = True, has_medical = True` | `"eligible"` (medical waiver) |
| `exam_eligibility` | `65 <= attendance < 75` and `has_medical` (False) | `attendance = 70, fees_paid = True, has_medical = False` | `"detained"` |
| `exam_eligibility` | `attendance < 65` and `has_medical` (True) | `attendance = 64, fees_paid = True, has_medical = True` | `"detained"` |
| `exam_eligibility` | `attendance < 65` and `has_medical` (False) | `attendance = 50, fees_paid = True, has_medical = False` | `"detained"` |

---

## 5. Comparative Coverage Summary

| Metric | Initial State | Code Coverage Suite | Branch Coverage Suite |
|---|:---:|:---:|:---:|
| **Statements Total** | 33 | 33 | 33 |
| **Statements Missed** | 24 | 0 | 0 |
| **Statement Coverage %** | **27%** | **100%** | **100%** |
| **Branches Total** | 26 | 26 | 26 |
| **Branches Partial / Missed** | 4 partial / 20 missed | 2 partial | 0 |
| **Branch Coverage %** | **22%** | **97%** | **100%** |
| **Number of Unit Tests** | 2 | 14 | 23 |
| **Test Execution Status** | 2 Passed | 14 Passed | 23 Passed |

---

## 6. How to Run the Tests

Execute full branch coverage and view detailed missing report:
```powershell
cd lab6
coverage erase
coverage run --branch -m pytest BranchCoverageTest_student_grades.py
coverage report -m
```

Execute code coverage:
```powershell
cd lab6
coverage erase
coverage run -m pytest CodeCoverageTest_student_grades.py
coverage report -m
```
