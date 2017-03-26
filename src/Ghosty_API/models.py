from os.path import basename

import geocoder
import reversion
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.html import format_html
from geoposition.fields import GeopositionField


# Create your models here.


@reversion.register()
class Deceased(models.Model):
    SINGLE = 'Soltero'
    MARRIED = 'Casado'
    DIVORCED = 'Divorciado',
    WIDOWER = 'Viudo'
    CIVIL_STATES = (
        (SINGLE, 'Soltero'),
        (MARRIED, 'Casado'),
        (DIVORCED, 'Divorciado'),
        (WIDOWER, 'Viudo'),
    )
    name = models.CharField(verbose_name="Nombre", max_length=50)
    nif = models.CharField(verbose_name="NIF", blank=True, null=True, max_length=50, )
    birthday = models.DateField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    birthplace = models.CharField(verbose_name="Lugar de nacimiento", blank="True", null=True, max_length=50)
    father = models.CharField(verbose_name="Madre", blank="True", null=True, max_length=50)
    mother = models.CharField(verbose_name="Padre", blank="True", null=True, max_length=50)
    civil_state = models.CharField(verbose_name="Estado civil", blank=True, null=True, choices=CIVIL_STATES,
                                   max_length=50)
    number_of_sons = models.IntegerField(verbose_name="Número de hijos", null=True, blank=True)
    sons = models.TextField(verbose_name="Nombre de los hijos", null=True, blank=True)
    address = models.CharField(verbose_name="Domicilio último", max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name="Población", max_length=50, null=True, blank=True)

    # fallecimiento
    death_date = models.DateField(verbose_name="Fecha del fallecimiento", blank=True, null=True)
    death_address = models.CharField(verbose_name="Dirección del fallecimiento", blank=True, null=True, max_length=50)
    death_city = models.CharField(verbose_name="Población del fallecimiento", blank=True, null=True, max_length=50)
    doctor = models.CharField(verbose_name="Médico D.", blank=True, null=True, max_length=50)
    collegiate_number = models.CharField(verbose_name="Colegiado Nº", blank=True, null=True, max_length=50)
    judged_by = models.CharField(verbose_name="Juzgado de", blank=True, null=True, max_length=50)
    medical_institute = models.CharField(verbose_name="Instituto de medicina legal", blank=True, null=True,
                                         max_length=50)
    illness = models.BooleanField(verbose_name="Enfermedad", default=False)
    judicial = models.BooleanField(verbose_name="Judicial", default=False)

    def __str__(self):
        return str(self.name) + " " + str(self.nif) + " " + str(self.death_date)

    class Meta:
        verbose_name = "Fallecido"
        verbose_name_plural = "Fallecidos"


@reversion.register()
class Task(models.Model):
    CANCELLED = 'Cancelado'
    NOT_ASSIGNED = 'Sin asignar'
    PENDING = 'Pendiente'
    WIP = 'En progreso'
    DONE = 'Hecho'

    STATES = (
        (CANCELLED, 'Cancelado'),
        (NOT_ASSIGNED, 'Sin asignar'),
        (PENDING, 'Pendiente'),
        (WIP, 'En proceso'),
        (DONE, 'Hecho'),
    )
    name = models.CharField(verbose_name="Nombre", max_length=50, blank=True, null=True)
    details = models.CharField(verbose_name="Detalles", blank=True, null=True, max_length=100)
    location = GeopositionField(verbose_name="Localización", blank=True, null=True)
    attachment = models.FileField(verbose_name="Adjunto", upload_to='/media/uploads/%Y/%m/%d/', blank=True, null=True)
    done_date = models.DateField(verbose_name="Fecha de realización", blank=True, null=True)
    status = models.CharField(verbose_name="Estado", choices=STATES, max_length=20, default=NOT_ASSIGNED)
    responsible = models.ForeignKey(User, verbose_name="Responsable", blank=True, null=True)

    def shorten_attachment(self):
        if self.attachment.name is not None:
            return format_html(
                '<a href={}><i class ="material-icons">link</i ></a> <span>{}</span>',
                self.attachment.name,
                '{:.20}'.format(basename(self.attachment.name)),
            )
        else:
            return "-"

    shorten_attachment.short_description = "Adjunto"

    def name_location(self):
        if self.location is not None:
            return format_html(
                '<span>{}</span>',
                geocoder.google([self.location.latitude, self.location.longitude], method='reverse').city,
            )
        else:
            return "-"

    name_location.short_description = "Localización"

    def __str__(self):
        return str(self.name) + " a cargo de " + str(self.responsible)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


