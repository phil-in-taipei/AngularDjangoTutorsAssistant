from django.contrib.admin import AdminSite


class StaffAdminSite(AdminSite):
    site_header = "David's English Center Staff Admin"
    site_title = "DEC Staff Admin"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff


staff_admin_site = StaffAdminSite(name='staff_admin')
