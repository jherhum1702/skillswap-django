import zoneinfo
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Habilidad(models.Model):
    """
    Model for a user skill in SkillSwap

    Represents a skill in SkillSwap.

    Attributes:
        nombre (str): Skill name (max 100 characters, unique)
        estado (bool): Represents if your skill is active or not (max 100 characters, unique)

    Example:
        >>> habilidad = Habilidad.objects.create(
        ...     nombre="Photoshop",
        ...     estado=True
        ...     )
        >>> habilidad.save()
    """
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)


class Usuario(AbstractUser):
    """
    Model for users in SkillSwap

    Represents a registered user in SkillSwap with auth and profile info.

    Attributes:
        nombre (str): Username (max 100 characters)
        alias (str): User alias for search (max 16 characters, unique)
        email (str): User email address (Unique)

    Example:
        >>> usuario = Usuario.objects.create(
        ...     nombre="Paco Tester",
        ...     alias="pacogamer30",
        ...     email="pacotest@gmail.com"
        ...     )
        >>> usuario.save()
    """
    nombre = models.CharField(max_length=100)
    alias = models.CharField(max_length=16, unique=True) # Represents a user alias (e.g. @JohnPork)
    email = models.EmailField(unique=True)
    # is_active - 'Estado' attribute. Python is faster checking for a boolean rather than a string - FROM AbstractUser !!

    def __str__(self):
        """
        Returns the string representation of the user.

        Args:
            self: User instance

        Format: [nombre] (user's name) - e.g., "Paco Tester"

        Returns:
            str: User's full name.

        Example:
            >>> usuario = Usuario.objects.create(
            ...     nombre="Paco Tester",
            ...     alias="pacogamer30",
            ...     email="pacotest@gmail.com"
            ...     )
            >>> usuario.save()
            >>> print(usuario)
        """
        return self.nombre

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['nombre']


def timezone_choices():
    """
    Returns a list of available timezones

    Gives a list of available timezones
    You can see the list of available timezones here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    Returns:
        list: List of available timezones

    Example:
    >>> timezone_choices()
    """
    return [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]


def default_preferencias():
    """
    Returns the default user preferences dicc.

    Gives initial preferences for new user profiles.

    Returns:
        dict: Default preferences for users

   Example:
       >>> default_preferencias()
    """
    return {
        "theme": "light",
        "language": "es",
        # This will be modified in case of adding a new preference.
    }

