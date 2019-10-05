import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tablero.settings.local")
django.setup()

from faker import Faker
from indicadores.models import Post
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

create_post(3000)
print("Model Post: Datos cargados correctamente")