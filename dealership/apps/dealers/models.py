from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()

class Dealer(models.Model):
    title =  models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        verbose_name="Название дилера",
        help_text="Максимальная длина 255 символов"
    )
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Руководитель'
    )


class Dealership(models.Model):
    title = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        verbose_name="Дилерский центр",
        help_text="Максимальная длина 255 символов"
    )
    profit = models.IntegerField(
        default=0,
        verbose_name='Прибыль'
    )


class Car(models.Model):
    dealership = models.ForeignKey(
        Dealership,
        on_delete=models.CASCADE,
        verbose_name="Дилерский центр",
        related_name="cars"
    )
    brand = models.CharField(
        max_length=100,
        verbose_name="Марка",
        help_text="Максимальная длина 100 символов"
    )
    model = models.CharField(
        max_length=100,
        verbose_name="Модель автомобиля",
        help_text="Максимальная длина 100 символов"
    )
    color = models.CharField(
        max_length=25,
        verbose_name="Цвет автомобиля",
        help_text="Максимальная длина 25 символов"
    )
    vin = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name="VIN номер",
        help_text="Поле уникальное, максимальная длина 100 символов"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата поступления",
        help_text="Дата поступления заполняется автоматически"
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Стоимость без наценки"
    )
    markup = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Наценка в %",
        validators=[MinValueValidator(0)]
    )
    cost = models.IntegerField(
        blank=True,
        verbose_name="Цена"
    )

    def __str__(self):
        return f"{self.brand}  {self.model}"

    def save(self, *args, **kwargs):
        self.cost = int(self.price + self.price * (self.markup / 100))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = "Атомобили"


class Component(models.Model):
    dealership = models.ForeignKey(
        Dealership,
        on_delete=models.CASCADE,
        verbose_name="Дилерский центр",
        related_name='components'
    )
    title = models.CharField(
        db_index=True,
        max_length=250,
        verbose_name="Название",
        help_text="Название детали, максимальная длина 250 символов"
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Количество",
        help_text="Не может быть отрицательным"
    )

    class Meta:
        verbose_name_plural = "Детали"

    def __str__(self):
        return self.title


class Sale(models.Model):
    dealership = models.ForeignKey(
        Dealership,
        on_delete=models.CASCADE,
        verbose_name="Дилерский центр",
        related_name='sales'
    )
    brand = models.CharField(
        max_length=100,
        verbose_name="Марка",
        help_text="Максимальная длина 100 символов"
    )
    model = models.CharField(
        max_length=100,
        verbose_name="Модель автомобиля",
        help_text="Максимальная длина 100 символов"
    )
    color = models.CharField(
        max_length=25,
        verbose_name="Цвет автомобиля",
        help_text="Максимальная длина 25 символов"
    )
    vin = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name="VIN номер",
        help_text="Поле уникальное, максимальная длина 100 символов"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата продажи",
        help_text="Дата продажи заполняется автоматически"
    )
    price = models.IntegerField(
        verbose_name="Цена захода"
    )
    profit = models.IntegerField(
        verbose_name="Чистая прибыль"
    )

    class Meta:
        verbose_name_plural = "Продажи"

    def __str__(self):
        return f"{self.brand}  {self.model} - {self.vin}"
