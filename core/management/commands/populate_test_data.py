from django.core.management import BaseCommand
from core.models import Habilidad, Perfil, Publicacion, Acuerdo, Sesion
from django.contrib.auth import get_user_model
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating skills...')

        habilidades_nombres = ['Photoshop', 'Ingles', 'Gaming', 'Literatura', 'Estrategia', 'Indie']
        habilidades = {}
        for nombre in habilidades_nombres:
            habilidad, created = Habilidad.objects.get_or_create(nombre=nombre)
            habilidades[nombre] = habilidad
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created Skill "{nombre}"'))

        self.stdout.write('\nCreating users with their profiles...')

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
                self.stdout.write(self.style.SUCCESS(f'  ✓ User "{usuario.username}" created'))

        self.stdout.write('\nCreating posts...')
        publicaciones_data = [
            {"tipo": "OFREZCO", "descripcion": "Ofrezco clases de Photoshop", "autor": usuarios[0],
             "habilidad": habilidades["Photoshop"]},
            {"tipo": "BUSCO", "descripcion": "Busco aprender inglés", "autor": usuarios[1],
             "habilidad": habilidades["Ingles"]},
            {"tipo": "OFREZCO", "descripcion": "Ofrezco gaming coaching", "autor": usuarios[2],
             "habilidad": habilidades["Gaming"]},
            {"tipo": "BUSCO", "descripcion": "Busco clases de literatura", "autor": usuarios[3],
             "habilidad": habilidades["Literatura"]},
            {"tipo": "OFREZCO", "descripcion": "Ofrezco estrategia empresarial", "autor": usuarios[4],
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
                self.stdout.write(self.style.SUCCESS(f' ✓ Post: {pub.descripcion[:30]}'))

        self.stdout.write('\nCreating Agreements...')
        acuerdos_data = [
            {"usuario_a": usuarios[0], "usuario_b": usuarios[1], "semanas": 4, "mins_sesion": 60,
             "sesiones_por_semana": 2,
             "estado": "ACEPTADO", "condiciones": "Ejercicios diarios",
             "habilidad_tradea_a": habilidades["Photoshop"], "habilidad_tradea_b": habilidades["Ingles"]},
            {"usuario_a": usuarios[2], "usuario_b": usuarios[3], "semanas": 3, "mins_sesion": 90,
             "sesiones_por_semana": 1,
             "estado": "EN CURSO", "condiciones": "Práctica intensiva",
             "habilidad_tradea_a": habilidades["Gaming"], "habilidad_tradea_b": habilidades["Literatura"]},
            {"usuario_a": usuarios[1], "usuario_b": usuarios[4], "semanas": 5, "mins_sesion": 60,
             "sesiones_por_semana": 2,
             "estado": "PROPUESTO", "condiciones": "Material Google Drive",
             "habilidad_tradea_a": habilidades["Ingles"], "habilidad_tradea_b": habilidades["Estrategia"]},
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
                self.stdout.write(self.style.SUCCESS(f' ✓ Agreement {acuerdo.id}'))

        self.stdout.write('\nCreating Sessions...')
        sesiones_data = [
            {"fecha": date.today() + timedelta(days=1), "duracion_real": 60,
             "resumen": "Sesión introductoria", "asistencia_user_a": True, "asistencia_user_b": True,
             "estado": True, "acuerdo": acuerdos[1]},
            {"fecha": date.today() + timedelta(days=3), "duracion_real": 90,
             "resumen": "Repaso conceptos", "asistencia_user_a": True, "asistencia_user_b": False,
             "estado": True, "acuerdo": acuerdos[1]},
        ]

        for sesion_data in sesiones_data:
            try:
                sesion = Sesion(**sesion_data)
                sesion.full_clean()
                sesion.save()
                self.stdout.write(self.style.SUCCESS(f' ✓ Session {sesion.id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f' ✗ Session error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('Users: 5 | Skills: 6 | Posts: 5 | Agreements: 3 | Sessions: 2'))
