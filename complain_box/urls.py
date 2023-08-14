from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import ComplaintViewSet, GetComplaint, FileUploadViewSet, GetMunicipalityViewSet, GetInstituteTypeViewSet, \
    GetClassViewSet, GetCommonDataAPIView, UpdateComplaintStatus, FeedbackViewSet, FeedbackByComplaintViewSet, \
    SendSmsView

router = DefaultRouter()
router.register(r'get-class', GetClassViewSet)
router.register(r'get-municipality', GetMunicipalityViewSet)
router.register(r'get-institute-type', GetInstituteTypeViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'get-complaints', GetComplaint)
router.register(r'upload', FileUploadViewSet)
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/get-common-property/', GetCommonDataAPIView.as_view(), name='common-property-api'),
    path('v1/complaints/<int:complaint_id>/update_status/', UpdateComplaintStatus.as_view(),
         name='update-complaint-status'),
    path('v1/feedback/complaint/<int:complaint_id>/', FeedbackByComplaintViewSet.as_view({'get': 'list'}),
         name='feedback-by-complaint'),
    path('v1/send-sms/', SendSmsView.as_view(), name='send-sms'),
]
