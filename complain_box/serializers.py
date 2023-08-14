from django.utils import timezone
from rest_framework import serializers

from author.models import User
from author.models.user_model import Designation
from .models import Complaint, Feedback, Institute, File, InstituteType, Municipality, Class, Subject, ComplainantType


class InstituteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteType
        fields = '__all__'


class InstituteSerializer(serializers.ModelSerializer):
    institute_type = InstituteTypeSerializer()

    class Meta:
        model = Institute
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    institute_set = InstituteSerializer(many=True, read_only=True)

    class Meta:
        model = Municipality
        fields = '__all__'


class MunicipalityForComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class UserForFeedBackSerializer(serializers.ModelSerializer):
    designation = DesignationSerializer()

    class Meta:
        model = User
        fields = ["salutation", "first_name", "last_name", "designation"]


class InstituteForCmplnSerializer(serializers.ModelSerializer):
    institute_type = InstituteTypeSerializer()
    municipality = MunicipalityForComplaintSerializer()

    class Meta:
        model = Institute
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ComplainantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplainantType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', "last_name"]


class ComplainedToSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, source="user_set", read_only=True)

    class Meta:
        model = Designation
        fields = ["name", "users"]


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


class DateOnlyField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if value is not None:
            return timezone.localtime(value).strftime('%d/%m/%Y')
        return None


class GetComplaintSerializer(serializers.ModelSerializer):
    institute = InstituteForCmplnSerializer()
    complained_to = ComplainedToSerializer()
    complainant_type = ComplainantTypeSerializer()
    student_class = ClassSerializer()
    subject = SubjectSerializer()
    created_at = DateOnlyField()
    updated_at = DateOnlyField()

    class Meta:
        model = Complaint
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CommonPropertiesSerializer(serializers.Serializer):
    class_list = ClassSerializer(many=True)
    subject_list = SubjectSerializer(many=True)
    complainant_type_list = ComplainantTypeSerializer(many=True)


class GetFeedbackSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserForFeedBackSerializer()
    created_at = DateOnlyField()
    updated_at = DateOnlyField()

    class Meta:
        model = Feedback
        fields = '__all__'
        ordering = ['-id']

    def get_replies(self, obj):
        replies = Feedback.objects.filter(parent=obj).order_by("id")
        return GetFeedbackSerializer(replies, many=True).data


class SmsSerializer(serializers.Serializer):
    to = serializers.CharField(max_length=100)  # for list of phone user # to = '+88017xxxxxxx,+88016xxxxxxxx'
    message = serializers.CharField()
