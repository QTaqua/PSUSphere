from django.contrib import admin

from .models import College, Program, Organization, Student, OrgMember


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("college_name", "created_at", "updated_at")
    search_fields = ("college_name",)
    list_filter = ("created_at",)
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("prog_name", "college")
    search_fields = ("prog_name", "college__college_name")
    list_filter = ("college",)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "college", "description")
    search_fields = ("name", "description")
    list_filter = ("college",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname", "firstname", "middlename", "program")
    search_fields = ("lastname", "firstname", "student_id")

@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "organization", "date_joined")
    search_fields = (
        "student__lastname",
        "student__firstname",
        "student__student_id",
    )
    list_select_related = ("student__program", "organization")

    @admin.display(description="Program", ordering="student__program__prog_name")
    def get_member_program(self, obj):
        return obj.student.program
