from Ghosty_API.models import Deceased, Task, Work, Move, Morgue, Church, Cemetery, Florist, Declarant, \
    SonOrBeneficiary, ChurchPlace, MorgueBusiness, FloristWork, FlowerProvider, Taxi, Obituary, MiniTombstone, Chair, \
    Tap, Tombstone
from django.contrib import admin
from reversion.admin import VersionAdmin


@admin.register(Deceased)
class DeceasedAdmin(VersionAdmin):
    icon = '<i class="material-icons">airline_seat_individual_suite</i>'
    list_display = ("name", "nif", "city", "death_date")


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
    list_display = ("exit_place_1", "exit_time_1", "arrival_place_1", "arrival_time_1")


@admin.register(Morgue)
class MorgueAdmin(VersionAdmin):
    list_display = ("business", "arrival_date", "exit_date")
    icon = '<i class="material-icons">location_city</i>'


@admin.register(MorgueBusiness)
class MorgueBusinessAdmin(VersionAdmin):
    list_display = ("name", "town")
    icon = '<i class="material-icons">location_city</i>'


@admin.register(Church)
class ChurchAdmin(VersionAdmin):
    list_display = ("church_place", "undertaker", "time")
    icon = '<i class="material-icons">local_hospital</i>'


@admin.register(ChurchPlace)
class ChurchPlaceAdmin(VersionAdmin):
    list_display = ("name", "town")
    icon = '<i class="material-icons">local_hospital</i>'


@admin.register(Cemetery)
class CemeteryAdmin(VersionAdmin):
    list_display = ("town", "burial_date")
    icon = '<i class="material-icons">account_balance</i>'


@admin.register(Florist)
class FloristAdmin(VersionAdmin):
    list_display = ("order_name", "order_nif", "order_telephone")
    icon = '<i class="material-icons">local_florist</i>'


@admin.register(FloristWork)
class FloristWorkAdmin(VersionAdmin):
    list_display = ("flower_provider", "florist", "florist_2")
    icon = '<i class="material-icons">local_florist</i>'


@admin.register(FlowerProvider)
class FlowerProviderAdmin(VersionAdmin):
    list_display = ("name", "town")
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
    list_display = ("name", "nif", "town", "company", "phone_contact")
    icon = '<i class="material-icons">create</i>'


@admin.register(SonOrBeneficiary)
class SonOrBeneficiaryAdmin(VersionAdmin):
    list_display = ("name", "relationship", "phone")
    icon = '<i class="material-icons">favorite</i>'