class Perfil(models.Model):
    """
    Model for a user profile in SkillSwap

    Represents a customizable user profile in SkillSwap.

    Attributes:
        usuario (Usuario): User in SkillSwap
        biografia (str): User bio where he can write anything about him.
        zona_horaria (str): User timezone.
        disponibilidad (str): User availability (e.g. time ranges or anything else)
        preferencias (dict): User preferences (e.g. light/dark mode)

    Example:
        >>> usuario = Usuario.objects.create(
        ...     nombre="Paco Tester",
        ...     alias="pacogamer30",
        ...     email="pacotest@gmail.com"
        ...     )
        >>> usuario.save()
        >>> perfil_usuario = Perfil.objects.create(
        ...     usuario=usuario,
        ...     biografia = "Hi, I'm John, and I'm highly skilled in Adobe Suite. I want to learn about Linux system management."
        ...     zona_horaria = "Africa/Abidjan"
        ...     disponibilidad = "From Monday to Friday, 8.00 - 22.00"
        ...     preferencias = {"theme": "dark", "language": "es"}
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil', related_query_name='perfil')
    biografia = models.CharField(max_length=200, blank=True)
    zona_horaria = models.CharField(max_length=100, choices=timezone_choices(), default='Europe/Madrid')
    disponibilidad = models.TextField()
    preferencias = models.JSONField(default=default_preferencias, blank=True)

    habilidades = models.ManyToManyField(Habilidad, blank=True, related_name='perfil', related_query_name='perfil')


    def clean(self):
        """
        Validates the entire model before saving it.

        This method is used for validation.

        Args:
            self (Perfil): User profile in SkillSwap

        Raises:
            ValidationError: Raises when validation fails:
                - Invalid keys in preferencias JSONField. Keys must match default_preferencias keys)
                - Invalid theme values ("dark" or "light" only).
                - Invalid language values ("es" or "en" only).

        Example:
            >>> usuario = Usuario.objects.create(
            ...     nombre="Paco Tester",
            ...     alias="pacogamer30",
            ...     email="pacotest@gmail.com"
            ...     )
            >>> usuario.save()
            >>> perfil = Perfil.objects.create(
            ...     usuario=usuario,
            ...     preferencias={"theme": "gray"}  # Raises ValidationError
            ... )
            Traceback (most recent call last):
                ...
            ValidationError: The theme must be 'dark' or 'light', not 'gray'
        """

        # Clean Preferencias
        theme_values = ["dark", "light"]
        language_values = ["es", "en"]

        default_preferences = default_preferencias()
        preferences = self.preferencias or {}

        for k, v in preferences.items():
            if k not in default_preferences.keys():
                raise ValidationError(f"The key {k} is not valid.")
            if k == "theme" and v not in theme_values:
                raise ValidationError(f"The theme must be 'dark' or 'light', not '{v}'")
            if k == "language" and v not in language_values:
                raise ValidationError(f"The language must be 'es' or 'en', not '{v}'")

class Publicacion(models.Model):
    """
    Model for a post in SkillSwap

    Represents a post in SkillSwap.

    Attributes:
        tipo (str): Post type (choices in TIPO_CHOICES, max 30 characters, unique).
        descripcion (str): Post description (max 200 characters, unique).
        estado (bool): Represents if your post is active or not (enabled by default).
        fecha_creacion (datetime): Date and time the post was created.
        fecha_modificacion (datetime): Date and time the post was last modified.

    Example:
        >>> usuario = Usuario.objects.create(
        ...     nombre="Paco Tester",
        ...     alias="pacogamer30",
        ...     email="pacotest@gmail.com"
        ...     )
        >>> usuario.save()
        >>> habilidad = Habilidad.objects.create(
        ...     nombre="Photoshop",
        ...     estado=True
        ...     )
        >>> habilidad.save()
        >>> publicacion = Publicacion.objects.create(
        ...     tipo="Ofrezco",
        ...     descripcion="Looking for someone to SkillSwap. I offer Photoshop, and I'm looking for learning English",
        ...     estado=True,
        ...     autor = usuario,
        ...     habilidad=habilidad,
        ...     )
        >>> habilidad.save()
    """
    TIPO_CHOICES = (
        ('OFREZCO', 'Ofrezco'),
        ('BUSCO', 'Busco'),
    )

    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones', related_query_name='publicacion') # It has no-sense if the post remains when the user closes it's account, as you won't be able to contact him.
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE, related_name='publicaciones', related_query_name='publicacion') # It has no-sense if the post remains when the skill is removed, as you won't be able to SkillSwap.

class Acuerdo(models.Model):
    """
    Model for an agreement in SkillSwap

    Represents an agreement in SkillSwap.

    Attributes:
        usuario_a (Usuario): First User
        usuario_b (Usuario): Second User
        semanas (int): Number of weeks of the agreement's duration
        mins_sesion (int): Mins per session of the agreement
        sesiones_por_semana (int): Sessions per week
        estado (str): Agreement's status.(Choices in ESTADO_CHOICES,PROPUESTO by default)
        condiciones (str): Agreement's conditions.
        habilidad_tradea_a (Habilidad): Skill from A user
        habilidad_tradea_b (Habilidad): Skill from B user

    Example:
        >>> usuario_a = Usuario.objects.create(
        ...     nombre="Paco Tester",
        ...     alias="pacogamer30",
        ...     email="pacotest@gmail.com"
        ...     )
        >>> usuario_a.save()
        >>> usuario_b = Usuario.objects.create(
        ...     nombre="Manolita Tester",
        ...     alias="manola33",
        ...     email="manolagamer@outlook.com"
        ...     )
        >>> usuario_b.save()
        >>> habilidad_a = Habilidad.objects.create(
        ...     nombre="Photoshop",
        ...     estado=True
        ...     )
        >>> habilidad_a.save()
        >>> habilidad_b = Habilidad.objects.create(
        ...     nombre="Inglés",
        ...     estado=True
        ...     )
        >>> habilidad_b.save()
        >>> acuerdo = Acuerdo.objects.create(
        ...     usuario_a=usuario_a,
        ...     usuario_b=usuario_b,
        ...     semanas=3,
        ...     mins_sesion=60,
        ...     sesiones_por_semana=7,
        ...     estado='Aceptado',
        ...     condiciones='The users MUST give some exercises at the end of the class.',
        ...     habilidad_tradea_a=habilidad_a,
        ...     habilidad_tradea_b=habilidad_b,
        ...     )
    """

    ESTADO_CHOICES = (
        ('PROPUESTO', 'Propuesto'),
        ('ACEPTADO', 'Aceptado'),
        ('EN CURSO', 'En Curso'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )

    usuario_a = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='acuerdos_a', related_query_name='acuerdo_a') # User won't be able to delete its account unless the trade has been finished.
    usuario_b = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='acuerdos_b', related_query_name='acuerdo_a') # User won't be able to delete its account unless the trade has been finished.
    semanas = models.PositiveIntegerField(default=1) # The user won't be able to use a negative integer.
    mins_sesion = models.PositiveIntegerField(default=60) # The user won't be able to use a negative integer. Default 1 hour
    sesiones_por_semana = models.PositiveIntegerField(default=1) # The user won't be able to use a negative integer. Default 1 session per week.
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=30, default='PROPUESTO') # Default: Proposal pending owner's approval or denial after responding to their post
    condiciones = models.TextField()

    habilidad_tradea_a = models.ForeignKey(Habilidad, on_delete=models.CASCADE, related_name='acuerdos_a', related_query_name='acuerdos_a') # It has no-sense if the post remains when the skill is removed, as you won't offer/search for a Null skill.
    habilidad_tradea_b = models.ForeignKey(Habilidad, on_delete=models.CASCADE, related_name='acuerdos_b', related_query_name='acuerdos_b') # It has no-sense if the post remains when the skill is removed, as you won't offer/search for a Null skill.

    def clean(self):
        """
        Validates the entire model before saving it.

        This method is used for validation.

        Args:
            self (Acuerdo): An agreement in SkillSwap

        Raises:
            ValidationError: Raises when validation fails:
                - User A is the same as User B. Users must be different.
                - Swapped Skills are the same. Skills must be different.

        Example:
            >>> from django.core.exceptions import ValidationError
            >>> usuario_a = Usuario.objects.create(nombre="Paco", alias="paco30", email="paco@test.com")
            >>> usuario_b = Usuario.objects.create(nombre="Ana", alias="ana33", email="ana@test.com")
            >>> acuerdo_mismo_usuario = Acuerdo(usuario_a=usuario_a, usuario_b=usuario_a, semanas=4, mins_sesion=60, sesiones_por_semana=3, condiciones="Test", habilidad_tradea_a=habilidad_a, habilidad_tradea_b=habilidad_b)
            >>> acuerdo_mismo_usuario.clean()
            Traceback (most recent call last):
                ...
            ValidationError: A SkillSwap cannot be created with two equivalent users.

            >>> acuerdo_mismas_habilidades = Acuerdo(usuario_a=usuario_a, usuario_b=usuario_b, semanas=4, mins_sesion=60, sesiones_por_semana=3, condiciones="Test", habilidad_tradea_a=habilidad_a, habilidad_tradea_b=habilidad_a)
            >>> acuerdo_mismas_habilidades.clean()
            Traceback (most recent call last):
                ...
            ValidationError: A SkillSwap cannot be created with two equivalent skills.
        """

        # Clean Habilidades
        if self.habilidad_tradea_a == self.habilidad_tradea_b:
            raise ValidationError('A SkillSwap cannot be created with two equivalent skills.')

        # Clean Usuarios
        if self.usuario_a == self.usuario_b:
            raise ValidationError('A SkillSwap cannot be created with two equivalent users.')

    class Meta:
        db_table = 'acuerdo'
        verbose_name = 'acuerdo'
        verbose_name_plural = 'acuerdos'
        ordering = ['usuario_a']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario_a', 'usuario_b', 'habilidad_tradea_a', 'habilidad_tradea_b'],
                condition=models.Q(estado__in=['PROPUESTO', 'ACEPTADO', 'EN CURSO']),
                name = 'unique_acuerdo_activo'
            )
        ] # Used due to unique_together is deprecated.

def validate_date_today_or_later(value):
    """
    Validates that a date is today or later.

    This function is used as a validator for a DateField to ensure users do not select a past date.

    Args:
        value (datetime.date): The date to validate.

    Raises:
        django.core.exceptions.ValidationError: If the date is earlier than today.

    Example:
        >>> from django.db import models
        >>> from django.core.exceptions import ValidationError
        >>> import datetime
        >>> class Event(models.Model):
        ...     event_date = models.DateField(validators=[validate_date_today_or_later])
        >>> event = Event(event_date=datetime.date.today() + datetime.timedelta(days=1))
        >>> event.full_clean()  # Passes without ValidationError
        >>> past_event = Event(event_date=datetime.date.today() - datetime.timedelta(days=1))
        >>> try:
        ...     past_event.full_clean()
        ... except ValidationError as e:
        ...     print(e)  # Will raise ValidationError: 'The date must be today or later.'
    """
    if value < timezone.now().date():
        raise ValidationError('The date must be today or later.')

class Sesion(models.Model):
    """
    Model for an session in SkillSwap

    Represents a session in SkillSwap, where users teach and learn skills.

    Attributes:
        fecha (datetime.date): Session date
        duracion_real (int): Minutes per session
        resumen (str): Session's summary
        duracion_real (int): Mins per session of the agreement
        asistencia_user_a (bool): Did the user A attend?
        asistencia_user_b (bool): Did the user B attend?
        estado (bool): If the session is active or not
        acuerdo (Acuerdo): The SkillSwap agreement that this session is part of

    Example:
        >>> usuario_a = Usuario.objects.create(nombre="Paco Tester", alias="pacogamer30", email="pacotest@gmail.com")
        >>> usuario_b = Usuario.objects.create(nombre="Manolita Tester", alias="manola33", email="manolagamer@outlook.com")
        >>> habilidad_a = Habilidad.objects.create(nombre="Photoshop", estado=True)
        >>> habilidad_b = Habilidad.objects.create(nombre="Inglés", estado=True)
        >>> acuerdo = Acuerdo.objects.create(
        ...     usuario_a=usuario_a,
        ...     usuario_b=usuario_b,
        ...     semanas=3,
        ...     mins_sesion=60,
        ...     sesiones_por_semana=7,
        ...     estado='ACEPTADO',
        ...     condiciones='The users MUST give some exercises at the end of the class.',
        ...     habilidad_tradea_a=habilidad_a,
        ...     habilidad_tradea_b=habilidad_b
        ... )
        >>> from datetime import date
        >>> sesion = Sesion.objects.create(
        ...     fecha=date.today(),
        ...     duracion_real=60,
        ...     resumen="Introduction to Photoshop basics",
        ...     asistencia_user_a=True,
        ...     asistencia_user_b=True,
        ...     estado=True,
        ...     acuerdo=acuerdo
        ... )
        >>> sesion.fecha
        >>> sesion.resumen
    """

    fecha = models.DateField(validators=[validate_date_today_or_later])
    duracion_real = models.PositiveIntegerField(default=60, validators=[MinValueValidator(60), MaxValueValidator(240)])  # Minutes of actual session duration
    resumen = models.CharField(max_length=200)
    asistencia_user_a = models.BooleanField(default=False)
    asistencia_user_b = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)     # True if Active, otherwise False. Python is faster checking for a boolean rather than a string

    acuerdo = models.ForeignKey(Acuerdo, on_delete=models.CASCADE, related_name='sesiones', related_query_name='sesion')

    def clean(self):
        """
        Validates the entire model before saving it.

        This method is used for validation, ensuring the session can be only created/modified if the
        agreement status is currently ongoing ("En Curso").

        Args:
            self (Sesion): Skill swapping session

        Raises:
            ValidationError: Raises when validation fails:
                - Invalid agreement status ('En Curso' only),

        Example:
        >>> usuario_a = Usuario.objects.create(nombre="Paco Tester", alias="pacogamer30", email="pacotest@gmail.com")
        >>> usuario_b = Usuario.objects.create(nombre="Manolita Tester", alias="manola33", email="manolagamer@outlook.com")
        >>> habilidad_a = Habilidad.objects.create(nombre="Photoshop", estado=True)
        >>> habilidad_b = Habilidad.objects.create(nombre="Inglés", estado=True)
        >>> acuerdo = Acuerdo.objects.create(
        ...     usuario_a=usuario_a,
        ...     usuario_b=usuario_b,
        ...     semanas=3,
        ...     mins_sesion=60,
        ...     sesiones_por_semana=7,
        ...     estado='PROPUESTO',  # Not 'En Curso'
        ...     condiciones='The users MUST give some exercises at the end of the class.',
        ...     habilidad_tradea_a=habilidad_a,
        ...     habilidad_tradea_b=habilidad_b
        ... )
        >>> from datetime import date
        >>> sesion = Sesion(
        ...     fecha=date.today(),
        ...     duracion_real=60,
        ...     resumen="Intro to Photoshop",
        ...     asistencia_user_a=True,
        ...     asistencia_user_b=True,
        ...     estado=True,
        ...     acuerdo=acuerdo
        ... )
        >>> sesion.clean()
        Traceback (most recent call last):
            ...
        ValidationError: The agreement status must be ongoing.
        """

        if self.acuerdo.estado != 'EN CURSO':
            raise ValidationError('The agreement status must be ongoing.')

    class Meta:
        db_table = 'sesion'
        verbose_name = 'sesion'
        verbose_name_plural = 'sesiones'
        ordering = ('fecha',)
