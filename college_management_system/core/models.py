from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Users(models.Model):
    """
    Custom user model extending Django's built-in User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    full_name = models.CharField(max_length=255)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('hod', 'Head of Department'),
        ('faculty', 'Faculty'),
        ('lab_assistant', 'Lab Assistant'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.role}"

class Student(models.Model):
    """
    Student model as per the ER diagram
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, primary_key=True)
    batch_name = models.CharField(max_length=50)
    admission_year = models.IntegerField()
    graduation_year = models.IntegerField()
    program = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    current_semester = models.IntegerField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.roll_number} - {self.user.user_profile.full_name}"

class Faculty(models.Model):
    """
    Faculty model as per the ER diagram
    """
    faculty_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_year = models.IntegerField()
    weekly_hours_limit = models.IntegerField()
    current_weekly_hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee_id} - {self.user.user_profile.full_name}"

class Subject(models.Model):
    """
    Subject model as per the ER diagram
    """
    subject_id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    credits = models.IntegerField()
    is_elective = models.BooleanField(default=False)
    prerequisite_subjects = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

class SubjectFaculty(models.Model):
    """
    Subject-Faculty relationship model as per the ER diagram
    """
    subject_faculty_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    academic_year_start = models.IntegerField()
    academic_year_end = models.IntegerField()

    def __str__(self):
        return f"{self.subject.subject_name} - {self.faculty.user.user_profile.full_name}"

class StudentSubject(models.Model):
    """
    Student-Subject relationship model as per the ER diagram
    """
    student_subject_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField()
    academic_year = models.IntegerField()

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.subject_name}"

class SemesterProgression(models.Model):
    """
    Semester progression model as per the ER diagram
    """
    progression_id = models.AutoField(primary_key=True)
    prerequisite_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='prerequisite_for')
    next_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='next_for')

    def __str__(self):
        return f"{self.prerequisite_subject.subject_name} -> {self.next_subject.subject_name}"

class Timetable(models.Model):
    """
    Timetable model as per the ER diagram
    """
    timetable_id = models.AutoField(primary_key=True)
    subject_faculty = models.ForeignKey(SubjectFaculty, on_delete=models.CASCADE)
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)
    is_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject_faculty.subject.subject_name} - {self.day_of_week} {self.start_time}"

class Attendance(models.Model):
    """
    Attendance model as per the ER diagram
    """
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_faculty = models.ForeignKey(SubjectFaculty, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    recorded_at = models.DateTimeField(default=timezone.now)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject_faculty.subject.subject_name} - {self.attendance_date}"