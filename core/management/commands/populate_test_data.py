from django.core.management import BaseCommand
from core.models import Habilidad, Perfil, Publicacion, Acuerdo, Sesion
from django.contrib.auth import get_user_model
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate db with test data'

    def handle(self, *args, **kwargs):
        Usuario = get_user_model()

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

        for nombre in habilidades_nombres:
            hab, created = Habilidad.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Skill "{nombre}" created successfully.'))

        # USERS
        self.stdout.write('\nCreating users...')

        usuarios_data = [
            {
                'username': 'pacogamer30', 'first_name': 'Paco', 'last_name': 'Tester',
                'email': 'pacotest@gmail.com', 'password': '1234',
                'biografia': 'Me gusta aprender programación y gaming.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Lunes a viernes 8-22h',
            },
            {
                'username': 'anadev', 'first_name': 'Ana', 'last_name': 'López',
                'email': 'ana@gmail.com', 'password': '1234',
                'biografia': 'Frontend developer apasionada por el diseño.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Fines de semana',
            },
            {
                'username': 'luism', 'first_name': 'Luis', 'last_name': 'Martín',
                'email': 'luis@gmail.com', 'password': '1234',
                'biografia': 'Apasionado por la ciberseguridad y Linux.',
                'zona_horaria': 'Europe/London', 'disponibilidad': 'Tardes entre semana',
            },
            {
                'username': 'mariadev', 'first_name': 'María', 'last_name': 'Gómez',
                'email': 'maria@gmail.com', 'password': '1234',
                'biografia': 'Data scientist junior, amante del ML.',
                'zona_horaria': 'Europe/Paris', 'disponibilidad': 'Mañanas',
            },
            {
                'username': 'carlosdev', 'first_name': 'Carlos', 'last_name': 'Ruiz',
                'email': 'carlos@gmail.com', 'password': '1234',
                'biografia': 'Backend developer con Django y Docker.',
                'zona_horaria': 'America/Argentina/Buenos_Aires', 'disponibilidad': 'Noches',
            },
            {
                'username': 'sofiahm', 'first_name': 'Sofía', 'last_name': 'Hernández',
                'email': 'sofia@gmail.com', 'password': '1234',
                'biografia': 'Diseñadora UX/UI freelance.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Lunes, miércoles y viernes tarde',
            },
            {
                'username': 'jorgeperez', 'first_name': 'Jorge', 'last_name': 'Pérez',
                'email': 'jorge@gmail.com', 'password': '1234',
                'biografia': 'Músico y productor musical autodidacta.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Noches y fines de semana',
            },
            {
                'username': 'laurasan', 'first_name': 'Laura', 'last_name': 'Sánchez',
                'email': 'laura@gmail.com', 'password': '1234',
                'biografia': 'Profesora de inglés nativa. Aprendo programación.',
                'zona_horaria': 'Europe/London', 'disponibilidad': 'Mañanas entre semana',
            },
            {
                'username': 'davidj', 'first_name': 'David', 'last_name': 'Jiménez',
                'email': 'david@gmail.com', 'password': '1234',
                'biografia': 'Estudiante de máster en IA.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Tardes',
            },
            {
                'username': 'elenatorres', 'first_name': 'Elena', 'last_name': 'Torres',
                'email': 'elena@gmail.com', 'password': '1234',
                'biografia': 'Fotógrafa profesional y amante del yoga.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Flexible',
            },
            {
                'username': 'pablomoreno', 'first_name': 'Pablo', 'last_name': 'Moreno',
                'email': 'pablo@gmail.com', 'password': '1234',
                'biografia': 'Desarrollador full-stack con React y Django.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Noches entre semana',
            },
            {
                'username': 'carmend', 'first_name': 'Carmen', 'last_name': 'Díaz',
                'email': 'carmen@gmail.com', 'password': '1234',
                'biografia': 'Experta en marketing digital y SEO.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Mañanas y mediodía',
            },
            {
                'username': 'miguelf', 'first_name': 'Miguel', 'last_name': 'Fernández',
                'email': 'miguel@gmail.com', 'password': '1234',
                'biografia': 'Chef aficionado. Quiero aprender inglés.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Fines de semana',
            },
            {
                'username': 'luciarom', 'first_name': 'Lucía', 'last_name': 'Romero',
                'email': 'lucia@gmail.com', 'password': '1234',
                'biografia': 'Pianista clásica. Interesada en producción.',
                'zona_horaria': 'Europe/Paris', 'disponibilidad': 'Tardes',
            },
            {
                'username': 'alexalonso', 'first_name': 'Alejandro', 'last_name': 'Alonso',
                'email': 'alejandro@gmail.com', 'password': '1234',
                'biografia': 'Ajedrecista amateur. Aprendo japonés.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Noches',
            },
            {
                'username': 'isanav', 'first_name': 'Isabel', 'last_name': 'Navarro',
                'email': 'isabel@gmail.com', 'password': '1234',
                'biografia': 'Copywriter y redactora de contenidos.',
                'zona_horaria': 'America/Mexico_City', 'disponibilidad': 'Mañanas',
            },
            {
                'username': 'fernandor', 'first_name': 'Fernando', 'last_name': 'Ramos',
                'email': 'fernando@gmail.com', 'password': '1234',
                'biografia': 'Guitarrista y profesor de música.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Tardes y noches',
            },
            {
                'username': 'nataliagil', 'first_name': 'Natalia', 'last_name': 'Gil',
                'email': 'natalia@gmail.com', 'password': '1234',
                'biografia': 'Especialista en redes sociales y contenido.',
                'zona_horaria': 'Europe/Madrid', 'disponibilidad': 'Flexible',
            },
            {
                'username': 'robertoserr', 'first_name': 'Roberto', 'last_name': 'Serrano',
                'email': 'roberto@gmail.com', 'password': '1234',
                'biografia': 'Ingeniero de datos. Aprendo alemán.',
                'zona_horaria': 'Europe/Berlin', 'disponibilidad': 'Mañanas entre semana',
            },
            {
                'username': 'claudiam', 'first_name': 'Claudia', 'last_name': 'Molina',
                'email': 'claudia@gmail.com', 'password': '1234',
                'biografia': 'Estudiante de Filología. Enseño francés.',
                'zona_horaria': 'Europe/Paris', 'disponibilidad': 'Mediodías',
            },
        ]

        for datos in usuarios_data:
            usuario, created = Usuario.objects.get_or_create(
                username=datos['username'],
                defaults={
                    'first_name': datos['first_name'],
                    'last_name':  datos['last_name'],
                    'email':      datos['email'],
                }
            )
            if created:
                usuario.set_password(datos['password'])
                usuario.save()
                Perfil.objects.create(
                    usuario=usuario,
                    biografia=datos['biografia'],
                    zona_horaria=datos['zona_horaria'],
                    disponibilidad=datos['disponibilidad'],
                )
                self.stdout.write(self.style.SUCCESS(f'  ✓ User "{usuario.username}" created successfully.'))

        # SKILLS PER PROFILE
        self.stdout.write('\nAdding skills to profiles...')

        habilidades_por_perfil = {
            'pacogamer30':  ['Photoshop', 'Gaming', 'Python'],
            'anadev':       ['React', 'Figma', 'Diseño UX/UI', 'JavaScript'],
            'luism':        ['Linux', 'Docker', 'Python'],
            'mariadev':     ['Machine Learning', 'Python', 'SQL'],
            'carlosdev':    ['Django', 'Docker', 'Python', 'SQL'],
            'sofiahm':      ['Figma', 'Diseño UX/UI', 'Illustrator', 'Photoshop'],
            'jorgeperez':   ['Guitarra', 'Piano', 'Producción Musical'],
            'laurasan':     ['Inglés', 'Literatura', 'Copywriting'],
            'davidj':       ['Machine Learning', 'Python', 'SQL', 'React'],
            'elenatorres':  ['Fotografía', 'Yoga', 'Photoshop'],
            'pablomoreno':  ['React', 'Django', 'JavaScript', 'Docker'],
            'carmend':      ['Marketing Digital', 'SEO', 'Copywriting', 'Redes Sociales'],
            'miguelf':      ['Cocina'],
            'luciarom':     ['Piano', 'Canto'],
            'alexalonso':   ['Ajedrez', 'Estrategia'],
            'isanav':       ['Copywriting', 'Marketing Digital', 'SEO'],
            'fernandor':    ['Guitarra', 'Canto', 'Producción Musical'],
            'nataliagil':   ['Redes Sociales', 'Fotografía', 'Marketing Digital'],
            'robertoserr':  ['SQL', 'Python', 'Machine Learning', 'Excel'],
            'claudiam':     ['Francés', 'Literatura', 'Inglés'],
        }

        for username, nombres_habilidades in habilidades_por_perfil.items():
            try:
                perfil = Perfil.objects.get(usuario__username=username)
                for nombre in nombres_habilidades:
                    perfil.habilidades.add(Habilidad.objects.get(nombre=nombre))
            except Perfil.DoesNotExist:
                pass

        # POSTS
        self.stdout.write('\nCreating posts...')

        publicaciones_data = [
            # OFREZCO
            ('OFREZCO', 'Ofrezco clases de Photoshop para principiantes',           'pacogamer30',  'Photoshop'),
            ('OFREZCO', 'Enseño Python desde cero, con proyectos reales',           'pacogamer30',  'Python'),
            ('OFREZCO', 'Clases de React y hooks modernos',                         'anadev',       'React'),
            ('OFREZCO', 'Diseño interfaces en Figma, portfolio incluido',           'anadev',       'Figma'),
            ('OFREZCO', 'Explico Linux y administración de sistemas',               'luism',        'Linux'),
            ('OFREZCO', 'Introduzco Docker y contenedores desde cero',              'luism',        'Docker'),
            ('OFREZCO', 'Machine Learning aplicado con scikit-learn',               'mariadev',     'Machine Learning'),
            ('OFREZCO', 'Clases de SQL avanzado y optimización de queries',         'carlosdev',    'SQL'),
            ('OFREZCO', 'Desarrollo de APIs REST con Django',                       'carlosdev',    'Django'),
            ('OFREZCO', 'Diseño UX/UI con metodología centrada en usuario',         'sofiahm',      'Diseño UX/UI'),
            ('OFREZCO', 'Clases de guitarra eléctrica y acústica',                  'fernandor',    'Guitarra'),
            ('OFREZCO', 'Inglés conversacional con hablante nativa',                'laurasan',     'Inglés'),
            ('OFREZCO', 'Producción musical en Ableton Live',                       'jorgeperez',   'Producción Musical'),
            ('OFREZCO', 'Fotografía de retrato y paisaje urbano',                   'elenatorres',  'Fotografía'),
            ('OFREZCO', 'SEO técnico y estrategia de contenidos',                   'carmend',      'SEO'),
            ('OFREZCO', 'Copywriting persuasivo para landing pages',                'isanav',       'Copywriting'),
            ('OFREZCO', 'Piano clásico para todos los niveles',                     'luciarom',     'Piano'),
            ('OFREZCO', 'Clases de francés conversacional',                         'claudiam',     'Francés'),
            ('OFREZCO', 'Recetas de cocina mediterránea paso a paso',               'miguelf',      'Cocina'),
            ('OFREZCO', 'Estrategia de ajedrez: aperturas y finales',               'alexalonso',   'Ajedrez'),
            ('OFREZCO', 'Gestión de redes sociales y creación de contenido',        'nataliagil',   'Redes Sociales'),
            ('OFREZCO', 'Análisis de datos con Python y Pandas',                    'robertoserr',  'Python'),
            ('OFREZCO', 'Excel avanzado: tablas dinámicas y macros',                'robertoserr',  'Excel'),
            ('OFREZCO', 'JavaScript moderno (ES2023) y async/await',                'pablomoreno',  'JavaScript'),
            ('OFREZCO', 'Marketing digital: campañas en Meta y Google Ads',         'carmend',      'Marketing Digital'),
            # BUSCO
            ('BUSCO',   'Busco aprender inglés para trabajo remoto',                'pacogamer30',  'Inglés'),
            ('BUSCO',   'Quiero aprender guitarra, tengo disponibilidad por tardes', 'carlosdev',   'Guitarra'),
            ('BUSCO',   'Busco clases de piano, soy principiante total',            'davidj',       'Piano'),
            ('BUSCO',   'Quiero aprender fotografía profesional',                   'sofiahm',      'Fotografía'),
            ('BUSCO',   'Busco aprender a cocinar platos internacionales',          'laurasan',     'Cocina'),
            ('BUSCO',   'Me interesa aprender japonés desde cero',                  'alexalonso',   'Japonés'),
            ('BUSCO',   'Quiero aprender React para proyectos freelance',           'luism',        'React'),
            ('BUSCO',   'Busco aprender SEO para mi blog personal',                 'miguelf',      'SEO'),
            ('BUSCO',   'Quiero mejorar en Machine Learning avanzado',              'pablomoreno',  'Machine Learning'),
            ('BUSCO',   'Busco clases de alemán para negocios',                     'robertoserr',  'Alemán'),
            ('BUSCO',   'Quiero aprender producción musical básica',                'fernandor',    'Producción Musical'),
            ('BUSCO',   'Busco aprender Figma para mis proyectos',                  'davidj',       'Figma'),
            ('BUSCO',   'Me interesa aprender estrategia empresarial',              'nataliagil',   'Estrategia'),
            ('BUSCO',   'Quiero aprender yoga para el estrés',                      'carmend',      'Yoga'),
            ('BUSCO',   'Busco clases de Illustrator para diseño vectorial',        'nataliagil',   'Illustrator'),
            ('BUSCO',   'Quiero aprender SQL para análisis de datos',               'anadev',       'SQL'),
            ('BUSCO',   'Busco aprender copywriting para mi negocio',               'elenatorres',  'Copywriting'),
            ('BUSCO',   'Me interesa aprender Docker para mis proyectos',           'mariadev',     'Docker'),
            ('BUSCO',   'Quiero aprender ajedrez desde nivel básico',               'claudiam',     'Ajedrez'),
            ('BUSCO',   'Busco aprender francés para viajar a París',               'jorgeperez',   'Francés'),
        ]

        for tipo, descripcion, username, habilidad_nombre in publicaciones_data:
            try:
                pub, created = Publicacion.objects.get_or_create(
                    descripcion=descripcion,
                    defaults={
                        'tipo':      tipo,
                        'autor':     Usuario.objects.get(username=username),
                        'habilidad': Habilidad.objects.get(nombre=habilidad_nombre),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Post ({tipo}): {descripcion[:45]} created successfully.'))
            except Exception as error:
                self.stdout.write(self.style.ERROR(f'  ✗ Error in post "{descripcion[:40]}": {error}'))

        # AGREEMENTS
        self.stdout.write('\nCreating agreements...')

        acuerdos_data = [
            # (username_a, username_b, semanas, mins, sesiones_semana, estado, condiciones, habilidad_a, habilidad_b)
            ('pacogamer30', 'laurasan',    4, 60, 2, 'EN CURSO',   'Ejercicios semanales y vocabulario específico.', 'Photoshop',         'Inglés'),
            ('anadev',      'carlosdev',   3, 60, 2, 'EN CURSO',   'Revisión de proyectos reales en cada sesión.',   'React',             'Django'),
            ('luism',       'pablomoreno', 5, 90, 1, 'EN CURSO',   'Prácticas con servidor propio en VPS.',          'Linux',             'JavaScript'),
            ('mariadev',    'davidj',      6, 60, 2, 'EN CURSO',   'Kaggle competitions como práctica.',             'Machine Learning',  'SQL'),
            ('sofiahm',     'elenatorres', 4, 60, 1, 'EN CURSO',   'Feedback mutuo en portfolio.',                   'Figma',             'Fotografía'),
            ('jorgeperez',  'claudiam',    3, 90, 2, 'EN CURSO',   'Canciones en francés como práctica.',            'Producción Musical','Francés'),
            ('fernandor',   'miguelf',     4, 60, 1, 'EN CURSO',   'Recetas temáticas por sesión.',                  'Guitarra',          'Cocina'),
            ('carmend',     'isanav',      5, 60, 2, 'EN CURSO',   'Análisis de campañas reales semanales.',         'SEO',               'Copywriting'),
            ('luciarom',    'alexalonso',  4, 60, 1, 'EN CURSO',   'Partidas comentadas tras cada sesión.',          'Piano',             'Ajedrez'),
            ('nataliagil',  'robertoserr', 3, 60, 2, 'EN CURSO',   'Proyecto de dashboard como hilo conductor.',     'Redes Sociales',    'Python'),

            ('pacogamer30', 'anadev',      4, 60, 1, 'ACEPTADO',   'Revisión de portfolio al finalizar.',            'Python',            'React'),
            ('luism',       'mariadev',    3, 60, 2, 'ACEPTADO',   'Entorno de pruebas compartido en cloud.',        'Docker',            'Machine Learning'),
            ('carlosdev',   'davidj',      5, 90, 1, 'ACEPTADO',   'Proyecto API + frontend como resultado.',        'Django',            'Figma'),
            ('sofiahm',     'carmend',     4, 60, 2, 'ACEPTADO',   'Caso real de branding como práctica.',           'Diseño UX/UI',      'Marketing Digital'),
            ('fernandor',   'jorgeperez',  6, 60, 2, 'ACEPTADO',   'Componer una canción juntos al final.',          'Guitarra',          'Producción Musical'),
            ('elenatorres', 'nataliagil',  3, 60, 1, 'ACEPTADO',   'Shooting fotográfico para RRSS como meta.',      'Fotografía',        'Redes Sociales'),
            ('claudiam',    'alexalonso',  4, 60, 1, 'ACEPTADO',   'Literatura francesa de apertura en ajedrez.',    'Francés',           'Ajedrez'),
            ('robertoserr', 'isanav',      5, 60, 2, 'ACEPTADO',   'Newsletter conjunta como proyecto final.',       'Excel',             'Copywriting'),

            ('pablomoreno', 'luism',       3, 60, 1, 'PROPUESTO',  'Acordar horario a confirmar.',                   'React',             'Linux'),
            ('davidj',      'sofiahm',     4, 60, 2, 'PROPUESTO',  'Pendiente confirmar disponibilidad.',            'Machine Learning',  'Figma'),
            ('miguelf',     'claudiam',    3, 60, 1, 'PROPUESTO',  'Intercambio recetas+idioma, pendiente inicio.',  'Cocina',            'Francés'),
            ('luciarom',    'fernandor',   4, 90, 1, 'PROPUESTO',  'Sesiones combinadas música clásica/moderna.',    'Piano',             'Guitarra'),
            ('carmend',     'nataliagil',  5, 60, 2, 'PROPUESTO',  'Estrategia de contenido como proyecto.',         'SEO',               'Redes Sociales'),
            ('isanav',      'elenatorres', 3, 60, 1, 'PROPUESTO',  'Portafolio fotográfico con copy incluido.',      'Copywriting',       'Fotografía'),

            ('pacogamer30', 'carlosdev',   4, 60, 2, 'FINALIZADO', 'Completado con éxito. Buen intercambio.',        'Photoshop',         'Docker'),
            ('anadev',      'mariadev',    3, 60, 1, 'FINALIZADO', 'Objetivo alcanzado en todas las sesiones.',      'Figma',             'SQL'),
            ('luism',       'davidj',      5, 60, 2, 'FINALIZADO', 'Proyecto desplegado en producción.',             'Linux',             'Machine Learning'),
            ('jorgeperez',  'fernandor',   4, 90, 1, 'FINALIZADO', 'Canción compuesta y grabada juntos.',            'Producción Musical','Guitarra'),
            ('robertoserr', 'carmend',     3, 60, 2, 'FINALIZADO', 'Dashboard de métricas de marketing entregado.',  'Python',            'Marketing Digital'),

            ('sofiahm',     'luism',       3, 60, 2, 'CANCELADO',  'Cancelado por incompatibilidad de horarios.',    'Illustrator',       'Docker'),
            ('miguelf',     'alexalonso',  4, 60, 1, 'CANCELADO',  'Cancelado por cambio de prioridades.',           'Cocina',            'Estrategia'),
        ]

        acuerdos = []
        for (username_a, username_b, semanas, mins, sesiones_semana, estado, condiciones, habilidad_a, habilidad_b) in acuerdos_data:
            try:
                acuerdo, created = Acuerdo.objects.get_or_create(
                    usuario_a=Usuario.objects.get(username=username_a),
                    usuario_b=Usuario.objects.get(username=username_b),
                    habilidad_tradea_a=Habilidad.objects.get(nombre=habilidad_a),
                    habilidad_tradea_b=Habilidad.objects.get(nombre=habilidad_b),
                    defaults={
                        'semanas':             semanas,
                        'mins_sesion':         mins,
                        'sesiones_por_semana': sesiones_semana,
                        'estado':              estado,
                        'condiciones':         condiciones,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Agreement {acuerdo.id}: {username_a} ↔ {username_b} [{habilidad_a} ↔ {habilidad_b}] ({estado}) created successfully.'
                    ))
                acuerdos.append(acuerdo)
            except Exception as error:
                self.stdout.write(self.style.ERROR(f'  ✗ Error in agreement {username_a}↔{username_b}: {error}'))

        # SESSIONS
        self.stdout.write('\nCreating sessions...')

        acuerdos_en_curso = [acuerdo for acuerdo in acuerdos if acuerdo.estado == 'EN CURSO']

        plantillas_sesiones = [
            [
                (1,  60, 'Sesión introductoria: presentación y objetivos.',      True,  True),
                (8,  60, 'Práctica guiada sobre conceptos básicos.',             True,  True),
                (15, 60, 'Resolución de dudas y ejercicios propuestos.',         True,  False),
                (22, 60, 'Avance significativo, primeros resultados visibles.',  True,  True),
            ],
            [
                (2,  60, 'Primera toma de contacto y nivelación.',              True,  True),
                (9,  60, 'Profundización en conceptos intermedios.',            True,  True),
                (16, 90, 'Proyecto práctico en desarrollo.',                    False, True),
            ],
            [
                (3,  60, 'Sesión inicial con definición de roadmap.',           True,  True),
                (10, 60, 'Ejercicios aplicados con feedback.',                  True,  True),
                (17, 60, 'Revisión de avances y correcciones.',                 True,  True),
                (24, 60, 'Práctica autónoma supervisada.',                      True,  True),
                (31, 60, 'Consolidación de conocimientos adquiridos.',          True,  False),
            ],
            [
                (1,  60, 'Onboarding y acuerdo de metodología de trabajo.',     True,  True),
                (8,  60, 'Primera entrega de ejercicios revisada.',             True,  True),
                (15, 60, 'Sesión intensiva de práctica avanzada.',              True,  True),
            ],
        ]

        sesiones_creadas = 0
        for indice, acuerdo in enumerate(acuerdos_en_curso):
            plantilla = plantillas_sesiones[indice % len(plantillas_sesiones)]
            for dias_offset, duracion, resumen, asistencia_a, asistencia_b in plantilla:
                try:
                    sesion, created = Sesion.objects.get_or_create(
                        acuerdo=acuerdo,
                        fecha=date.today() + timedelta(days=dias_offset),
                        defaults={
                            'duracion_real':    duracion,
                            'resumen':          resumen,
                            'asistencia_user_a': asistencia_a,
                            'asistencia_user_b': asistencia_b,
                            'estado':           True,
                        }
                    )
                    if created:
                        sesiones_creadas += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Session {sesion.id} — Agreement {acuerdo.id} (+{dias_offset}d): {resumen[:40]} created successfully.'
                        ))
                except Exception as error:
                    self.stdout.write(self.style.ERROR(
                        f'  ✗ Error in session (Agreement {acuerdo.id}, +{dias_offset}d): {error}'
                    ))

        # SUMMARY
        self.stdout.write(self.style.SUCCESS('\n¡Database populated successfully.'))
        self.stdout.write(self.style.SUCCESS(
            f'Skills: {len(habilidades_nombres)} | '
            f'Users: {len(usuarios_data)} | '
            f'Posts: {len(publicaciones_data)} | '
            f'Agreements: {len(acuerdos_data)} | '
            f'Sessions created: {sesiones_creadas}'
        ))