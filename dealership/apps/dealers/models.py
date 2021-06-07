from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Dealer(models.Model):
    title = models.CharField(
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

    class Meta:
        verbose_name_plural = "Дилер"


class Dealership(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        verbose_name="Дилер",
        related_name="dealership"
    )
    author = models.ForeignKey(
        User,
        related_name="author_dealerships",
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    title = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        verbose_name="Дилерский центр",
        help_text="Максимальная длина 255 символов"
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Расположен",
        blank=True,
        null=True
    )
    profit = models.IntegerField(
        default=0,
        verbose_name='Прибыль'
    )

    class Meta:
        verbose_name_plural = "Диллерские центры"

    def __str__(self):
        return self.title


class Car(models.Model):
    dealership = models.ForeignKey(
        Dealership,
        on_delete=models.CASCADE,
        verbose_name="Дилерский центр",
        related_name="cars"
    )
    author = models.ForeignKey(
        User,
        related_name="author_cars",
        on_delete=models.CASCADE,
        verbose_name="Автор"
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
    author = models.ForeignKey(
        User,
        related_name="author_components",
        on_delete=models.CASCADE,
        verbose_name="Автор"
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
    unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Единица измерения, максимум 20 симоволов'
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
    author = models.ForeignKey(
        User,
        related_name="author_sales",
        on_delete=models.CASCADE,
        verbose_name="Автор"
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
    profit = models.IntegerField(
        verbose_name="Чистая прибыль"
    )
    buyer = models.CharField(
        max_length=100,
        verbose_name="Покупатель",
        help_text="Максимальная длина 100 символов"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер телефона",
        help_text="Максимальная длина 20 символов"
    )

    class Meta:
        verbose_name_plural = "Продажи"
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.brand}  {self.model} - {self.vin}"


class Support(models.Model):
    STATUS = (
        ("PROCESSING", "Принят"),
        ("SHIPPED", "Отгружен"),
    )

    dealership = models.ForeignKey(
        Dealership,
        on_delete=models.CASCADE,
        verbose_name="Дилерский центр",
        related_name='supported'
    )
    author = models.ForeignKey(
        User,
        related_name="author_supported",
        on_delete=models.CASCADE,
        verbose_name="Автор"
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
    discription = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание дефекта"
    )
    shipment = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата отгрузки"
    )
    conclusion = models.TextField(
        blank=True,
        verbose_name="Заключение мастера",
        help_text="Подробное описание выполненных работ"
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Стоимость ремонта",
        default=0
    )
    status = models.CharField(
        choices=STATUS,
        max_length=20,
        verbose_name="Статус"
    )

    class Meta:
        verbose_name_plural = "Ремонт автомобилей"
        ordering = ("-pub_date",)

    def status_verbose(self):
        return dict(Support.STATUS)[self.status]

    def __str__(self):
        return f"{self.brand}  {self.model} - {self.vin}"
