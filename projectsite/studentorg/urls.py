from django.urls import path

from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("organizations/", views.OrganizationList.as_view(), name="organization-list"),
    path("organizations/add/", views.OrganizationCreateView.as_view(), name="organization-add"),
    path("organizations/<int:pk>/edit/", views.OrganizationUpdateView.as_view(), name="organization-update"),
    path("organizations/<int:pk>/delete/", views.OrganizationDeleteView.as_view(), name="organization-delete"),
    path("programs/", views.ProgramList.as_view(), name="program-list"),
    path("programs/add/", views.ProgramCreateView.as_view(), name="program-add"),
    path("programs/<int:pk>/edit/", views.ProgramUpdateView.as_view(), name="program-update"),
    path("programs/<int:pk>/delete/", views.ProgramDeleteView.as_view(), name="program-delete"),
    path("colleges/", views.CollegeList.as_view(), name="college-list"),
    path("colleges/add/", views.CollegeCreateView.as_view(), name="college-add"),
    path("colleges/<int:pk>/edit/", views.CollegeUpdateView.as_view(), name="college-update"),
    path("colleges/<int:pk>/delete/", views.CollegeDeleteView.as_view(), name="college-delete"),
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/add/", views.StudentCreateView.as_view(), name="student-add"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student-update"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student-delete"),
    path("members/", views.OrgMemberList.as_view(), name="orgmember-list"),
    path("members/add/", views.OrgMemberCreateView.as_view(), name="orgmember-add"),
    path("members/<int:pk>/edit/", views.OrgMemberUpdateView.as_view(), name="orgmember-update"),
    path("members/<int:pk>/delete/", views.OrgMemberDeleteView.as_view(), name="orgmember-delete"),
]
