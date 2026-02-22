from django.contrib import admin
from .models import Profile, Project, ContactMessage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'created_at')
    
   
    search_fields = ('title', 'tech_stack')
    
    list_filter = ('created_at',)
    
    prepopulated_fields = {'slug': ('title',)}
    
    ordering = ('-created_at',)

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp')
    search_fields = ('name', 'email')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',) 

admin.site.register(Profile)