from django.core.management import BaseCommand
from core.models import Habilidad, Perfil, Publicacion, Acuerdo, Sesion
from django.contrib.auth import get_user_model
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating skills...')

        # Create Skills
        habilidades_nombres = ['Photoshop', 'Ingles', 'Gaming', 'Literatura', 'Estrategia', 'Indie']
        habilidades = {}
        for nombre in habilidades_nombres:
            habilidad, created = Habilidad.objects.get_or_create(nombre=nombre)
            habilidades[nombre] = habilidad
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created Skill "{nombre}"'))

        self.stdout.write('\nCreating users with their profiles...')

        # Create Users with their profile
        Usuario = get_user_model()

        usuarios_data = [
            {"first_name": "Paco", "last_name": "Tester", "username": "pacogamer30", "email": "pacotest@gmail.com",
             "password": "1234", "perfil": {"biografia": "Me gusta aprender programación.", "zona_horaria": "Europe/Madrid",
                                            "disponibilidad": "Lunes a viernes de 8:00 a 22:00"}},
            {"first_name": "Ana", "last_name": "López", "username": "anadev", "email": "ana@gmail.com",
             "password": "1234", "perfil": {"biografia": "Frontend developer.", "zona_horaria": "Europe/Madrid",
                                            "disponibilidad": "Fines de semana"}},
            {"first_name": "Luis", "last_name": "Martín", "username": "luism", "email": "luis@gmail.com",
             "password": "1234", "perfil": {"biografia": "Apasionado por la ciberseguridad.", "zona_horaria": "Europe/London",
                                            "disponibilidad": "Tardes entre semana"}},
            {"first_name": "María", "last_name": "Gómez", "username": "mariadev", "email": "maria@gmail.com",
             "password": "1234", "perfil": {"biografia": "Data scientist junior.", "zona_horaria": "Europe/Paris",
                                            "disponibilidad": "Mañanas"}},
            {"first_name": "Carlos", "last_name": "Ruiz", "username": "carlosdev", "email": "carlos@gmail.com",
             "password": "1234", "perfil": {"biografia": "Backend con Django.", "zona_horaria": "America/Argentina/Buenos_Aires",
                                            "disponibilidad": "Noches"}},
        ]

        usuarios = []

        for usuario_data in usuarios_data:
            perfil_data = usuario_data.pop("perfil")
            password = usuario_data.pop("password")

            usuario, created = Usuario.objects.get_or_create(
                username=usuario_data["username"],
                defaults=usuario_data
            )

            if created:
                usuario.set_password(password)
                usuario.save()
                Perfil.objects.create(usuario=usuario, **perfil_data)
                usuarios.append(usuario)
                self.stdout.write(self.style.SUCCESS(f'  ✓ User "{usuario.username}" and profile created successfully'))

        # Create posts
        self.stdout.write('\nCreating posts...')
        publicaciones_data = [
            {"tipo": "OFREZCO", "descripcion": "Ofrezco clases de Python para principiantes", "autor": usuarios[0],
             "habilidad": habilidades["Photoshop"]},
            {"tipo": "BUSCO", "descripcion": "Busco aprender inglés a cambio de programación", "autor": usuarios[1],
             "habilidad": habilidades["Ingles"]},
            {"tipo": "OFREZCO", "descripcion": "Ofrezco diseño gráfico con Photoshop", "autor": usuarios[2],
             "habilidad": habilidades["Gaming"]},
            {"tipo": "BUSCO", "descripcion": "Busco aprender bases de datos SQL", "autor": usuarios[3],
             "habilidad": habilidades["Literatura"]},
            {"tipo": "OFREZCO", "descripcion": "Ofrezco ayuda con Django y APIs REST", "autor": usuarios[4],
             "habilidad": habilidades["Estrategia"]},
        ]

        publicaciones = []
        for pub_data in publicaciones_data:
            pub, created = Publicacion.objects.get_or_create(
                descripcion=pub_data["descripcion"],
                defaults=pub_data
            )
            if created:
                publicaciones.append(pub)
                self.stdout.write(self.style.SUCCESS(f' ✓ Created post: {pub.descripcion[:30]}'))

        # Create agreements
        self.stdout.write('\nCreating Agreements...')
        acuerdos_data = [
            {"usuario_a": usuarios[0], "usuario_b": usuarios[1], "semanas": 4, "mins_sesion": 60, "sesiones_por_semana": 2,
             "estado": "ACEPTADO", "condiciones": "Ejercicios al final de cada sesión",
             "habilidad_tradea_a": habilidades["Photoshop"], "habilidad_tradea_b": habilidades["Ingles"]},
            {"usuario_a": usuarios[2], "usuario_b": usuarios[3], "semanas": 3, "mins_sesion": 90, "sesiones_por_semana": 1,
             "estado": "EN CURSO", "condiciones": "Clases prácticas",
             "habilidad_tradea_a": habilidades["Gaming"], "habilidad_tradea_b": habilidades["Literatura"]},
            {"usuario_a": usuarios[1], "usuario_b": usuarios[4], "semanas": 5, "mins_sesion": 60, "sesiones_por_semana": 2,
             "estado": "PROPUESTO", "condiciones": "Material compartido por Drive",
             "habilidad_tradea_a": habilidades["Ingles"], "habilidad_tradea_b": habilidades["Estrategia"]},
            {"usuario_a": usuarios[3], "usuario_b": usuarios[0], "semanas": 2, "mins_sesion": 120, "sesiones_por_semana": 1,
             "estado": "EN CURSO", "condiciones": "Sesiones grabadas",
             "habilidad_tradea_a": habilidades["Literatura"], "habilidad_tradea_b": habilidades["Photoshop"]},
            {"usuario_a": usuarios[4], "usuario_b": usuarios[2], "semanas": 6, "mins_sesion": 60, "sesiones_por_semana": 3,
             "estado": "ACEPTADO", "condiciones": "Proyecto final obligatorio",
             "habilidad_tradea_a": habilidades["Estrategia"], "habilidad_tradea_b": habilidades["Gaming"]},
        ]

        acuerdos = []
        for acuerdo_data in acuerdos_data:
            acuerdo, created = Acuerdo.objects.get_or_create(
                usuario_a=acuerdo_data["usuario_a"],
                usuario_b=acuerdo_data["usuario_b"],
                habilidad_tradea_a=acuerdo_data["habilidad_tradea_a"],
                habilidad_tradea_b=acuerdo_data["habilidad_tradea_b"],
                defaults=acuerdo_data
            )
            if created:
                acuerdos.append(acuerdo)
                self.stdout.write(self.style.SUCCESS(
                    f' ✓ Agreement between {acuerdo.usuario_a} and {acuerdo.usuario_b} created successfully.'))

        # Create Sessions
        self.stdout.write('\nCreating Sessions...')
        sesiones_data = [
            {"fecha": date.today() + timedelta(days=1), "duracion_real": 60,
             "resumen": "Primera sesión de introducción", "asistencia_user_a": True, "asistencia_user_b": True,
             "estado": True, "acuerdo": acuerdos[1]},
            {"fecha": date.today() + timedelta(days=3), "duracion_real": 90,
             "resumen": "Repaso de conceptos", "asistencia_user_a": True, "asistencia_user_b": False,
             "estado": True, "acuerdo": acuerdos[1]},
            {"fecha": date.today() + timedelta(days=2), "duracion_real": 120,
             "resumen": "Proyecto práctico", "asistencia_user_a": True, "asistencia_user_b": True,
             "estado": True, "acuerdo": acuerdos[3]},
            {"fecha": date.today() + timedelta(days=4), "duracion_real": 60,
             "resumen": "Evaluación intermedia", "asistencia_user_a": True, "asistencia_user_b": True,
             "estado": True, "acuerdo": acuerdos[3]},
            {"fecha": date.today() + timedelta(days=5), "duracion_real": 90,
             "resumen": "Cierre del módulo", "asistencia_user_a": False, "asistencia_user_b": True,
             "estado": True, "acuerdo": acuerdos[3]},
        ]

        for sesion_data in sesiones_data:
            sesion = Sesion(**sesion_data)
            sesion.full_clean()
            sesion.save()

        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))