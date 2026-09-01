from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CollegeForm, OrgMemberForm, OrganizationForm, ProgramForm, StudentForm
from .models import College, OrgMember, Organization, Program, Student


class SearchableListMixin:
    search_fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if not query or not self.search_fields:
            return queryset

        filters = Q()
        for field in self.search_fields:
            filters |= Q(**{f"{field}__icontains": query})
        return queryset.filter(filters)


class HomePageView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = "home"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context.update(
            total_students=Student.objects.count(),
            total_organizations=Organization.objects.count(),
            total_programs=Program.objects.count(),
            students_joined_this_year=(
                OrgMember.objects.filter(date_joined__year=today.year)
                .values("student")
                .distinct()
                .count()
            ),
        )
        return context


class OrganizationList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = Organization
    context_object_name = "organization"
    template_name = "org_list.html"
    paginate_by = 5
    ordering = ("college__college_name", "name")
    search_fields = ("name", "description", "college__college_name")

    def get_queryset(self):
        return super().get_queryset().select_related("college")


class ProgramList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = Program
    context_object_name = "program"
    template_name = "program_list.html"
    paginate_by = 5
    search_fields = ("prog_name", "college__college_name")

    def get_queryset(self):
        return super().get_queryset().select_related("college")

    def get_ordering(self):
        allowed = {
            "prog_name": "prog_name",
            "college__college_name": "college__college_name",
        }
        return allowed.get(self.request.GET.get("sort_by"), "prog_name")


class CollegeList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = College
    context_object_name = "college"
    template_name = "college_list.html"
    paginate_by = 5
    ordering = ("college_name",)
    search_fields = ("college_name",)


class StudentList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = Student
    context_object_name = "student"
    template_name = "student_list.html"
    paginate_by = 5
    ordering = ("lastname", "firstname")
    search_fields = (
        "student_id",
        "lastname",
        "firstname",
        "middlename",
        "program__prog_name",
    )

    def get_queryset(self):
        return super().get_queryset().select_related("program", "program__college")


class OrgMemberList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = OrgMember
    context_object_name = "org_member"
    template_name = "orgmember_list.html"
    paginate_by = 5
    search_fields = (
        "student__student_id",
        "student__lastname",
        "student__firstname",
        "organization__name",
    )

    def get_queryset(self):
        return super().get_queryset().select_related(
            "student",
            "student__program",
            "organization",
        )

    def get_ordering(self):
        allowed = {
            "student": ("student__lastname", "student__firstname"),
            "date_joined": ("date_joined",),
            "-date_joined": ("-date_joined",),
        }
        return allowed.get(
            self.request.GET.get("sort_by"),
            ("student__lastname", "student__firstname"),
        )


class ModelPermissionRequiredMixin(PermissionRequiredMixin):
    permission_action = None
    raise_exception = True

    def get_permission_required(self):
        opts = self.model._meta
        return (f"{opts.app_label}.{self.permission_action}_{opts.model_name}",)


class ProtectedCreateView(LoginRequiredMixin, ModelPermissionRequiredMixin, CreateView):
    template_name = "entity_form.html"
    permission_action = "add"


class ProtectedUpdateView(LoginRequiredMixin, ModelPermissionRequiredMixin, UpdateView):
    template_name = "entity_form.html"
    permission_action = "change"


class ProtectedDeleteView(LoginRequiredMixin, ModelPermissionRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    permission_action = "delete"


class OrganizationCreateView(ProtectedCreateView):
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy("organization-list")
    extra_context = {"page_title": "Add organization"}


class OrganizationUpdateView(ProtectedUpdateView):
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy("organization-list")
    extra_context = {"page_title": "Update organization"}


class OrganizationDeleteView(ProtectedDeleteView):
    model = Organization
    success_url = reverse_lazy("organization-list")


class ProgramCreateView(ProtectedCreateView):
    model = Program
    form_class = ProgramForm
    success_url = reverse_lazy("program-list")
    extra_context = {"page_title": "Add program"}


class ProgramUpdateView(ProtectedUpdateView):
    model = Program
    form_class = ProgramForm
    success_url = reverse_lazy("program-list")
    extra_context = {"page_title": "Update program"}


class ProgramDeleteView(ProtectedDeleteView):
    model = Program
    success_url = reverse_lazy("program-list")


class CollegeCreateView(ProtectedCreateView):
    model = College
    form_class = CollegeForm
    success_url = reverse_lazy("college-list")
    extra_context = {"page_title": "Add college"}


class CollegeUpdateView(ProtectedUpdateView):
    model = College
    form_class = CollegeForm
    success_url = reverse_lazy("college-list")
    extra_context = {"page_title": "Update college"}


class CollegeDeleteView(ProtectedDeleteView):
    model = College
    success_url = reverse_lazy("college-list")


class StudentCreateView(ProtectedCreateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("student-list")
    extra_context = {"page_title": "Add student"}


class StudentUpdateView(ProtectedUpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("student-list")
    extra_context = {"page_title": "Update student"}


class StudentDeleteView(ProtectedDeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class OrgMemberCreateView(ProtectedCreateView):
    model = OrgMember
    form_class = OrgMemberForm
    success_url = reverse_lazy("orgmember-list")
    extra_context = {"page_title": "Add organization member"}


class OrgMemberUpdateView(ProtectedUpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    success_url = reverse_lazy("orgmember-list")
    extra_context = {"page_title": "Update organization member"}


class OrgMemberDeleteView(ProtectedDeleteView):
    model = OrgMember
    success_url = reverse_lazy("orgmember-list")
