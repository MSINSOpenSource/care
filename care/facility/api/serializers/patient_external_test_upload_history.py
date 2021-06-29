from rest_framework import serializers


class PatientExternalTestUploadHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    file_name = serializers.CharField(read_only=True)
    hash = serializers.CharField(read_only=True)
    uploaded_by = serializers.CharField(source="uploaded_by.username", read_only=True)
    most_recent_date_of_sample_tested_in_file = serializers.DateTimeField(read_only=True)
