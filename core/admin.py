from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html
from django.urls import *
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.




def banear_usuarios(modeladmin, request, queryset):
    queryset.update(is_active=False)
banear_usuarios.short_description = "🚫 Banear usuarios seleccionados"

def desbanear_usuarios(modeladmin, request, queryset):
    queryset.update(is_active=True)
desbanear_usuarios.short_description = "✅ Desbanear usuarios seleccionados"

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
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_grupos', 'estado_baneo', 'boton_banear')
    search_fields = ('username', 'first_name', 'email')
    list_filter = ('username', 'first_name', 'email')
    actions = [banear_usuarios, desbanear_usuarios]
    fieldsets = (
        ('Datos', {
            'fields': ('username', 'email', 'first_name', 'password', 'is_active')
        }),
        ('Permisos', {
            'fields': ('groups',)
        }),
    )
    filter_horizontal = ('groups',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('banear/<int:usuario_id>/', self.admin_site.admin_view(self.banear_view), name='banear_usuario'),
            path('desbanear/<int:usuario_id>/', self.admin_site.admin_view(self.desbanear_view),
                 name='desbanear_usuario'),
        ]
        return custom_urls + urls

    def banear_view(self, request, usuario_id):
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.is_active = False
        usuario.save()
        messages.success(request, f'Usuario {usuario.username} baneado correctamente.')
        return redirect('/admin/core/usuario/')

    def desbanear_view(self, request, usuario_id):
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.is_active = True
        usuario.save()
        messages.success(request, f'Usuario {usuario.username} desbaneado correctamente.')
        return redirect('/admin/core/usuario/')

    def get_grupos(self, obj):
        return ', '.join([g.name for g in obj.groups.all()])

    get_grupos.short_description = 'groups'

    def estado_baneo(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color:green;">✅ Activo</span>')
        else:
            return mark_safe('<span style="color:red;">🚫 Baneado</span>')

    estado_baneo.short_description = 'Estado'

    def boton_banear(self, obj):
        if obj.is_active:
            return format_html(
                '<a class="button" style="background:red;color:white;padding:3px 8px;border-radius:4px;" '
                'href="{}">🚫 Banear</a>',
                f'/admin/core/usuario/banear/{obj.pk}/'
            )
        else:
            return format_html(
                '<a class="button" style="background:green;color:white;padding:3px 8px;border-radius:4px;" '
                'href="{}">✅ Desbanear</a>',
                f'/admin/core/usuario/desbanear/{obj.pk}/'
            )

    boton_banear.short_description = 'Banear'
    class Meta:
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


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    class Meta:
        model = Publicacion
        list_display = ('nombre','descripcion','fecha_creacion')
        list_filter = ('nombre','fecha_creacion')
        ordering = ('nombre',)
        fieldsets = [
            ('Datos', {
                'fields': [
                    'nombre','fecha_creacion',
                ],}),
            ('Informacion', {'fields': ('descripcion',)}),
        ]

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    class Meta:
        model = Habilidad
        list_display = ('nombre', 'estado')
        list_filter = ('estado',)
        ordering = ('nombre',)
        fieldsets = [('Datos', {'fields': ('nombre', 'estado')})]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    class Meta:
        model = Perfil
        list_display = ('usuario', 'biografia','zona_horaria','disponibilidad','preferencias','habilidades')
        list_filter = ('usuario',)
        ordering = ('usuario',)
        fieldsets = [
            ('datos',{'fields': ('usuario', 'biografia')}),
            ('Informacion detallada',{'fields': ('zona_horaria','disponibilidad', 'preferencias','habilidades')}),
        ]

@admin.register(Acuerdo)
class AcuerdoAdmin(admin.ModelAdmin):
    class Meta:
        model = Acuerdo
        list_display = ('usuario_a', 'usuario_b','publicacion','semanas','mins_sesion','sesiones_por_semana','condiciones','habilidad_tradea_a','habilidad_tradea_b')
        list_filter = ('usuario_a',)
        ordering = ('usuario_a',)
        fieldsets = [
            ('Datos', {'fields': ('usuario_a', 'usuario_b','publicacion')}),
            ('Detalles',{'fields': ('semanas', 'mins_sesion','sesiones_por_semana','condiciones')}),
            ('Intercambio',{'habilidad_tradea_a','habilidad_tradea_b'})
        ]



@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    class Meta:
        model = Sesion
        list_display = ('fecha','duracion_real','resumen','asistencia_user_a','asistencia_user_b','estado','acuerdo')
        list_filter = ('fecha',)
        ordering = ('fecha',)
        fieldsets = [
            ('Datos',{'acuerdo','duracion_real'}),
            ('Informacion', {'fields': ('resumen', 'duracion_real','estado','acuerdo')}),
            ('Usuarios',{'asistencia_user_a','asistencia_user_b'})
        ]
