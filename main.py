"""
Student Performance Analytics System
Run: python main.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.csv"
SUBJECTS = ["Python", "Mathematics", "Statistics", "AI_Fundamentals"]
PASS_MARK = 40
ATTENDANCE_THRESHOLD = 75


def assign_grade(average):
    """Return a letter grade based on the student's average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    elif average >= 40:
        return "E"
    return "F"


def process_student_records(data):
    """Calculate totals, averages, grades and pass/fail status."""
    data = data.copy()
    data["Total_Marks"] = data[SUBJECTS].sum(axis=1)
    data["Average_Marks"] = data[SUBJECTS].mean(axis=1).round(2)

    # A student passes only when every subject mark is at least PASS_MARK.
    data["Result"] = np.where((data[SUBJECTS] >= PASS_MARK).all(axis=1), "PASS", "FAIL")
    data["Grade"] = [assign_grade(avg) for avg in data["Average_Marks"]]
    data["Attendance_Status"] = np.where(
        data["Attendance_Percent"] >= ATTENDANCE_THRESHOLD, "Eligible", "Low Attendance"
    )
    return data


def load_dataset(path=DATA_FILE):
    """Load and validate the CSV dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    data = pd.read_csv(path)
    required = ["Student_ID", "Name", "Department", *SUBJECTS, "Attendance_Percent"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if data.empty:
        raise ValueError("The dataset contains no student records.")
    if data[required].isnull().any().any():
        raise ValueError("The dataset contains blank values in required columns.")
    for subject in SUBJECTS:
        if not data[subject].between(0, 100).all():
            raise ValueError(f"{subject} marks must be between 0 and 100.")
    if not data["Attendance_Percent"].between(0, 100).all():
        raise ValueError("Attendance_Percent must be between 0 and 100.")
    return data


def print_section(title):
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)


def display_summary(data):
    print_section("STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print(f"Records loaded: {len(data)}")
    print(f"Departments: {', '.join(sorted(data['Department'].unique()))}")
    print("\nStudent results:")
    view_cols = ["Student_ID", "Name", "Department", "Total_Marks",
                 "Average_Marks", "Grade", "Result", "Attendance_Status"]
    print(data[view_cols].to_string(index=False))

    print_section("CLASS SUMMARY")
    print(f"Class average: {data['Average_Marks'].mean():.2f} / 100")
    print(f"Highest student average: {data['Average_Marks'].max():.2f}")
    print(f"Lowest student average: {data['Average_Marks'].min():.2f}")
    print(f"Students passed: {(data['Result'] == 'PASS').sum()}")
    print(f"Students failed: {(data['Result'] == 'FAIL').sum()}")
    print(f"Pass percentage: {(data['Result'].eq('PASS').mean() * 100):.2f}%")
    print(f"Attendance >= {ATTENDANCE_THRESHOLD}%: "
          f"{(data['Attendance_Status'] == 'Eligible').sum()} students")

    print_section("SUBJECT-WISE PERFORMANCE")
    subject_means = data[SUBJECTS].mean().sort_values(ascending=False)
    subject_summary = pd.DataFrame({
        "Average": data[SUBJECTS].mean(),
        "Highest": data[SUBJECTS].max(),
        "Lowest": data[SUBJECTS].min(),
        "Pass_Count": (data[SUBJECTS] >= PASS_MARK).sum()
    }).round(2).sort_values("Average", ascending=False)
    print(subject_summary.to_string())
    print(f"\nBest-performing subject: {subject_means.index[0]} ({subject_means.iloc[0]:.2f})")
    print(f"Lowest-average subject: {subject_means.index[-1]} ({subject_means.iloc[-1]:.2f})")

    print_section("TOP 5 STUDENTS")
    top_students = data.nlargest(min(5, len(data)), "Average_Marks")
    print(top_students[["Student_ID", "Name", "Department", "Average_Marks", "Grade"]]
          .to_string(index=False))

    print_section("DEPARTMENT-WISE AVERAGE")
    dept_summary = data.groupby("Department")["Average_Marks"].agg(["mean", "max", "min", "count"])
    dept_summary.columns = ["Average", "Highest", "Lowest", "Students"]
    print(dept_summary.round(2).to_string())

    print_section("GRADE DISTRIBUTION")
    print(data["Grade"].value_counts().reindex(["A+", "A", "B", "C", "D", "E", "F"], fill_value=0)
          .rename_axis("Grade").to_string())


def save_processed_data(data):
    output_path = BASE_DIR / "output"
    output_path.mkdir(exist_ok=True)
    data.to_csv(output_path / "student_results.csv", index=False)
    subject_report = data[SUBJECTS].agg(["mean", "max", "min"]).T.round(2)
    subject_report.to_csv(output_path / "subject_summary.csv")
    print(f"\nSaved detailed results to: {output_path / 'student_results.csv'}")
    print(f"Saved subject summary to: {output_path / 'subject_summary.csv'}")


def main():
    try:
        raw_data = load_dataset()
        processed_data = process_student_records(raw_data)
        display_summary(processed_data)
        save_processed_data(processed_data)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
