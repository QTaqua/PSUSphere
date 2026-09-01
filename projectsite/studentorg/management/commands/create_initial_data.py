from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from studentorg.models import College, OrgMember, Organization, Program, Student


COLLEGES_AND_PROGRAMS = {
    "College of Computing Sciences": [
        "Bachelor of Science in Computer Science",
        "Bachelor of Science in Information Technology",
    ],
    "College of Business and Public Administration": [
        "Bachelor of Science in Business Administration",
        "Bachelor of Public Administration",
    ],
    "College of Education": [
        "Bachelor of Elementary Education",
        "Bachelor of Secondary Education",
    ],
    "College of Engineering and Architecture": [
        "Bachelor of Science in Civil Engineering",
    ],
    "College of Arts and Humanities": [
        "Bachelor of Arts in Communication",
    ],
    "College of Science": [
        "Bachelor of Science in Biology",
    ],
    "College of Tourism and Hospitality Management": [
        "Bachelor of Science in Hospitality Management",
    ],
    "College of Agriculture": [],
}


class Command(BaseCommand):
    help = "Create prerequisite colleges/programs and sample application data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.create_colleges_and_programs()
        self.create_organizations(10)
        self.create_students(50)
        self.create_memberships(10)
        self.stdout.write(self.style.SUCCESS("Initial PSUSphere data created successfully."))

    def create_colleges_and_programs(self):
        for college_name, program_names in COLLEGES_AND_PROGRAMS.items():
            college, _ = College.objects.get_or_create(college_name=college_name)
            for program_name in program_names:
                Program.objects.get_or_create(prog_name=program_name, college=college)

    def create_organizations(self, count):
        fake = Faker()
        colleges = list(College.objects.all())
        for _ in range(count):
            name = " ".join(fake.words(nb=2)).title()
            Organization.objects.create(
                name=name,
                college=fake.random_element(colleges),
                description=fake.sentence(),
            )

    def create_students(self, count):
        fake = Faker("en_PH")
        programs = list(Program.objects.all())
        for _ in range(count):
            Student.objects.create(
                student_id=self.unique_student_id(fake),
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name(),
                program=fake.random_element(programs),
            )

    def unique_student_id(self, fake):
        while True:
            student_id = (
                f"{fake.random_int(2020, 2026)}-"
                f"{fake.random_int(1, 8)}-"
                f"{fake.random_number(digits=4, fix_len=True)}"
            )
            if not Student.objects.filter(student_id=student_id).exists():
                return student_id

    def create_memberships(self, count):
        fake = Faker()
        students = list(Student.objects.all())
        organizations = list(Organization.objects.all())
        for _ in range(count):
            OrgMember.objects.create(
                student=fake.random_element(students),
                organization=fake.random_element(organizations),
                date_joined=fake.date_between(start_date="-2y", end_date="today"),
            )
