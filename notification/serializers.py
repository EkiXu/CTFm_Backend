from rest_framework import serializers
from notification.models import Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id","title","content","pub_date","type_icon")
        read_only_field = [
            "id",
            "title",
            "content",
            "pub_date",
            "type_icon"
        ]