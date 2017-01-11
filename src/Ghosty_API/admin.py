from django.contrib import admin
from reversion.admin import VersionAdmin

from Ghosty_API.models import Customer, Assignment, Task, Work


@admin.register(Customer)
class CustomerAdmin(VersionAdmin):
    pass


@admin.register(Work)
class WorkAdmin(VersionAdmin):
    pass


@admin.register(Task)
class TaskAdmin(VersionAdmin):
    pass


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    pass
