# tablero
Core

Django sin dolor!
1- 	Crear repo en github y clonarlo de forma local
2-	Crear https://www.gitignore.io/
3-	Crear entorno vitual python
		python -m venv myvenv
4-	Iniciar el entorno virtual
		source myvenv/Scripts/activate
		deactivate
5-	Instalar Django
		3.1 Actualizar a la ultima version de pip en el entorno
				python -m pip install --upgrade pip
		3.2	Crear requirements.txt en el raiz e indicar version de Django a usar
				Django~=2.2.6
		3.3	Instalar Django
				pip install -r requirements.txt
6-	Crear proyecto
		django-admin.exe startproject mysite .
		Un proyecto tendra n aplicaciones
7- Preparar los archivos settings del project para los ambientes desa y produccion
		folder settings
		__init__.py
		file base.py
			todo menos DEBUG, ALLOWED_HOSTS, DATABASES, STATIC_URL
		file local.py
		file production.py
			DEBUG, ALLOWED_HOSTS, DATABASES, STATIC_URL
			from .base import *
		setear el entorno a correr en manage.py y wsgi.py
8-	Configurar settings.py
		ALLOWED_HOSTS = ['*']
		LANGUAGE_CODE = 'es-ar'
		TIME_ZONE = 'America/Argentina/Buenos_Aires'
9-	Crear DB
		python manage.py migrate
10-	Iniciar servidor web
		python manage.py runserver
11-	Crear una aplicación
		python manage.py startapp blog
12-	Decirle a Django que la utilice
		Agregar la entrada blog al array:
		INSTALLED_APPS = [
			'django.contrib.admin',
			'django.contrib.auth',
			'django.contrib.contenttypes',
			'django.contrib.sessions',
			'django.contrib.messages',
			'django.contrib.staticfiles',
			'blog',
		]
13- Crear modelos
		blog/models.py
			from django.db import models
			from django.utils import timezone

			class Post(models.Model):
				author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
				title = models.CharField(max_length=200)
				text = models.TextField()
				created_date = models.DateTimeField(
						default=timezone.now)
				published_date = models.DateTimeField(
						blank=True, null=True)

				def publish(self):
					self.published_date = timezone.now()
					self.save()

				def __str__(self):
					return self.title
14- Crear tablas en funcion de los modelos
		python manage.py makemigrations blog
		python manage.py migrate blog
15- Crear un super usuario
		python manage.py createsuperuser
		pass: superusuario
16- Agregar modelo al admin (blog/admin.py)
		from .models import Post
		admin.site.register(Post)
		En el caso que la DB ya esta creada con este comando creamos los modelos de forma automatica
			python manage.py inspectdb > nombreapp/models.py
16.1- Popular el modelo
		pip install Faker
		crear populate_models.py en el root
			import os, django, random

			os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nombreprojecto.settings.local")
			django.setup()

			from faker import Faker
			from nombreapp.models import Post
			from django.contrib.auth.models import User
			from django.utils import timezone

			def create_post(N):
				fake = Faker()
				for _ in range(N):
					author = User.objects.get(username='admin')
					title = fake.name()
					text = fake.text()
					published_date = timezone.now()
					Post.objects.create(author=author,title=title + " Post", text= text, published_date=published_date)

			create_post(1500)
			print("Model Post: Datos cargados correctamente")
		
		ejecutarlo con python populate_models.py
17- Subir a github
		Crear repo GIT
			git init
			git config --global user.name "Rodolfo"
			git config --global user.email rmbertolino@hotmail.com
			git status
			git add --all
			git commit -m "Commit Inicial"
		Subir Codigo
			git remote add origin https://github.com/rmbertolino/my-first-blog.git (opcional)
			git push -u origin master
18-	URLs
		Para mantener limpio el archivo, importar las urls de nuestra aplicación en el archivo principal project/urls.py
		from django.urls import path, include
		path('', include('nombreapp.urls')),
		Ahora Django redirigirá todo lo que entre a 'http://127.0.0.1:8000/' hacia nombreapp.urls y buscará más instrucciones allí.
