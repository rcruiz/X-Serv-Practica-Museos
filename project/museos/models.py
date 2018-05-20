from django.db import models

class Museo(models.Model):
    nombre = models.CharField(max_length=128)
    url = models.URLField()
    direccion = models.CharField(max_length=256)
    latitud = models.FloatField()
    longitud = models.FloatField()
    descripcion = models.TextField()
    horario = models.CharField(max_length=256)
    busMetro = models.CharField(max_length=256)
    accesible = models.BooleanField(default=False)
    barrio = models.CharField(max_length=64)
    distrito = models.CharField(max_length=32)
    email = models.EmailField(max_length=128,default = "")
    tlfno = models.CharField(max_length = 12)
    ncomment = models.IntegerField(default = 0)

class MuseoSeleccionado(models.Model):
    fecha = models.DateTimeField(auto_now_add=True) # (auto_now=True)
    usuario = models.CharField(max_length = 32)
    museo = models.ForeignKey(Museo)

class Comentario(models.Model):
    contenido = models.TextField(default="")
    fecha = models.DateField(auto_now_add=True)
    usuario = models.CharField(max_length = 32)
    museo = models.ForeignKey(Museo)

class Css(models.Model):
    usuario = models.CharField(max_length = 32)
    titulo = models.CharField(max_length = 32)
    tamLetra = models.IntegerField(default=12)
    colorFondo = models.CharField(max_length = 32, default='#efefef')
