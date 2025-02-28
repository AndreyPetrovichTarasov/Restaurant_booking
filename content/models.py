from django.db import models


class HomePageContent(models.Model):
    about_text = models.TextField(verbose_name="Текст о ресторане")
    about_image = models.ImageField(upload_to="home_images/", verbose_name="Изображение о ресторане", blank=True,
                                    null=True)

    menu_title = models.CharField(max_length=255, verbose_name="Меню")
    menu_image = models.ImageField(upload_to="home_images/", verbose_name="Меню", blank=True,
                                   null=True)
    menu_desc = models.TextField(verbose_name="Описание меню")

    events_title = models.CharField(max_length=255, verbose_name="Банкеты и мероприятия")
    events_desc = models.TextField(verbose_name="Описание Банкеты и мероприятия")
    events_image = models.ImageField(upload_to="home_images/", verbose_name="Банкеты и мероприятия", blank=True,
                                     null=True)

    live_music_title = models.CharField(max_length=255, verbose_name="Живая музыка")
    live_music_desc = models.TextField(verbose_name="Описание Живая музыка")
    live_music_image = models.ImageField(upload_to="home_images/", verbose_name="Живая музыка", blank=True,
                                         null=True)

    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.CharField(max_length=255, verbose_name="График работы")
    scheme_image = models.ImageField(upload_to="home_images/", verbose_name="Схема проезда", blank=True,
                                     null=True)

    def __str__(self):
        return "Контент главной страницы"
