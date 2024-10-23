from rest_framework import serializers

from apps.divar.models import Landing


class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)


class ExtraDataSerializer(serializers.Serializer):
    location = LocationSerializer(allow_null=True, required=False)

class DivarUserSerializer(serializers.Serializer):
    id = serializers.CharField()

class InitSessionFromChatSerializer(serializers.Serializer):
    extra_data = ExtraDataSerializer(required=False)
    callback_url = serializers.CharField()
    post_token = serializers.CharField()
    user_id = serializers.CharField()
    peer_id = serializers.CharField()
    supplier = DivarUserSerializer()
    demand = DivarUserSerializer()

class InitSessionV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Landing
        fields = ("return_url", "source", "post_token", "conversation_id", "user_side", "extra_data")
