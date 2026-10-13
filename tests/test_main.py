import unittest
import pandas as pd
from main import SUBJECTS, assign_grade, process_student_records


class TestStudentAnalytics(unittest.TestCase):
    def test_grade_boundaries(self):
        self.assertEqual(assign_grade(95), "A+")
        self.assertEqual(assign_grade(80), "A")
        self.assertEqual(assign_grade(70), "B")
        self.assertEqual(assign_grade(60), "C")
        self.assertEqual(assign_grade(50), "D")
        self.assertEqual(assign_grade(40), "E")
        self.assertEqual(assign_grade(39.99), "F")

    def test_totals_average_and_pass(self):
        row = {
            "Student_ID": "TEST01", "Name": "Test Student", "Department": "ECE",
            "Python": 80, "Mathematics": 70, "Statistics": 90,
            "AI_Fundamentals": 60, "Attendance_Percent": 80
        }
        result = process_student_records(pd.DataFrame([row])).iloc[0]
        self.assertEqual(result["Total_Marks"], 300)
        self.assertEqual(result["Average_Marks"], 75)
        self.assertEqual(result["Result"], "PASS")
        self.assertEqual(result["Grade"], "B")

    def test_one_subject_below_pass_mark_fails(self):
        row = {
            "Student_ID": "TEST02", "Name": "Test Student", "Department": "CSE",
            "Python": 39, "Mathematics": 90, "Statistics": 90,
            "AI_Fundamentals": 90, "Attendance_Percent": 90
        }
        result = process_student_records(pd.DataFrame([row])).iloc[0]
        self.assertEqual(result["Result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
