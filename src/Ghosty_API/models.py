import reversion
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.


@reversion.register()
class Customer(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    address = models.CharField(verbose_name="Dirección", max_length=50)
    city = models.CharField(verbose_name="Ciudad", max_length=50)
    postal_code = models.IntegerField(verbose_name="Código postal", blank=True, null=True)
    phone_number = models.IntegerField(verbose_name="Teléfono")
    nif_cif = models.CharField(max_length=50, verbose_name="NIF/CIF", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


@reversion.register()
class Task(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    details = models.CharField(max_length=100, blank=True, null=True, verbose_name="Detalles")

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


@reversion.register()
class Work(models.Model):
    OPEN = 'AB'
    CLOSED = 'CE'
    STATES = (
        (OPEN, 'Abierto'),
        (CLOSED, 'Cerrado'),
    )
    name = models.CharField(verbose_name="Nombre", max_length=50, unique=True)
    customer = models.ForeignKey(Customer, verbose_name="Cliente", blank=True, null=True)
    tasks = models.ManyToManyField(Task, verbose_name="Tareas", through='Ghosty_API.Assignment')
    status = models.CharField(verbose_name="Estado", max_length=10, choices=STATES, default=OPEN)
    creation_date = models.DateField(verbose_name="Fecha de creación", default=timezone.now)
    finish_date = models.DateField(verbose_name="Fecha de finalización", blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"
        ordering = ['-creation_date', 'name', ]


@reversion.register()
class Assignment(models.Model):
    CANCELLED, PENDING, WIP, DONE = range(0, 4)

    STATES = (
        (CANCELLED, 'Cancelado'),
        (PENDING, 'Pendiente'),
        (WIP, 'En proceso'),
        (DONE, 'Hecho'),
    )
    task = models.ForeignKey(Task, verbose_name="Tarea")
    work = models.ForeignKey(Work, verbose_name="Trabajo")
    done_date = models.DateField(verbose_name="Fecha de realización", blank=True, null=True, default=None)
    status = models.IntegerField(verbose_name="Estado", choices=STATES, default=PENDING)
    responsible = models.ForeignKey(User, verbose_name="Responsable")

    @property
    def status_str(self):
        return self.ESTADOS[self.status][1]

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"


def complete_task(sender, instance, **kwargs):
    if instance.status is Assignment.DONE and instance.done_date is None:
        instance.done_date = timezone.now()
        instance.save()


def close_work(sender, instance, **kwargs):
    query = sender.objects.filter(work=instance.work)
    work = Work.objects.get(nombre=instance.work.name)
    is_closed = False
    for q in query:
        if q.status != Assignment.DONE:
            is_closed = False
            break
        else:
            is_closed = True

    if is_closed:
        work.status = Work.CLOSED
        work.finish_date = timezone.now()
        work.save()


post_save.connect(complete_task, sender=Assignment, dispatch_uid="update_complete_task")
post_save.connect(close_work, sender=Assignment, dispatch_uid="update_close_work")
