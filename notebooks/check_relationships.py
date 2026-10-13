import pandas as pd
from pathlib import Path

DATA_DIR = Path("../Dataset/OULAD")

# Load required files
student_info = pd.read_csv(DATA_DIR / "studentInfo.csv")
student_assessment = pd.read_csv(DATA_DIR / "studentAssessment.csv")
assessments = pd.read_csv(DATA_DIR / "assessments.csv")
student_vle = pd.read_csv(DATA_DIR / "studentVle.csv")
vle = pd.read_csv(DATA_DIR / "vle.csv")

print("\n" + "=" * 70)
print("1. STUDENT INFORMATION")
print("=" * 70)

print("Unique students:", student_info["id_student"].nunique())
print("Student records:", len(student_info))

print("\nFinal result distribution:")
print(student_info["final_result"].value_counts())


print("\n" + "=" * 70)
print("2. ASSESSMENT RELATIONSHIP")
print("=" * 70)

print("Unique assessments in assessments.csv:",
      assessments["id_assessment"].nunique())

print("Unique assessments in studentAssessment.csv:",
      student_assessment["id_assessment"].nunique())

print("Assessment IDs missing from assessments.csv:",
      len(set(student_assessment["id_assessment"])
          - set(assessments["id_assessment"])))


print("\n" + "=" * 70)
print("3. STUDENT-ASSESSMENT CONNECTION")
print("=" * 70)

print("Students with assessment records:",
      student_assessment["id_student"].nunique())

print("Average assessment score:",
      round(student_assessment["score"].mean(), 2))

print("Missing assessment scores:",
      student_assessment["score"].isna().sum())


print("\n" + "=" * 70)
print("4. STUDENT-VLE CONNECTION")
print("=" * 70)

print("Unique students in studentVle:",
      student_vle["id_student"].nunique())

print("Unique VLE sites in studentVle:",
      student_vle["id_site"].nunique())

print("Unique VLE sites in vle:",
      vle["id_site"].nunique())

print("VLE sites missing from vle.csv:",
      len(set(student_vle["id_site"]) - set(vle["id_site"])))


print("\n" + "=" * 70)
print("5. VLE ACTIVITY TYPES")
print("=" * 70)

print(vle["activity_type"].value_counts())


print("\n" + "=" * 70)
print("6. STUDENT ENGAGEMENT")
print("=" * 70)

print("Total VLE click records:", len(student_vle))

print("Total clicks:",
      student_vle["sum_click"].sum())

print("Average clicks per record:",
      round(student_vle["sum_click"].mean(), 2))


print("\n" + "=" * 70)
print("7. MODULES")
print("=" * 70)

print("Modules:")
print(sorted(student_info["code_module"].unique()))

print("\nNumber of students by module:")
print(student_info["code_module"].value_counts())


print("\n" + "=" * 70)
print("8. FINAL RESULT BY MODULE")
print("=" * 70)

result_table = pd.crosstab(
    student_info["code_module"],
    student_info["final_result"]
)

print(result_table)


print("\n" + "=" * 70)
print("RELATIONSHIP CHECK COMPLETED")
print("=" * 70)