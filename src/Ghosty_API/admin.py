from Ghosty_API.models import Deceased, Task, Work, Move, Morgue, Church, Cemetery, Florist, Declarant, \
    SonOrBeneficiary, ChurchPlace, MorgueBusiness, FloristWork, FlowerProvider, Taxi, Obituary, MiniTombstone, Chair, \
    Tap, Tombstone
from django.contrib import admin
from reversion.admin import VersionAdmin


@admin.register(Deceased)
class DeceasedAdmin(VersionAdmin):
    icon = '<i class="material-icons">airline_seat_individual_suite</i>'


@admin.register(Work)
class WorkAdmin(VersionAdmin):
    icon = '<i class="material-icons">work</i>'
    raw_id_fields = ("employed",)
    list_display = ("a24h", "status", "deceased", "employed", "creation_date", "finish_date")


@admin.register(Task)
class TaskAdmin(VersionAdmin):
    icon = '<i class="material-icons">assignment</i>'
    list_display = ("name", "shorten_attachment", "name_location")


@admin.register(Move)
class MoveAdmin(VersionAdmin):
    icon = '<i class="material-icons">directions_car</i>'


@admin.register(Morgue)
class MorgueAdmin(VersionAdmin):
    icon = '<i class="material-icons">location_city</i>'


@admin.register(MorgueBusiness)
class MorgueBusinessAdmin(VersionAdmin):
    icon = '<i class="material-icons">location_city</i>'


@admin.register(Church)
class ChurchAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_hospital</i>'


@admin.register(ChurchPlace)
class ChurchPlaceAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_hospital</i>'


@admin.register(Cemetery)
class CemeteryAdmin(VersionAdmin):
    icon = '<i class="material-icons">account_balance</i>'


@admin.register(Florist)
class FloristAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_florist</i>'


@admin.register(FloristWork)
class FloristWorkAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_florist</i>'


@admin.register(FlowerProvider)
class FlowerProviderAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_florist</i>'


@admin.register(Taxi)
class TaxiAdmin(VersionAdmin):
    icon = '<i class="material-icons">local_taxi</i>'


@admin.register(Obituary)
class ObituaryAdmin(VersionAdmin):
    icon = '<i class="material-icons">view_headline</i>'


@admin.register(MiniTombstone)
class MiniTombstoneAdmin(VersionAdmin):
    icon = '<i class="material-icons">format_list_bulleted</i>'


@admin.register(Chair)
class ChairAdmin(VersionAdmin):
    icon = '<i class="material-icons">event_seat</i>'


@admin.register(Tap)
class TapAdmin(VersionAdmin):
    icon = '<i class="material-icons">format_list_bulleted</i>'


@admin.register(Tombstone)
class TombstoneAdmin(VersionAdmin):
    icon = '<i class="material-icons">format_list_bulleted</i>'


@admin.register(Declarant)
class DeclarantAdmin(VersionAdmin):
    icon = '<i class="material-icons">create</i>'


@admin.register(SonOrBeneficiary)
class SonOrBeneficiaryAdmin(VersionAdmin):
    icon = '<i class="material-icons">favorite</i>'