18.1 Crear urls.py en la app
		from django.urls import path
		from . import views

		urlpatterns = [
			path('', views.post_list, name='post_list'),
		]
		De esta forma asociamos vistas a urls
19-	Vistas
		Una View es un lugar donde ponemos la "lógica" de nuestra aplicación. Pedirá información del modelo creado antes y se la pasará a la plantilla.
		def post_list(request):
			return render(request, 'indicadores/post_list.html', {})
20- Templates
		crear folder app/templates/app/post_list.html
		crear folder static con los archivos estaticos(css, img, js, vendor) de la plantilla al mismo nivel
21-	ORM
	Django shell
		(myvenv) ~/djangogirls$ python manage.py shell
	Todos los objetos
		from blog.models import Post
		Post.objects.all()
	Crear Objeto
		>>> me = User.objects.get(username='admin')
		>>> Post.objects.create(author=me, title='Sample title', text='Test')
	Filtrar objetos
		Post.objects.filter(author=me)
		Post.objects.filter(title__contains='title')
		>>> post = Post.objects.get(title="Sample title")
		>>> post.publish()
	Ordenar objetos
		Post.objects.order_by('created_date')
		Post.objects.order_by('-created_date')
	Encadenar QuerySets
		Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
22-	Datos dinámicos en plantillas
	from django.utils import timezone
	from .models import Post
	def post_list(request):
		posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
		return render(request, 'blog/post_list.html', {'posts': posts})
23-	Plantillas de Django
		en la app creada creo los folders:
			static inluyo css,img,js,vendor
			nombreapp/templates/nombreapp/ incluyo los html
			al inicio del html	{% load static %}
			en cada referencia a un file estatico {% static 'xxx' %}
24-	Extendiendo plantillas
		Plantilla base
		crear base.html e incorporar bloques para contenido dinamico
			{% block content %}

			{% endblock %}
		Luego en cada template extendemos de base.html y agregamos contenido a los bloques

***********************************************************************************************
Extender funcionalidades
1-	Agregar enlace para ver detalle del post
		<h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
2-	Agregar la url
		path('post/<int:pk>/', views.post_detail, name='post_detail'),
3- Agregar la vista
		def post_detail(request, pk):
			post = get_object_or_404(Post, pk=pk)
			return render(request, 'indicadores/post_detail.html', {'post': post})
4- Crear template
	/post_detail.html
5-	Formularios
		Vamos a crear: un enlace a la página, una dirección URL, una vista y una plantilla.
		Creamos forms.py dentro de nuestra app
			from django import forms
			from .models import Post

			class PostForm(forms.ModelForm):
				class Meta:
					model = Post
					fields = ('title', 'text',)
		Enlace a una página con el formulario
			 href="{% url 'post_new' %}"
		URL
			path('post/new', views.post_new, name='post_new'),
		Vista
			from .forms import PostForm
			def post_new(request):
				form = PostForm()
				return render(request, 'blog/post_edit.html', {'form': form})
		Template
			
		1-	Agregar mas a tu sitio web
		Eliminacion de post
2-	Asegura tu sitio
		Asegurar vistas post_new, post_edit, post_draft_list, post_remove y post_publish con decoradores
		Importar funcionalidad de login 
		from django.contrib.auth.decorators import login_required
		@login_required decorardor arriba de las views
2.1 Agregar login en root/url.py
		path('accounts/login/', views.login, name='login')
		LOGIN_REDIRECT_URL = '/' en seetings.py
3-	Crea un modelo de comentarios
		Crear model Comment
		Preparar tablas de la DB en funcion del modelo:	python manage.py makemigrations blog
		Aplicar los cambios en la DB:					python manage.py migrate blog
		Registrar el modelo en el panel admin			
		
4-	Instalacion de PostgreSQL