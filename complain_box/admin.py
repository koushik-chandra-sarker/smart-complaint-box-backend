from django.contrib import admin
from .models import Municipality, InstituteType, Institute, ComplainantType, Class, Subject, Complaint, \
    Feedback, File


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')


class InstituteInline(admin.TabularInline):
    model = Institute
    extra = 1


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class InstituteTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [InstituteInline]


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'institute_type', 'municipality')
    search_fields = ('name', 'address')
    list_filter = ('municipality', 'institute_type')


class ComplainantTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'id')
    search_fields = ('name',)
    list_editable = ['priority']


class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'id',)
    search_fields = ('name',)
    list_editable = ['priority']


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'id',)
    search_fields = ('name',)
    list_editable = ['priority']


class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'complained_to', 'complainant_name', 'complainant_phone', 'complainant_email', 'status',
        'created_at', 'updated_at')
    search_fields = ('title', 'complainant_name', 'complainant_phone', 'complainant_email')
    list_filter = ('status', 'institute', 'complained_to', 'complainant_type', 'student_class', 'subject')
    # raw_id_fields = ('complainant_type', )
    readonly_fields = ('id',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('complain', 'user')
    search_fields = ('complain__title', 'user__username')
    raw_id_fields = ('complain', 'user')
    autocomplete_fields = ('complain', 'user')
    readonly_fields = ('id',)


# Register the models and their respective admin classes
admin.site.register(File, FileAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(InstituteType, InstituteTypeAdmin)
admin.site.register(Institute, InstituteAdmin)

admin.site.register(ComplainantType, ComplainantTypeAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Feedback, FeedbackAdmin)
