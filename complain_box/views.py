from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, status
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author.models import User
from .models import Complaint, File, Municipality, InstituteType, Class, Subject, ComplainantType, Feedback
from .serializers import ComplaintSerializer, GetComplaintSerializer, FileUploadSerializer, MunicipalitySerializer, \
    InstituteTypeSerializer, CommonPropertiesSerializer, FeedbackSerializer, GetFeedbackSerializer, SmsSerializer
from .sms import send_sms


class GetCommonDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        classes = Class.objects.all().order_by("-priority")
        subjects = Subject.objects.all().order_by("-priority")
        complainant_types = ComplainantType.objects.all().order_by("-priority")

        serializer = CommonPropertiesSerializer({
            'class_list': classes,
            'subject_list': subjects,
            "complainant_type_list": complainant_types
        })

        return Response(serializer.data)


class GetClassViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Class.objects.all().order_by("-priority")
    serializer_class = InstituteTypeSerializer


class GetMunicipalityViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class GetInstituteTypeViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = InstituteType.objects.all()
    serializer_class = InstituteTypeSerializer


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer


class ComplaintViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer


class GetComplaint(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Complaint.objects.all()
    serializer_class = GetComplaintSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'created_at']
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Complaint.objects.all()
        else:
            queryset = Complaint.objects.filter(complained_to=user.designation)
        ordering = self.request.query_params.get('ordering', None)
        if ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        return queryset


class UpdateComplaintStatus(APIView):
    def patch(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
        except Complaint.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status is None:
            return Response({'error': 'Status field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        complaint.status = new_status
        complaint.save()

        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data)


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (not self.request.user.is_superuser) and (self.request.user != instance.user):
            raise PermissionDenied("Unauthorized to access this feedback.")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Unauthorized to access feedback list.")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Ensure the user is the one assigned as complained_to
        if not self.request.user.is_superuser and self.request.user.designation != serializer.validated_data[
            'complain'].complained_to:
            return Response({'detail': 'You are not authorized to provide feedback for this complaint.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedbackByComplaintViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GetFeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        complaint_id = self.kwargs['complaint_id']
        if user.is_superuser:
            queryset = Feedback.objects.filter(complain_id=complaint_id, parent=None).order_by("-id")
        else:
            queryset = Feedback.objects.filter(user=user, complain_id=complaint_id, parent=None).order_by("-id")

        # Fetch the parent feedback instances (main feedback) and prefetch related replies
        queryset = queryset.prefetch_related('replies')

        return queryset


class SendSmsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SmsSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            response = send_sms(validated_data["to"], validated_data["message"])
            if response.status_code == 200:
                response_data = {
                    'message': 'Message sent successful',
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response({'message': 'Message sent successful'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
