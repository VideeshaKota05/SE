
# Lab 5 – Static Code Analysis

**Student ID:** PES1UG24AM140

**Project:** Animal Shelter Adoption Register

**File:** pet_shelter.py

## Issues Identified and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SQL injection (B608) | Security – Medium | 10 | SQL values were inserted using string formatting. | Used parameterized SQL queries. |
| Insecure random generation (B311) | Security – Low | 22 | random.randint() was used for adoption codes. | Replaced random with secrets. |
| Silent exception handling (B110) | Security – Low | 36 | Exceptions were caught and silently ignored. | Removed try-except-pass. |
| Mutable default argument | Bug | 9 | A shared list was used as a default argument. | Replaced [] with None. |
| Bare exception | Code quality | 29 | A bare except statement caught unspecified exceptions. | Added explicit handling of empty database results. |
| Broad exception handling | Code quality | 36 | A general Exception handler suppressed errors. | Removed unnecessary exception handling. |
| Global statement | Code quality | 16 | Global adoption_count was used. | Encapsulated functionality in a class. |
| Naming conventions | Code quality | 9, 21, 25, 33, 40 | Function names did not follow snake_case. | Renamed functions using snake_case. |
| Missing documentation | Code quality | 1, 9, 15, 21, 25, 33, 40, 45 | Module and functions lacked docstrings. | Added documentation strings. |
| Long lines (E501) | Style | 5, 10, 27 | Lines exceeded the 79-character limit. | Reformatted long statements. |
| Bare except (E722) | Style | 29 | An unspecified exception handler was used. | Removed bare except. |
| Multiple statements (E701) | Style | 41 | Multiple statements appeared on one line. | Separated statements. |

## Conclusion

The original program was analyzed using Pylint, Bandit and Flake8. The identified code quality, security and formatting issues were corrected. All three tools were executed again to verify the improvements.