@reversion.register()
class Move(Task):
    exit_place_1 = models.CharField(verbose_name="Lugar de salida", max_length=50)
    exit_time_1 = models.DateField(verbose_name="Fecha de salida", blank=True, null=True)
    arrival_place_1 = models.CharField(verbose_name="Lugar de llegada", max_length=50)
    arrival_time_1 = models.DateField(verbose_name="Fecha de llegada", blank=True, null=True)
    exit_place_2 = models.CharField(verbose_name="Lugar de salida-2", max_length=50, blank=True, null=True)
    exit_time_2 = models.DateField(verbose_name="Fecha de salida-2", blank=True, null=True)
    arrival_place_2 = models.CharField(verbose_name="Lugar de llegada-2", max_length=50, blank=True, null=True)
    arrival_time_2 = models.DateField(verbose_name="Fecha de llegada-2", blank=True, null=True)

    def __str__(self):
        return "Traslados con salida el " + str(self.exit_time_1) + " desde "
        str(self.exit_place_1) + " a " + str(self.arrival_place_1)

    class Meta:
        verbose_name = "Traslado"
        verbose_name_plural = "Traslados"


@reversion.register()
class MorgueBusiness(models.Model):
    name = models.CharField(verbose_name="Nombre empresa", max_length=20, blank=True, null=True)
    town = models.CharField(verbose_name="Población", max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.name) + " de " + str(self.town)

    class Meta:
        verbose_name = "Empresa Tanatorio"
        verbose_name_plural = "Empresas Tanatorio"


@reversion.register()
class Morgue(Task):
    business = models.ForeignKey(MorgueBusiness, verbose_name="Empresa", blank=True, null=True)
    arrival_date = models.DateField(verbose_name="Fecha Entrada", blank=True, null=True)
    exit_date = models.DateField(verbose_name="Fecha Salida", blank=True, null=True)

    def __str__(self):
        return str(self.business) + " " + str(self.arrival_date)

    class Meta:
        verbose_name = "Tarea Tanatorio"
        verbose_name_plural = "Tareas Tanatorio"


@reversion.register()
class ChurchPlace(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=40, null=True, blank=True)
    town = models.CharField(verbose_name="Población", max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name) + " de " + str(self.town)

    class Meta:
        verbose_name = "Parroquia"
        verbose_name_plural = "Parroquias"


@reversion.register()
class Church(Task):
    church_place = models.ForeignKey(ChurchPlace, verbose_name="Iglesia", blank=True, null=True)
    undertaker = models.CharField(verbose_name="Funeraria", blank=True, null=True, max_length=20)
    time = models.DateTimeField(verbose_name="Fecha y hora", blank=True, null=True)

    def __str__(self):
        return str(self.undertaker) + " " + str(self.church_place) + " " + str(self.time)

    class Meta:
        verbose_name = "Tarea Parroquia"
        verbose_name_plural = "Tareas Parroquia"


@reversion.register()
class Cemetery(Task):
    CREMACION, INHUMACION = range(0, 2)
    ALQUILER, PERPETUIDAD = range(0, 2)
    REDUCCION, TRASLADO = range(0, 2)
    APERTURA, NUEVO_FAMILIA, NUEVO_CIA = range(0, 3)
    PRIMERA, SEGUNDA, TERCERA = range(0, 3)

    TYPES = ((CREMACION, "Cremación"), (INHUMACION, "Inhumación"))
    NICHES = ((APERTURA, "Apertura"), (NUEVO_FAMILIA, "Nuevo Familia"), (NUEVO_CIA, "Nuevo CIA"))
    TITLES = ((ALQUILER, "Alquiler"), (PERPETUIDAD, "Perpetuidad"))
    BURIALS = ((PRIMERA, "1ª"), (SEGUNDA, "2ª"), (TERCERA, "3ª"))
    RESTS = ((REDUCCION, "Reducción"), (TRASLADO, "Traslado"))

    town = models.CharField(verbose_name="Población", max_length=20, blank=True, null=True)
    burial_date = models.DateField(verbose_name="Fecha Inhumación", blank=True, null=True)
    type = models.IntegerField(verbose_name="Tipo", choices=TYPES,
                               default=0)
    niche = models.IntegerField(verbose_name="Nicho", choices=NICHES, default=0)
    title = models.IntegerField(verbose_name="Título", choices=TITLES,
                                default=0)
    burial = models.IntegerField(verbose_name="Inhumación", choices=BURIALS,
                                 default=0)
    rest = models.IntegerField(verbose_name="Restos", choices=RESTS,
                               default=0)

    def __str__(self):
        return str(self.town) + " " + str(self.burial_date)

    class Meta:
        verbose_name = "Cementerio/\nCrematorio"
        verbose_name_plural = "Cementerios/\nCrematorios"


