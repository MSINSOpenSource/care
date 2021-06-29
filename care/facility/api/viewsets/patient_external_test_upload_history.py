from rest_framework import status
from rest_framework.mixins import  ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from care.facility.api.serializers.patient_external_test_upload_history import (
    PatientExternalTestUploadHistorySerializer
)
from care.facility.models import PatientExternalTestUploadHistory


class PatientExternalTestUploadHistoryViewSet(
    RetrieveModelMixin, ListModelMixin, GenericViewSet,
):
    serializer_class = PatientExternalTestUploadHistorySerializer
    queryset = PatientExternalTestUploadHistory.objects.select_related("uploaded_by").all().order_by("-id")
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(uploaded_by=request.user).order_by("-created_date")
        serializer = PatientExternalTestUploadHistorySerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        