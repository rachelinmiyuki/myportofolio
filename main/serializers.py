from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    project_type_display = serializers.CharField(
        source="get_project_type_display",
        read_only=True
    ) # untuk project type display yang diambil dari model

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "project_type", "project_type_display",
            "thumbnail", "tag1", "tag2", "tag3", "tag4", "detail_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value): #setara dengan clean_title di ProjectForm
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tag1(self, value):
        return strip_tags(value)

    def validate_tag2(self, value):
            return strip_tags(value)

    def validate_tag3(self, value):
            return strip_tags(value)

    def validate_tag4(self, value):
            return strip_tags(value)
    
    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj): 
        #memakai request agar hasilnya sesuai akun yang sedang melihat, dan menghasilkan False jika tidak ada request atau belum login.
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())