from django.contrib import admin

from .models import Museo, MuseoSeleccionado, Comentario, Css

admin.site.register(Museo)
admin.site.register(MuseoSeleccionado)
admin.site.register(Comentario)
admin.site.register(Css)
