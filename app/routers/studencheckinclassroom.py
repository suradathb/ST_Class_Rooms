from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from datetime import datetime
import pandas as pd

router = APIRouter(
    prefix='/api/std/v1',
    tags=['Studen ClassRooms Checkin'],
    responses={404: {'message': 'Not found'}}
)

students_data = []


def check_attendance(names_to_check):
    result = []
    for name in names_to_check:
        found = any(name.lower() == student['name'].lower() for student in students_data)
        result.append({"name": name, "status": "Attended" if found else "Not Enrolled"})
    return result

# @router.get("/")
# def read_root():
#     return {"Hello": "World"}

@router.post("/upload-names/")
async def upload_names(file: UploadFile = File(...)):

    contents = await file.read()
    lines = contents.decode('utf-8').split(',')

    new_students = [{"name": line.strip(), "status": "Not Enrolled"} for line in lines]

    added_students = []
    for new_students in new_students:
        if any(new_students['name'].lower() == student['name'].lower() for student in students_data):
            # Duplicate found, skip adding to students_data
            continue
        else:
            # Not a duplicate, add to students_data
            students_data.append(new_students)
            added_students.append(new_students)
    return {"message": "Names uploaded successfully.", "added_students": added_students}
    # students_data.extend(new_students)
    # return {"message": "Names uploaded successfully."}

@router.post("/check-attendance/")
async def check_attendance_endpoint(names: List[str]):
    if not names:
        return JSONResponse(content={"message": "List of names is empty"}, status_code=400)

    attendance_result = check_attendance(names)
    # Update enrollment status based on attendance
    for student in students_data:
        for result in attendance_result:
            if student['name'].lower() == result['name'].lower():
                student['status'] = result['status']

    return {"attendance_result": attendance_result}

@router.get("/not-enrolled-names/")
async def not_enrolled_names():
    not_enrolled_students = [student for student in students_data if student['status'] == "Not Enrolled"]
    return {"not_enrolled_students": not_enrolled_students}

@router.get("/attended-names/")
async def attended_names():
    attended_students = [student for student in students_data if student['status'] == "Attended"]
    return {"attended_students": attended_students}

@router.post("/add-new-student/")
async def add_new_student(name: str):
    lowercase_name = name.lower()
    
    # Check if the name already exists
    if any(student['name'].lower() == lowercase_name for student in students_data):
        raise HTTPException(status_code=400, detail="Student already exists")

    # Add the new student
    new_student = {"name": name, "status": "Not Enrolled"}
    students_data.append(new_student)

    # Update "fire.txt" with the new student's name
    with open("student_names.txt", "a",encoding="utf-8") as file:
        file.write(f"{name},\n")

    return {"message": "New student added successfully."}

@router.get("/generate-attendance-report/")
async def generate_attendance_report():
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"attendance_report_{current_date}.xlsx"

    save_to_excel(students_data, filename)
    return FileResponse(filename, media_type="application/octet-stream", filename=filename)

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
