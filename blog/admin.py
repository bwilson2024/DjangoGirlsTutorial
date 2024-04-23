from django.contrib import admin
from .models import Post,Person,Meditation,Journaling

admin.site.register(Post)
admin.site.register(Person)
admin.site.register(Meditation)
admin.site.register(Journaling)