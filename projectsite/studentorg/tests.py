import os
import subprocess
import sys
from datetime import date
from io import StringIO
from pathlib import Path

from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone

from .admin import OrgMemberAdmin
from .models import College, OrgMember, Organization, Program, Student


class StudentOrgTestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="psu-admin",
            email="admin@example.com",
            password="test-password-123",
        )
        cls.college = College.objects.create(college_name="College of Computing Sciences")
        cls.program = Program.objects.create(
            prog_name="Bachelor of Science in Computer Science",
            college=cls.college,
        )
        cls.organization = Organization.objects.create(
            name="Association of Computing Students",
            college=cls.college,
            description="A community for computing students.",
        )
        cls.student = Student.objects.create(
            student_id="2026-1-0001",
            lastname="Dela Cruz",
            firstname="Alex",
            program=cls.program,
        )
        cls.membership = OrgMember.objects.create(
            student=cls.student,
            organization=cls.organization,
            date_joined=timezone.localdate(),
        )

    def setUp(self):
        self.client.force_login(self.user)


class AuthenticationTests(StudentOrgTestData):
    def test_home_redirects_anonymous_users_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, f"{reverse('account_login')}?next=/")

    def test_login_page_hides_unconfigured_social_providers(self):
        self.client.logout()
        response = self.client.get(reverse("account_login"))
        self.assertNotContains(response, "Continue with Google")
        self.assertNotContains(response, "Continue with GitHub")

    def test_login_page_shows_only_configured_social_providers(self):
        site, _ = Site.objects.update_or_create(
            pk=settings.SITE_ID,
            defaults={"domain": "testserver", "name": "PSUSphere Tests"},
        )
        for provider, name in (("google", "Google"), ("github", "GitHub")):
            app = SocialApp.objects.create(
                provider=provider,
                name=name,
                client_id=f"{provider}-client-id",
                secret=f"{provider}-client-secret",
            )
            app.sites.add(site)

        self.client.logout()
        response = self.client.get(reverse("account_login"))
        self.assertContains(response, "Continue with Google")
        self.assertContains(response, "Continue with GitHub")
        self.assertEqual(self.client.get(reverse("google_login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("github_login")).status_code, 200)

    def test_logout_requires_post(self):
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign out?")
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.post(reverse("account_logout"))
        self.assertRedirects(response, reverse("account_login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_social_signup_template_uses_the_psusphere_design(self):
        template = get_template("socialaccount/signup.html")
        self.assertIn("Finish your profile", template.template.source)
        self.assertIn("ready.css", template.template.source)


class DashboardTests(StudentOrgTestData):
    def test_dashboard_counts_registry_data(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.context["total_students"], 1)
        self.assertEqual(response.context["total_organizations"], 1)
        self.assertEqual(response.context["total_programs"], 1)
        self.assertEqual(response.context["students_joined_this_year"], 1)

    def test_joined_count_is_distinct_and_current_year_only(self):
        second_org = Organization.objects.create(
            name="Software Society",
            college=self.college,
            description="Software builders.",
        )
        OrgMember.objects.create(
            student=self.student,
            organization=second_org,
            date_joined=timezone.localdate(),
        )
        older_student = Student.objects.create(
            student_id="2025-1-9999",
            lastname="Old",
            firstname="Member",
            program=self.program,
        )
        OrgMember.objects.create(
            student=older_student,
            organization=second_org,
            date_joined=date(timezone.localdate().year - 1, 6, 1),
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.context["students_joined_this_year"], 1)


class ListViewTests(StudentOrgTestData):
    def test_all_list_pages_are_available(self):
        for name in (
            "organization-list",
            "orgmember-list",
            "student-list",
            "college-list",
            "program-list",
        ):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_search_is_available_on_every_list(self):
        cases = (
            ("organization-list", "Computing", self.organization),
            ("orgmember-list", "2026-1-0001", self.membership),
            ("student-list", "Dela Cruz", self.student),
            ("college-list", "Computing", self.college),
            ("program-list", "Computer Science", self.program),
        )
        for route_name, query, expected in cases:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name), {"q": query})
                self.assertIn(expected, response.context["object_list"])

    def test_program_sorting_by_college(self):
        first_college = College.objects.create(college_name="A College")
        first_program = Program.objects.create(prog_name="Z Program", college=first_college)
        response = self.client.get(
            reverse("program-list"),
            {"sort_by": "college__college_name"},
        )
        self.assertEqual(response.context["object_list"][0], first_program)

    def test_member_sorting_by_newest_joined(self):
        second_student = Student.objects.create(
            student_id="2026-1-0002",
            lastname="Zulu",
            firstname="Bea",
            program=self.program,
        )
        newest = OrgMember.objects.create(
            student=second_student,
            organization=self.organization,
            date_joined=date(2099, 1, 1),
        )
        response = self.client.get(reverse("orgmember-list"), {"sort_by": "-date_joined"})
        self.assertEqual(response.context["object_list"][0], newest)


class CrudViewTests(StudentOrgTestData):
    def test_create_views_for_all_models(self):
        cases = (
            ("college-add", {"college_name": "College of Science"}, College, 1),
            (
                "program-add",
                {"prog_name": "Bachelor of Science in Biology", "college": self.college.pk},
                Program,
                1,
            ),
            (
                "organization-add",
                {"name": "Math Circle", "college": self.college.pk, "description": "Math community"},
                Organization,
                1,
            ),
            (
                "student-add",
                {
                    "student_id": "2026-1-0003",
                    "lastname": "Santos",
                    "firstname": "Mia",
                    "middlename": "",
                    "program": self.program.pk,
                },
                Student,
                1,
            ),
            (
                "orgmember-add",
                {
                    "student": self.student.pk,
                    "organization": self.organization.pk,
                    "date_joined": "2026-08-31",
                },
                OrgMember,
                1,
            ),
        )
        for route_name, data, model, added in cases:
            with self.subTest(route_name=route_name):
                before = model.objects.count()
                response = self.client.post(reverse(route_name), data)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(model.objects.count(), before + added)

    def test_update_views_for_all_models(self):
        cases = (
            ("college-update", self.college.pk, {"college_name": "Updated College"}, College, "college_name", "Updated College"),
            ("program-update", self.program.pk, {"prog_name": "Updated Program", "college": self.college.pk}, Program, "prog_name", "Updated Program"),
            ("organization-update", self.organization.pk, {"name": "Updated Org", "college": self.college.pk, "description": "Updated"}, Organization, "name", "Updated Org"),
            ("student-update", self.student.pk, {"student_id": self.student.student_id, "lastname": "Updated", "firstname": "Alex", "middlename": "", "program": self.program.pk}, Student, "lastname", "Updated"),
            ("orgmember-update", self.membership.pk, {"student": self.student.pk, "organization": self.organization.pk, "date_joined": "2026-01-02"}, OrgMember, "date_joined", date(2026, 1, 2)),
        )
        for route_name, pk, data, model, field, expected in cases:
            with self.subTest(route_name=route_name):
                response = self.client.post(reverse(route_name, args=[pk]), data)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(getattr(model.objects.get(pk=pk), field), expected)

    def test_delete_views_for_all_models(self):
        college = College.objects.create(college_name="Delete College")
        program = Program.objects.create(prog_name="Delete Program", college=self.college)
        organization = Organization.objects.create(name="Delete Org", description="Delete")
        student = Student.objects.create(student_id="2026-8-9999", lastname="Delete", firstname="Me", program=self.program)
        membership = OrgMember.objects.create(student=self.student, organization=self.organization, date_joined=timezone.localdate())
        cases = (
            ("orgmember-delete", membership),
            ("student-delete", student),
            ("organization-delete", organization),
            ("program-delete", program),
            ("college-delete", college),
        )
        for route_name, instance in cases:
            with self.subTest(route_name=route_name):
                response = self.client.post(reverse(route_name, args=[instance.pk]))
                self.assertEqual(response.status_code, 302)
                self.assertFalse(type(instance).objects.filter(pk=instance.pk).exists())


class AuthorizationTests(StudentOrgTestData):
    def setUp(self):
        self.member_user = get_user_model().objects.create_user(
            username="registry-reader",
            email="reader@example.com",
            password="test-password-123",
        )
        self.client.force_login(self.member_user)

    def test_regular_accounts_can_view_registry_pages(self):
        for name in (
            "home",
            "organization-list",
            "orgmember-list",
            "student-list",
            "college-list",
            "program-list",
        ):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_regular_accounts_cannot_open_mutation_pages(self):
        cases = (
            ("organization-add", ()),
            ("organization-update", (self.organization.pk,)),
            ("organization-delete", (self.organization.pk,)),
            ("program-add", ()),
            ("program-update", (self.program.pk,)),
            ("program-delete", (self.program.pk,)),
            ("college-add", ()),
            ("college-update", (self.college.pk,)),
            ("college-delete", (self.college.pk,)),
            ("student-add", ()),
            ("student-update", (self.student.pk,)),
            ("student-delete", (self.student.pk,)),
            ("orgmember-add", ()),
            ("orgmember-update", (self.membership.pk,)),
            ("orgmember-delete", (self.membership.pk,)),
        )
        for name, args in cases:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 403)

    def test_regular_account_cannot_submit_delete(self):
        response = self.client.post(
            reverse("organization-delete", args=(self.organization.pk,))
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Organization.objects.filter(pk=self.organization.pk).exists())


class AdminTests(StudentOrgTestData):
    def test_membership_admin_uses_valid_student_id_lookup(self):
        self.assertIn("student__student_id", OrgMemberAdmin.search_fields)
        self.assertNotIn("student_id", OrgMemberAdmin.search_fields)

    def test_member_program_uses_selected_related_data(self):
        admin_instance = OrgMemberAdmin(OrgMember, None)
        with self.assertNumQueries(1):
            member = OrgMember.objects.select_related("student__program").get(pk=self.membership.pk)
            self.assertEqual(admin_instance.get_member_program(member), self.program)


class InitialDataCommandTests(TestCase):
    def test_command_seeds_a_fresh_database(self):
        output = StringIO()
        call_command("create_initial_data", stdout=output)
        self.assertEqual(College.objects.count(), 8)
        self.assertEqual(Program.objects.count(), 10)
        self.assertEqual(Organization.objects.count(), 10)
        self.assertEqual(Student.objects.count(), 50)
        self.assertEqual(OrgMember.objects.count(), 10)
        self.assertIn("created successfully", output.getvalue())


class ProductionSettingsTests(SimpleTestCase):
    manage_py = Path(__file__).resolve().parent.parent / "manage.py"

    def run_check(self, **overrides):
        env = os.environ.copy()
        for name in (
            "DJANGO_SECRET_KEY",
            "DJANGO_EMAIL_BACKEND",
            "DJANGO_EMAIL_HOST",
            "DJANGO_DEFAULT_FROM_EMAIL",
        ):
            env.pop(name, None)
        env.update(
            {
                "DJANGO_DEBUG": "False",
                "DJANGO_ALLOWED_HOSTS": "testserver",
                "DJANGO_EMAIL_HOST": "smtp.example.com",
                "DJANGO_DEFAULT_FROM_EMAIL": "noreply@example.com",
                **overrides,
            }
        )
        return subprocess.run(
            [sys.executable, str(self.manage_py), "check"],
            cwd=self.manage_py.parent,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_production_requires_secret_key(self):
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY must be set", result.stderr)

    def test_production_settings_accept_configured_smtp(self):
        result = self.run_check(DJANGO_SECRET_KEY="test-only-production-secret")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_production_rejects_console_email_backend(self):
        result = self.run_check(
            DJANGO_SECRET_KEY="test-only-production-secret",
            DJANGO_EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("console email backend cannot be used", result.stderr)
