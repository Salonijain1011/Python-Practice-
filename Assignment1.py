#You are tasked with designing a system for managing a university's course registration. Implement a set of classes using object-oriented principles in Python.
# Create a class Student with the following attributes:
#  student_id (an integer)
# name (a string)
# courses_enrolled (a list of course objects that the student is currently enrolled in)
# Implement a method enroll_course(course) that adds a course object to the student's list of enrolled courses.
# Create a class Course with the following attributes:
# course_code (a string)
# course_name (a string)
# max_students (an integer, indicating the maximum number of students allowed in the course)
# enrolled_students (a list of student objects currently enrolled in the course)
# Implement a method enroll_student(student) that adds a student object to the course's list of enrolled students. Ensure that the number of enrolled students does not exceed the max_students limit.
# Implement a method get_enrolled_students() that returns a list of names of students currently enrolled in the course.
# Create a class University with the following attributes:
# students (a list of student objects)
# courses (a list of course objects)
# Implement a method register_student(student) that adds a student object to the university's list of students.
# Implement a method offer_course (course) that adds a course object to the university's list of courses.
# Implement a method get_students_by_course (course_code) that returns a list of names of students enrolled in a specific course.


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses_enrolled = []
    
    def enroll_course(self, course):
        if course.enroll_student(self):  
            self.courses_enrolled.append(course)

class Course:
    def __init__(self, course_code, course_name, max_student):
        self.course_code = course_code
        self.course_name = course_name
        self.max_student = max_student
        self.enrolled_students = []  
    
    def enroll_student(self, student):
        if len(self.enrolled_students) < self.max_student:
            self.enrolled_students.append(student)
    
    def get_enrolled_students(self):
        return [student.name for student in self.enrolled_students]

class University:
    def __init__(self):
        self.students = []
        self.courses = []
    
    def register_student(self, student):
        self.students.append(student)
    
    def offer_course(self, course):
        self.courses.append(course)
    
    def get_students_by_course(self, course_name):
        for course in self.courses:
            if course.course_name == course_name:
                return course.get_enrolled_students()
        return []

u = University()
s1 = Student(1, "Saloni")
s2 = Student(2, "John")

course1 = Course("001", "Python", 10)

u.register_student(s1)
u.register_student(s2)
u.offer_course(course1)

s1.enroll_course(course1)  
s2.enroll_course(course1)

print(u.get_students_by_course("Python")) 
print(course1.get_enrolled_students())
        
    
            
        
        

        

        
        
        
        
            
                  
            
             
                 
                 
    