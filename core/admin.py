from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Skill model for SkillSwap platform.

    Represents a teachable skill that users can offer or request.
    Used for matching users in skill exchange system.

    Attributes:
        nombre (str): Skill name (max 50 characters).
        categoria (str): Category for filtering (e.g. "Programming", "Languages").
        nivel (int): Required proficiency level (1-5).
        descripcion (str): Detailed skill description (optional).
        creado_por (Usuario): User who created this skill entry.
        fecha_creacion (datetime): Timestamp when skill was added.

    Example:
        >>> skill = Skill.objects.create(
        ...     nombre="Django Development",
        ...     categoria="Programming",
        ...     nivel=4,
        ...     creado_por=user
        ... )
        >>> skill.descripcion = "Build REST APIs with Django"
        >>> skill.save()
    """
    list_display = ('username','first_name','last_name','email', 'get_grupos','is_active')
    search_fields = ('username','first_name','email')
    list_filter = ('username','first_name','email')
    fieldsets = (
        ('Datos', {
            'fields': ('username', 'email', 'first_name', 'password')
        }),
        ('Permisos', {
            'fields': ('groups',)
        }),
    )
    filter_horizontal = ('groups',)

    class meta:
        """
        Meta configuration for Usuario model.

        Defines display and ordering options for the Django admin panel.

        Attributes:
            model (Usuario): Model associated with this configuration.
            verbose_name (str): Singular display name in admin ('Usuario').
            verbose_name_plural (str): Plural display name in admin ('Usuarios').
            ordering (tuple): Default ordering by username.

        Example:
            >>> Usuario.objects.all()  # Returns users ordered by username
        """
        model = Usuario
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('username',)

    def get_grupos(self, obj):
        """
        Retrieve user groups as a comma-separated string.

        Joins all group names the user belongs to for display in admin panel.

        Args:
            obj (Usuario): User instance to retrieve groups from.

        Returns:
            str: Comma-separated group names (e.g. 'Admin, Editor, Moderador').

        Raises:
            AttributeError: If obj does not have a groups relation.
        """
        return ', '.join([g.name for g in obj.groups.all()])
    get_grupos.short_description = 'groups'


