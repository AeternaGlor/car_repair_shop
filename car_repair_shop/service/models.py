from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AbstractModel(models.Model):
    text = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
    )
    is_shown = models.BooleanField(
        default=True,
        verbose_name="Показывать услуги на главной странице",
    )

    class Meta:
        abstract = True


class TimeSlot(models.Model):
    start_time = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Время начала оказания услуги",
    )

    class Meta:
        verbose_name = "временной слот"
        verbose_name_plural = "Временные слоты"
        ordering = ("start_time",)

    def __str__(self):
        return self.start_time.strftime('%d-%m-%Y %H:%M')


class Master(AbstractModel):
    name = models.CharField(max_length=256, verbose_name="ФИО")
    photo = models.ImageField(
        upload_to="master_images",
        blank=True,
        verbose_name="Фото мастера",
    )
    slots = models.ManyToManyField(
        TimeSlot,
        verbose_name="Временной слот",
        related_name="masters",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "мастер"
        verbose_name_plural = "Мастера"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Service(AbstractModel):
    name = models.CharField(max_length=256, verbose_name="Название")
    price = models.IntegerField(
        verbose_name="Цена",
        default=0
    )
    duration = models.DurationField(verbose_name="Продолжительность оказания")
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name="services",
    )

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "Услуги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Box(models.Model):
    slots = models.ManyToManyField(
        TimeSlot,
        verbose_name="Временной слот",
        related_name="boxes",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Бокс для машины"
        verbose_name_plural = "Боксы для машины"
        ordering = ("id",)

    def __str__(self):
        return f'Бокс № {self.id}'


class Customer(models.Model):
    name = models.CharField(max_length=256, verbose_name="ФИО")
    discount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Процент скидки",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Order(models.Model):
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        verbose_name="Временной слот",
        related_name="orders",
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        verbose_name="Бокс для машины",
        related_name="orders",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="Услуга",
        related_name="orders",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="orders",
        null=True
    )

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"Запись № {self.id}"
