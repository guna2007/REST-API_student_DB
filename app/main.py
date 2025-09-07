from typing import List,Dict
from fastapi import FastAPI,HTTPException,Path,Query,status
from pydantic import BaseModel,Field
 
app = FastAPI(title="StudentDB API",version="1.0.0")

class StudentBase(BaseModel):
    name: str = Field(...,min_length=2,max_length=50,examples=["Sai"])
    age: int = Field(...,ge=13,le=24,examples=[17])
    grade: int = Field(...,ge=5,le=10,examples=[7])

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id : int

student_DB : Dict[int, Student] = {}
next_ID : int = 1

@app.get("/")
def root():
    return{"working" : "Good"}

#posting
@app.post("/students",response_model=Student,status_code=status.HTTP_201_CREATED)
def post_student(newstudent : StudentCreate):
    global student_DB,next_ID
    normalized_name = newstudent.name.title()
    student = Student(id = next_ID, name=normalized_name,age=newstudent.age,grade=newstudent.grade)
    student_DB[next_ID] = student
    next_ID+=1
    return student

#query param
@app.get("/students",response_model=List[Student],status_code=status.HTTP_200_OK)
def search_students(
    min_age : int | None = Query(default=None,ge=13,description="Minimum age required"),
    grade : int | None = Query(default=None,ge=5),
    search: str | None = Query(default=None,min_length=1)
):
    data = list(student_DB.values())
    if min_age is not None:
        data = [s for s in data if s.age >= min_age]
    if grade is not None:
        data = [s for s in data if s.grade == grade]
    if search is not None:
        data = [s for s in data if search.lower() in s.name.lower()]

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data not Found")
    return data

#path param 
@app.get("/student/{id}",response_model=Student,status_code=status.HTTP_200_OK)
def getbyID(id : int = Path(...,ge=1)):
    student = student_DB.get(id)
    if student is not None:
        return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data not Found {id}")
    
@app.delete("/student/{id}",status_code=status.HTTP_200_OK)
def deletebyID(id : int = Path(...,ge=1,description="ID of deleting student")):
    if id in student_DB:
        del student_DB[id]
        return {id : "deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not found")
        
@app.put("/student/{id}",response_model=Student,status_code=status.HTTP_200_OK)
def updatebyID(
    id : int = Path(...,ge=1,description="ID to be updated"),
    name : str = Query(default=None,min_length=1),
    age : int = Query(default=None,ge=13,le=24),
    grade : int = Query(default=None,ge=5,le=10)
):
    if id not in student_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not Found")
    
    student = student_DB[id]
    if name is not None:
        student.name = name.strip().title()
    if age is not None:
        student.age = age
    if grade is not None:
        student.grade = grade

    return student
    