@reversion.register()
class Florist(Task):
    company = models.BooleanField(verbose_name="Compañía", default=False)
    family = models.BooleanField(verbose_name="Familia", default=False)
    wreath = models.BooleanField(verbose_name="Corona", default=False)
    bouquet = models.BooleanField(verbose_name="Ramo", default=False)

    dedicatory = models.TextField(verbose_name="Dedicatoria", blank=True, null=True)
    order_name = models.CharField(verbose_name="Nombre pedido", max_length=40, blank=True, null=True)
    order_nif = models.CharField(verbose_name="NIF pedido", max_length=10, blank=True, null=True)
    order_telephone = models.IntegerField(verbose_name="Teléfono pedido", blank=True, null=True)

    def __str__(self):
        return str(self.order_name) + " " + str(self.order_nif)

    class Meta:
        verbose_name = "Tarea Floristeria"
        verbose_name_plural = "Tareas Floristería"


@reversion.register()
class FlowerProvider(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=20, blank=True, null=True)
    town = models.CharField(verbose_name="Población", max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.name) + " " + str(self.town)

    class Meta:
        verbose_name = "Proveedor de flores"
        verbose_name_plural = "Proveedores de flores"


@reversion.register()
class FloristWork(models.Model):
    flower_provider = models.ForeignKey(FlowerProvider, verbose_name="Proveedor", blank=True, null=True)
    florist = models.OneToOneField(Florist, verbose_name="Pedido 1", blank=True, null=True)
    florist_2 = models.OneToOneField(Florist, related_name='pedido_2', verbose_name="Pedido 2", blank=True, null=True)
    florist_3 = models.OneToOneField(Florist, related_name='pedido_3', verbose_name="Pedido 3", blank=True, null=True)
    florist_4 = models.OneToOneField(Florist, related_name='pedido_4', verbose_name="Pedido 4", blank=True, null=True)
    florist_5 = models.OneToOneField(Florist, related_name='pedido_5', verbose_name="Pedido 5", blank=True, null=True)
    florist_6 = models.OneToOneField(Florist, related_name='pedido_6', verbose_name="Pedido 6", blank=True, null=True)

    def __str__(self):
        return str(self.flower_provider) + " " + str(self.florist) + " " + str(self.florist_2) + " " + str(
            self.florist_3)

    class Meta:
        verbose_name = "Trabajo \nde floristería"
        verbose_name_plural = "Trabajos \nde floristería"


@reversion.register()
class Taxi(Task):
    def __str__(self):
        return "Taxi "

    class Meta:
        verbose_name = "Taxi"


@reversion.register()
class Obituary(Task):
    def __str__(self):
        return "Esquela "

    class Meta:
        verbose_name = "Esquela"


@reversion.register()
class MiniTombstone(Task):
    def __str__(self):
        return "Minilápida "

    class Meta:
        verbose_name = "Minilápida"


@reversion.register()
class Chair(Task):
    def __str__(self):
        return "Silla "

    class Meta:
        verbose_name = "Silla"


@reversion.register()
class Tap(Task):
    def __str__(self):
        return "Tapa frigorífica "

    class Meta:
        verbose_name = "Tapa frigorífica"
        verbose_name_plural = "Tapas frigoríficas"


@reversion.register()
class Tombstone(Task):
    def __str__(self):
        return "Lápida "

    class Meta:
        verbose_name = "Lápida"


@reversion.register()
class Declarant(models.Model):
    name = models.CharField(verbose_name="D./Dª", max_length=40, blank=True, null=True)
    nif = models.CharField(verbose_name="N.I.F", max_length=10, blank=True, null=True)
    relationship = models.CharField(verbose_name="Parentesco", max_length=10, blank=True, null=True)
    address = models.CharField(verbose_name="Domicilio", max_length=40, blank=True, null=True)
    town = models.CharField(verbose_name="Población", max_length=30, blank=True, null=True)
    phone = models.IntegerField(verbose_name="Teléfonos", blank=True, null=True)

    company = models.CharField(verbose_name="Compañía", max_length=30, blank=True, null=True)
    agencia = models.CharField(verbose_name="Agencia", max_length=30, blank=True, null=True)
    policy_number = models.CharField(verbose_name="Nº Póliza", max_length=30, blank=True, null=True)
    phone_contact = models.CharField(verbose_name="Teléfono/Contacto", max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.name) + " " + str(self.NIF) + " " + str(self.relationship)

    class Meta:
        verbose_name = "Contratante declarante"
        verbose_name_plural = "Contratantes declarantes"


