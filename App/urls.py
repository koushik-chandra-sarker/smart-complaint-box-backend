
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from App.views import root_redirect

admin.site.site_header = "SCB Administration"
admin.site.site_title = "Smart Complaint Boxe"
admin.site.index_title = "Smart Complaint Box"

urlpatterns = [
                  path('', root_redirect, name='root_redirect'),
                  path('admin/', admin.site.urls),
                  path('api/author/', include('author.urls')),
                  path('api/complaint-box/', include('complain_box.urls')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
