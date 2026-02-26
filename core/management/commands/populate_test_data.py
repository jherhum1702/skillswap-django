from django.core.management import BaseCommand
from core.models import Habilidad, Perfil, Publicacion, Acuerdo, Sesion
from django.contrib.auth import get_user_model
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):

        # SKILLS
        self.stdout.write('Creating skills...')

        habilidades_nombres = [
            'Photoshop', 'Inglés', 'Gaming', 'Literatura', 'Estrategia', 'Indie',
            'Python', 'JavaScript', 'React', 'Django', 'Docker', 'Linux',
            'Excel', 'SQL', 'Machine Learning', 'Diseño UX/UI', 'Figma',
            'Illustrator', 'After Effects', 'Edición de Vídeo',
            'Guitarra', 'Piano', 'Canto', 'Producción Musical',
            'Francés', 'Alemán', 'Japonés', 'Chino Mandarín',
            'Marketing Digital', 'SEO', 'Copywriting', 'Redes Sociales',
            'Fotografía', 'Cocina', 'Yoga', 'Ajedrez',
        ]

        habilidades = {}
        for nombre in habilidades_nombres:
            hab, created = Habilidad.objects.get_or_create(nombre=nombre)
            habilidades[nombre] = hab
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Skill "{nombre}" created successfully.'))


        # USERS + PROFILES
        self.stdout.write('\nCreating users with their profiles...')

        usuarios_data = [
            ("Paco",      "Tester",    "pacogamer30",  "pacotest@gmail.com",    "1234", "Me gusta aprender programación y gaming.",        "Europe/Madrid",                    "Lunes a viernes 8-22h"),
            ("Ana",       "López",     "anadev",       "ana@gmail.com",          "1234", "Frontend developer apasionada por el diseño.",   "Europe/Madrid",                    "Fines de semana"),
            ("Luis",      "Martín",    "luism",        "luis@gmail.com",         "1234", "Apasionado por la ciberseguridad y Linux.",       "Europe/London",                    "Tardes entre semana"),
            ("María",     "Gómez",     "mariadev",     "maria@gmail.com",        "1234", "Data scientist junior, amante del ML.",           "Europe/Paris",                     "Mañanas"),
            ("Carlos",    "Ruiz",      "carlosdev",    "carlos@gmail.com",       "1234", "Backend developer con Django y Docker.",          "America/Argentina/Buenos_Aires",   "Noches"),
            ("Sofía",     "Hernández", "sofiahm",      "sofia@gmail.com",        "1234", "Diseñadora UX/UI freelance.",                     "Europe/Madrid",                    "Lunes, miércoles y viernes tarde"),
            ("Jorge",     "Pérez",     "jorgeperez",   "jorge@gmail.com",        "1234", "Músico y productor musical autodidacta.",         "Europe/Madrid",                    "Noches y fines de semana"),
            ("Laura",     "Sánchez",   "laurasan",     "laura@gmail.com",        "1234", "Profesora de inglés nativa. Aprendo programación.","Europe/London",                  "Mañanas entre semana"),
            ("David",     "Jiménez",   "davidj",       "david@gmail.com",        "1234", "Estudiante de máster en IA.",                     "Europe/Madrid",                    "Tardes"),
            ("Elena",     "Torres",    "elenatorres",  "elena@gmail.com",        "1234", "Fotógrafa profesional y amante del yoga.",        "Europe/Madrid",                    "Flexible"),
            ("Pablo",     "Moreno",    "pablomoreno",  "pablo@gmail.com",        "1234", "Desarrollador full-stack con React y Django.",    "Europe/Madrid",                    "Noches entre semana"),
            ("Carmen",    "Díaz",      "carmend",      "carmen@gmail.com",       "1234", "Experta en marketing digital y SEO.",             "Europe/Madrid",                    "Mañanas y mediodía"),
            ("Miguel",    "Fernández", "miguelf",      "miguel@gmail.com",       "1234", "Chef aficionado. Quiero aprender inglés.",         "Europe/Madrid",                    "Fines de semana"),
            ("Lucía",     "Romero",    "luciarom",     "lucia@gmail.com",        "1234", "Pianista clásica. Interesada en producción.",     "Europe/Paris",                     "Tardes"),
            ("Alejandro", "Alonso",    "alexalonso",   "alejandro@gmail.com",    "1234", "Ajedrecista amateur. Aprendo japonés.",           "Europe/Madrid",                    "Noches"),
            ("Isabel",    "Navarro",   "isanav",       "isabel@gmail.com",       "1234", "Copywriter y redactora de contenidos.",           "America/Mexico_City",              "Mañanas"),
            ("Fernando",  "Ramos",     "fernandor",    "fernando@gmail.com",     "1234", "Guitarrista y profesor de música.",               "Europe/Madrid",                    "Tardes y noches"),
            ("Natalia",   "Gil",       "nataliagil",   "natalia@gmail.com",      "1234", "Especialista en redes sociales y contenido.",     "Europe/Madrid",                    "Flexible"),
            ("Roberto",   "Serrano",   "robertoserr",  "roberto@gmail.com",      "1234", "Ingeniero de datos. Aprendo alemán.",             "Europe/Berlin",                    "Mañanas entre semana"),
            ("Claudia",   "Molina",    "claudiam",     "claudia@gmail.com",      "1234", "Estudiante de Filología. Enseño francés.",        "Europe/Paris",                     "Mediodías"),
        ]

        Usuario = get_user_model()
        usuarios = []

        for (first_name, last_name, username, email, password,
             biografia, zona_horaria, disponibilidad) in usuarios_data:

            usuario, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                }
            )
            if created:
                usuario.set_password(password)
                usuario.save()
                Perfil.objects.create(
                    usuario=usuario,
                    biografia=biografia,
                    zona_horaria=zona_horaria,
                    disponibilidad=disponibilidad,
                )
                self.stdout.write(self.style.SUCCESS(f'  ✓ User "{username}" created successfully.'))
            else:
                self.stdout.write(f'  – User "{username}" already exists')

            usuarios.append(usuario)

        # Assign skills to profiles
        perfil_habilidades = {
            "pacogamer30":  ["Photoshop", "Gaming", "Python"],
            "anadev":       ["React", "Figma", "Diseño UX/UI", "JavaScript"],
            "luism":        ["Linux", "Docker", "Python"],
            "mariadev":     ["Machine Learning", "Python", "SQL"],
            "carlosdev":    ["Django", "Docker", "Python", "SQL"],
            "sofiahm":      ["Figma", "Diseño UX/UI", "Illustrator", "Photoshop"],
            "jorgeperez":   ["Guitarra", "Piano", "Producción Musical"],
            "laurasan":     ["Inglés", "Literatura", "Copywriting"],
            "davidj":       ["Machine Learning", "Python", "SQL", "React"],
            "elenatorres":  ["Fotografía", "Yoga", "Photoshop"],
            "pablomoreno":  ["React", "Django", "JavaScript", "Docker"],
            "carmend":      ["Marketing Digital", "SEO", "Copywriting", "Redes Sociales"],
            "miguelf":      ["Cocina"],
            "luciarom":     ["Piano", "Canto"],
            "alexalonso":   ["Ajedrez", "Estrategia"],
            "isanav":       ["Copywriting", "Marketing Digital", "SEO"],
            "fernandor":    ["Guitarra", "Canto", "Producción Musical"],
            "nataliagil":   ["Redes Sociales", "Fotografía", "Marketing Digital"],
            "robertoserr":  ["SQL", "Python", "Machine Learning", "Excel"],
            "claudiam":     ["Francés", "Literatura", "Inglés"],
        }

        for username, skill_names in perfil_habilidades.items():
            try:
                perfil = Perfil.objects.get(usuario__username=username)
                for skill_name in skill_names:
                    if skill_name in habilidades:
                        perfil.habilidades.add(habilidades[skill_name])
            except Perfil.DoesNotExist:
                pass

        # ─────────────────────────────────────────────
        # POSTS
        # ─────────────────────────────────────────────
        self.stdout.write('\nCreating posts...')

        publicaciones_data = [
            # OFREZCO
            ("OFREZCO", "Ofrezco clases de Photoshop para principiantes",          "pacogamer30",  "Photoshop"),
            ("OFREZCO", "Enseño Python desde cero, con proyectos reales",          "pacogamer30",  "Python"),
            ("OFREZCO", "Clases de React y hooks modernos",                        "anadev",       "React"),
            ("OFREZCO", "Diseño interfaces en Figma, portfolio incluido",          "anadev",       "Figma"),
            ("OFREZCO", "Explico Linux y administración de sistemas",              "luism",        "Linux"),
            ("OFREZCO", "Introduzco Docker y contenedores desde cero",             "luism",        "Docker"),
            ("OFREZCO", "Machine Learning aplicado con scikit-learn",              "mariadev",     "Machine Learning"),
            ("OFREZCO", "Clases de SQL avanzado y optimización de queries",        "carlosdev",    "SQL"),
            ("OFREZCO", "Desarrollo de APIs REST con Django",                      "carlosdev",    "Django"),
            ("OFREZCO", "Diseño UX/UI con metodología centrada en usuario",        "sofiahm",      "Diseño UX/UI"),
            ("OFREZCO", "Clases de guitarra eléctrica y acústica",                 "fernandor",    "Guitarra"),
            ("OFREZCO", "Inglés conversacional con hablante nativa",               "laurasan",     "Inglés"),
            ("OFREZCO", "Producción musical en Ableton Live",                      "jorgeperez",   "Producción Musical"),
            ("OFREZCO", "Fotografía de retrato y paisaje urbano",                  "elenatorres",  "Fotografía"),
            ("OFREZCO", "SEO técnico y estrategia de contenidos",                  "carmend",      "SEO"),
            ("OFREZCO", "Copywriting persuasivo para landing pages",               "isanav",       "Copywriting"),
            ("OFREZCO", "Piano clásico para todos los niveles",                    "luciarom",     "Piano"),
            ("OFREZCO", "Clases de francés conversacional",                        "claudiam",     "Francés"),
            ("OFREZCO", "Recetas de cocina mediterránea paso a paso",              "miguelf",      "Cocina"),
            ("OFREZCO", "Estrategia de ajedrez: aperturas y finales",              "alexalonso",   "Ajedrez"),
            ("OFREZCO", "Gestión de redes sociales y creación de contenido",       "nataliagil",   "Redes Sociales"),
            ("OFREZCO", "Análisis de datos con Python y Pandas",                   "robertoserr",  "Python"),
            ("OFREZCO", "Excel avanzado: tablas dinámicas y macros",               "robertoserr",  "Excel"),
            ("OFREZCO", "JavaScript moderno (ES2023) y async/await",               "pablomoreno",  "JavaScript"),
            ("OFREZCO", "Marketing digital: campañas en Meta y Google Ads",        "carmend",      "Marketing Digital"),
            # BUSCO
            ("BUSCO",   "Busco aprender inglés para trabajo remoto",               "pacogamer30",  "Inglés"),
            ("BUSCO",   "Quiero aprender guitarra, tengo disponibilidad por tardes","carlosdev",   "Guitarra"),
            ("BUSCO",   "Busco clases de piano, soy principiante total",           "davidj",       "Piano"),
            ("BUSCO",   "Quiero aprender fotografía profesional",                  "sofiahm",      "Fotografía"),
            ("BUSCO",   "Busco aprender a cocinar platos internacionales",         "laurasan",     "Cocina"),
            ("BUSCO",   "Me interesa aprender japonés desde cero",                 "alexalonso",   "Japonés"),
            ("BUSCO",   "Quiero aprender React para proyectos freelance",          "luism",        "React"),
            ("BUSCO",   "Busco aprender SEO para mi blog personal",                "miguelf",      "SEO"),
            ("BUSCO",   "Quiero mejorar en Machine Learning avanzado",             "pablomoreno",  "Machine Learning"),
            ("BUSCO",   "Busco clases de alemán para negocios",                    "robertoserr",  "Alemán"),
            ("BUSCO",   "Quiero aprender producción musical básica",               "fernandor",    "Producción Musical"),
            ("BUSCO",   "Busco aprender Figma para mis proyectos",                 "davidj",       "Figma"),
            ("BUSCO",   "Me interesa aprender estrategia empresarial",             "nataliagil",   "Estrategia"),
            ("BUSCO",   "Quiero aprender yoga para el estrés",                     "carmend",      "Yoga"),
            ("BUSCO",   "Busco clases de Illustrator para diseño vectorial",       "nataliagil",   "Illustrator"),
            ("BUSCO",   "Quiero aprender SQL para análisis de datos",              "anadev",       "SQL"),
            ("BUSCO",   "Busco aprender copywriting para mi negocio",              "elenatorres",  "Copywriting"),
            ("BUSCO",   "Me interesa aprender Docker para mis proyectos",          "mariadev",     "Docker"),
            ("BUSCO",   "Quiero aprender ajedrez desde nivel básico",              "claudiam",     "Ajedrez"),
            ("BUSCO",   "Busco aprender francés para viajar a París",              "jorgeperez",   "Francés"),
        ]

        publicaciones = []
        for tipo, descripcion, username, habilidad_nombre in publicaciones_data:
            try:
                autor = Usuario.objects.get(username=username)
                habilidad = habilidades[habilidad_nombre]
                pub, created = Publicacion.objects.get_or_create(
                    descripcion=descripcion,
                    defaults={"tipo": tipo, "autor": autor, "habilidad": habilidad}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Post ({tipo}): {descripcion[:45]}'))
                publicaciones.append(pub)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Post error "{descripcion[:40]}": {e}'))

        # AGREEMENTS
        self.stdout.write('\nCreating agreements...')

        # Helper to get user by username
        def u(username):
            return next(usr for usr in usuarios if usr.username == username)

        def h(nombre):
            return habilidades[nombre]

        acuerdos_data = [
            # (usuario_a, usuario_b, semanas, mins, sesiones/semana, estado, condiciones, hab_a, hab_b)
            ("pacogamer30", "laurasan",    4, 60, 2, "EN CURSO",   "Ejercicios semanales y vocabulario específico.", "Photoshop",        "Inglés"),
            ("anadev",      "carlosdev",   3, 60, 2, "EN CURSO",   "Revisión de proyectos reales en cada sesión.",   "React",            "Django"),
            ("luism",       "pablomoreno", 5, 90, 1, "EN CURSO",   "Prácticas con servidor propio en VPS.",          "Linux",            "JavaScript"),
            ("mariadev",    "davidj",      6, 60, 2, "EN CURSO",   "Kaggle competitions como práctica.",             "Machine Learning", "SQL"),
            ("sofiahm",     "elenatorres", 4, 60, 1, "EN CURSO",   "Feedback mutuo en portfolio.",                   "Figma",            "Fotografía"),
            ("jorgeperez",  "claudiam",    3, 90, 2, "EN CURSO",   "Canciones en francés como práctica.",            "Producción Musical","Francés"),
            ("fernandor",   "miguelf",     4, 60, 1, "EN CURSO",   "Recetas temáticas por sesión.",                  "Guitarra",         "Cocina"),
            ("carmend",     "isanav",      5, 60, 2, "EN CURSO",   "Análisis de campañas reales semanales.",         "SEO",              "Copywriting"),
            ("luciarom",    "alexalonso",  4, 60, 1, "EN CURSO",   "Partidas comentadas tras cada sesión.",          "Piano",            "Ajedrez"),
            ("nataliagil",  "robertoserr", 3, 60, 2, "EN CURSO",   "Proyecto de dashboard como hilo conductor.",     "Redes Sociales",   "Python"),

            ("pacogamer30", "anadev",      4, 60, 1, "ACEPTADO",   "Revisión de portfolio al finalizar.",            "Python",           "React"),
            ("luism",       "mariadev",    3, 60, 2, "ACEPTADO",   "Entorno de pruebas compartido en cloud.",        "Docker",           "Machine Learning"),
            ("carlosdev",   "davidj",      5, 90, 1, "ACEPTADO",   "Proyecto API + frontend como resultado.",        "Django",           "Figma"),
            ("sofiahm",     "carmend",     4, 60, 2, "ACEPTADO",   "Caso real de branding como práctica.",           "Diseño UX/UI",     "Marketing Digital"),
            ("fernandor",   "jorgeperez",  6, 60, 2, "ACEPTADO",   "Componer una canción juntos al final.",          "Guitarra",         "Producción Musical"),
            ("elenatorres", "nataliagil",  3, 60, 1, "ACEPTADO",   "Shooting fotográfico para RRSS como meta.",      "Fotografía",       "Redes Sociales"),
            ("claudiam",    "alexalonso",  4, 60, 1, "ACEPTADO",   "Literatura francesa de apertura en ajedrez.",    "Francés",          "Ajedrez"),
            ("robertoserr", "isanav",      5, 60, 2, "ACEPTADO",   "Newsletter conjunta como proyecto final.",       "Excel",            "Copywriting"),

            ("pablomoreno", "luism",       3, 60, 1, "PROPUESTO",  "Acordar horario a confirmar.",                   "React",            "Linux"),
            ("davidj",      "sofiahm",     4, 60, 2, "PROPUESTO",  "Pendiente confirmar disponibilidad.",            "Machine Learning", "Figma"),
            ("miguelf",     "claudiam",    3, 60, 1, "PROPUESTO",  "Intercambio recetas+idioma, pendiente inicio.",  "Cocina",           "Francés"),
            ("luciarom",    "fernandor",   4, 90, 1, "PROPUESTO",  "Sesiones combinadas música clásica/moderna.",    "Piano",            "Guitarra"),
            ("carmend",     "nataliagil",  5, 60, 2, "PROPUESTO",  "Estrategia de contenido como proyecto.",         "SEO",              "Redes Sociales"),
            ("isanav",      "elenatorres", 3, 60, 1, "PROPUESTO",  "Portafolio fotográfico con copy incluido.",      "Copywriting",      "Fotografía"),

            ("pacogamer30", "carlosdev",   4, 60, 2, "FINALIZADO", "Completado con éxito. Buen intercambio.",        "Photoshop",        "Docker"),
            ("anadev",      "mariadev",    3, 60, 1, "FINALIZADO", "Objetivo alcanzado en todas las sesiones.",      "Figma",            "SQL"),
            ("luism",       "davidj",      5, 60, 2, "FINALIZADO", "Proyecto desplegado en producción.",             "Linux",            "Machine Learning"),
            ("jorgeperez",  "fernandor",   4, 90, 1, "FINALIZADO", "Canción compuesta y grabada juntos.",            "Producción Musical","Guitarra"),
            ("robertoserr", "carmend",     3, 60, 2, "FINALIZADO", "Dashboard de métricas de marketing entregado.",  "Python",           "Marketing Digital"),

            ("sofiahm",     "luism",       3, 60, 2, "CANCELADO",  "Cancelado por incompatibilidad de horarios.",    "Illustrator",      "Docker"),
            ("miguelf",     "alexalonso",  4, 60, 1, "CANCELADO",  "Cancelado por cambio de prioridades.",           "Cocina",           "Estrategia"),
        ]

        acuerdos = []
        for (ua, ub, semanas, mins, sxs, estado, condiciones, ha, hb) in acuerdos_data:
            try:
                acuerdo, created = Acuerdo.objects.get_or_create(
                    usuario_a=u(ua),
                    usuario_b=u(ub),
                    habilidad_tradea_a=h(ha),
                    habilidad_tradea_b=h(hb),
                    defaults={
                        "semanas": semanas,
                        "mins_sesion": mins,
                        "sesiones_por_semana": sxs,
                        "estado": estado,
                        "condiciones": condiciones,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Agreement {acuerdo.id}: {ua} ↔ {ub} [{ha}↔{hb}] ({estado}) created successfully.'))
                acuerdos.append(acuerdo)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Agreement error {ua}↔{ub}: {e}'))


        # SESSIONS EN CURSO

        self.stdout.write('\nCreating sessions...')

        en_curso = [a for a in acuerdos if a.estado == 'EN CURSO']

        sesiones_por_acuerdo = [
            # (days_offset, duracion, resumen, asist_a, asist_b)
            [
                (1,  60, "Sesión introductoria: presentación y objetivos.",      True,  True),
                (8,  60, "Práctica guiada sobre conceptos básicos.",             True,  True),
                (15, 60, "Resolución de dudas y ejercicios propuestos.",         True,  False),
                (22, 60, "Avance significativo, primeros resultados visibles.",  True,  True),
            ],
            [
                (2,  60, "Primera toma de contacto y nivelación.",              True,  True),
                (9,  60, "Profundización en conceptos intermedios.",            True,  True),
                (16, 90, "Proyecto práctico en desarrollo.",                    False, True),
            ],
            [
                (3,  60, "Sesión inicial con definición de roadmap.",           True,  True),
                (10, 60, "Ejercicios aplicados con feedback.",                  True,  True),
                (17, 60, "Revisión de avances y correcciones.",                 True,  True),
                (24, 60, "Práctica autónoma supervisada.",                      True,  True),
                (31, 60, "Consolidación de conocimientos adquiridos.",          True,  False),
            ],
            [
                (1,  60, "Onboarding y acuerdo de metodología de trabajo.",     True,  True),
                (8,  60, "Primera entrega de ejercicios revisada.",             True,  True),
                (15, 60, "Sesión intensiva de práctica avanzada.",              True,  True),
            ],
        ]

        sesion_count = 0
        for i, acuerdo in enumerate(en_curso):
            template = sesiones_por_acuerdo[i % len(sesiones_por_acuerdo)]
            for (days, dur, resumen, asist_a, asist_b) in template:
                try:
                    sesion = Sesion(
                        fecha=date.today() + timedelta(days=days),
                        duracion_real=dur,
                        resumen=resumen,
                        asistencia_user_a=asist_a,
                        asistencia_user_b=asist_b,
                        estado=True,
                        acuerdo=acuerdo,
                    )
                    sesion.full_clean()
                    sesion.save()
                    sesion_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Session {sesion.id} — Acuerdo {acuerdo.id} (+{days}d): {resumen[:40]} created successfully.'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'  ✗ Session error (Acuerdo {acuerdo.id}, +{days}d): {e}'
                    ))

        # SUMMARY
        self.stdout.write(self.style.SUCCESS('\n🎉 Database populated successfully.'))
        self.stdout.write(self.style.SUCCESS(
            f'Skills: {len(habilidades_nombres)} | '
            f'Users: {len(usuarios_data)} | '
            f'Posts: {len(publicaciones_data)} | '
            f'Agreements: {len(acuerdos_data)} | '
            f'Sessions: {sesion_count}'
        ))