@reversion.register()
class SonOrBeneficiary(models.Model):
    relationship = models.CharField(verbose_name="Parentesco", max_length=10, blank=True, null=True)
    name = models.CharField(verbose_name="D./Dª", max_length=40, blank=True, null=True)
    address = models.CharField(verbose_name="Domicilio", max_length=40, blank=True, null=True)
    phone = models.CharField(verbose_name="Teléfono", max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.relationship) + " " + str(self.name) + " " + str(self.phone)

    class Meta:
        verbose_name = "Hijos y beneficiarios"
        verbose_name_plural = "Hijos y beneficiarios"


@reversion.register()
class Work(models.Model):
    OPEN = 'Abierto'
    CLOSED = 'Cerrado'
    FINISHED = 'Terminado'
    STATES = (
        (OPEN, 'Abierto'),
        (FINISHED, 'Terminado'),
        (CLOSED, 'Cerrado'),
    )
    a24h = models.CharField(verbose_name="A24H", max_length=50, unique=True, default=timezone.now())
    employed = models.ForeignKey(User, verbose_name="Empleado", blank=True, null=True)
    deceased = models.OneToOneField(Deceased, verbose_name="Fallecido", blank=True, null=True)
    move = models.OneToOneField(Move, verbose_name="Traslados", blank=True, null=True)
    morgue = models.OneToOneField(Morgue, verbose_name="Tanatorio", blank=True, null=True)
    church = models.OneToOneField(Church, verbose_name="Parroquia", blank=True, null=True)
    cemetery = models.OneToOneField(Cemetery, verbose_name="Cementerio/Crematorio", blank=True, null=True)
    florist_work = models.OneToOneField(FloristWork, verbose_name="Floristería", blank=True, null=True)

    sons_and_beneficiaries = models.ManyToManyField(SonOrBeneficiary, verbose_name="Hijos y beneficiarios",
                                                    blank=True)

    taxi = models.OneToOneField(Taxi, verbose_name="Taxi", blank=True, null=True)
    obituary = models.OneToOneField(Obituary, verbose_name="Esquelas", blank=True, null=True)
    mini_tombstone = models.OneToOneField(MiniTombstone, verbose_name="Minilápida", blank=True, null=True)
    chair = models.OneToOneField(Chair, verbose_name="Sillas", blank=True, null=True)
    tap = models.OneToOneField(Tap, verbose_name="Tapa frigorífica", blank=True, null=True)
    tombstone = models.OneToOneField(Tombstone, verbose_name="Lápida", blank=True, null=True)

    declarant = models.ForeignKey(Declarant, verbose_name="Contratante declarante", blank=True, null=True)

    status = models.CharField(verbose_name="Estado", max_length=10, choices=STATES, default=OPEN)
    creation_date = models.DateField(verbose_name="Fecha de creación", default=timezone.now)
    finish_date = models.DateField(verbose_name="Fecha de finalización", blank=True, null=True)
    comment = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    def __str__(self):
        return str(self.a24h) + " " + str(self.deceased) + " " + str(self.creation_date)

    class Meta:
        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"
        ordering = ['-creation_date', 'a24h', ]


def complete_task(sender, instance, **kwargs):
    if instance.status is Task.DONE:
        instance.done_date = timezone.now()
        instance.save()


# def finish_work(sender, instance, **kwargs):
#     query = sender.objects.filter(work=instance.work)
#     work = Work.objects.get(a24h=instance.work.a24h)
#     is_closed = False
#     for q in query:
#         if q.status != Task.DONE:
#             is_closed = False
#             break
#         else:
#             is_closed = True
#
#     if is_closed:
#         work.status = Work.FINISHED
#         work.finish_date = timezone.now()
#         work.save()


def assign_task(sender, instance, **kwargs):
    if instance.responsible is not None and instance.status is Task.NOT_ASSIGNED or None:
        instance.status = Task.WIP
        instance.save()
    else:
        if instance.responsible is None and instance.status is not Task.NOT_ASSIGNED:
            instance.status = Task.NOT_ASSIGNED
            instance.save()


post_save.connect(complete_task, sender=Task, dispatch_uid="update_complete_task")
# post_save.connect(finish_work, sender=Task, dispatch_uid="update_finished_work")
post_save.connect(assign_task, sender=Task, dispatch_uid="update_assigned_task")
