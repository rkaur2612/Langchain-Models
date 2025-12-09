from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str = 'Raman'
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(gt=0, lt=10, default=5, description='decimal value representing cgpa of student')

new_student = {'age': 30, 'email': 'test@gmail.com'}

student = Student(**new_student)

student_dict= dict(student)

print(student_dict['age'])

student_json = student.model_dump_json()
print(student_json)