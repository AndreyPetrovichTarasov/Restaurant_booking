from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Переопределение менеджера создания пользователей
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Определение модели пользователя
    """

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} ({self.email})"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["email"]
        permissions = [("can_block_user", "Can block user")]


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user} ({self.rating}★)"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
