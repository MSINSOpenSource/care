from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from care.facility.models import PatientExternalTest
from care.users.models import State, District, Ward, LocalBody, REVERSE_LOCAL_BODY_CHOICES
from care.users.api.serializers.lsg import (
    DistrictSerializer,
    LocalBodySerializer,
    StateSerializer,
    WardSerializer,
)


class PatientExternalTestSerializer(serializers.ModelSerializer):
    ward_object = WardSerializer(source="ward", read_only=True)
    local_body_object = LocalBodySerializer(source="local_body", read_only=True)
    district_object = DistrictSerializer(source="district", read_only=True)

    local_body_type = serializers.CharField(required=False, write_only=True)

    sample_collection_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    result_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)

    def validate_empty_values(self, data, *args, **kwargs):
        # if "is_repeat" in data:
        #     is_repeat = data["is_repeat"]
        #     if is_repeat.lower() == "yes":
        #         data["is_repeat"] = True
        #     else:
        #         data["is_repeat"] = False
        district_obj = None
        if "district" in data:
            district = data["district"]
            district_obj = District.objects.filter(name__icontains=district).first()
            if district_obj:
                data["district"] = district_obj.id
            else:
                raise ValidationError({"district": ["District Does not Exist"]})
        else:
            raise ValidationError({"district": ["District Not Present in Data"]})

        if "local_body_type" not in data:
            raise ValidationError({"local_body_type": ["local_body_type is not present in data"]})

        if not data["local_body_type"]:
            raise ValidationError({"local_body_type": ["local_body_type cannot be empty"]})

        if data["local_body_type"].lower() not in REVERSE_LOCAL_BODY_CHOICES:
            raise ValidationError({"local_body_type": ["Invalid Local Body Type"]})

        local_body_type = REVERSE_LOCAL_BODY_CHOICES[data["local_body_type"].lower()]

        local_body_obj = None
        if "local_body" in data and district_obj:
            if not data["local_body"]:
                raise ValidationError({"local_body": ["Local Body Cannot Be Empty"]})
            local_body = data["local_body"]
            local_body_obj = LocalBody.objects.filter(
                name__icontains=local_body, district=district_obj, body_type=local_body_type,
            ).first()
            if local_body_obj:
                data["local_body"] = local_body_obj.id
            else:
                raise ValidationError({"local_body": ["Local Body Does not Exist"]})
        else:
            raise ValidationError({"local_body": ["Local Body Not Present in Data"]})

        if "ward" in data and local_body_obj:
            try:
                int(data["ward"])
            except Exception:
                raise ValidationError({"ward": ["Ward must be an integer value"]})
            if data["ward"]:
                ward_obj = Ward.objects.filter(number=data["ward"], local_body=local_body_obj).first()
                if ward_obj:
                    data["ward"] = ward_obj.id
                else:
                    raise ValidationError({"ward": ["Ward Does not Exist"]})

        del data["local_body_type"]

        return super().validate_empty_values(data, *args, **kwargs)

    # def validate_ward(self, value):
    #     print(value)

    class Meta:
        model = PatientExternalTest
        fields = "__all__"

class ListPatientExternalTestICMRDataSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            PatientExternalTest.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)
        
        return result

class PatientExternalTestICMRDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    srf_id = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    age_in = serializers.CharField()
    gender = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)
    patient_category = serializers.CharField(required=False, allow_blank=True)
    lab_name = serializers.CharField(required=False, allow_blank=True)
    sample_type = serializers.CharField(required=False, allow_blank=True)
    result = serializers.CharField()
    icmr_id = serializers.CharField(required=False, allow_blank=True)
    icmr_patient_id = serializers.CharField(required=False, allow_blank=True)
    contact_number_of = serializers.CharField(required=False, allow_blank=True)
    nationality = serializers.CharField(required=False, allow_blank=True)
    aadhar_number = serializers.CharField(required=False, allow_blank=True)
    passport_number = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    village_town = serializers.CharField(required=False, allow_blank=True)
    underlying_medical_condition = serializers.CharField(required=False, allow_blank=True)

    sample_id = serializers.CharField(required=False, allow_blank=True)
    hospital_name = serializers.CharField(required=False, allow_blank=True)
    hospital_state = serializers.CharField(required=False, allow_blank=True)
    hospital_district = serializers.CharField(required=False, allow_blank=True)
    symptom_status = serializers.CharField(required=False, allow_blank=True)
    test_type = serializers.CharField(required=False, allow_blank=True)
    egene = serializers.CharField(required=False, allow_blank=True)
    rdrp = serializers.CharField(required=False, allow_blank=True)
    orf1b = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)
    state_id = serializers.IntegerField()
    district_id = serializers.IntegerField()

    is_hospitalized = serializers.BooleanField()
    is_repeat = serializers.BooleanField()

    sample_collection_date = serializers.DateField(input_formats=["%Y-%m-%d %H:%M:%S"], required=False)
    sample_received_date = serializers.DateTimeField(
        required=False, input_formats=["%Y-%m-%d %H:%M:%S"])
    entry_date = serializers.DateTimeField(required=False, input_formats=["%Y-%m-%d %H:%M:%S"])
    hospitalization_date = serializers.CharField(required=False, allow_blank=True)
    date_of_sample_tested = serializers.DateTimeField(
        required=False, input_formats=["%Y-%m-%d %H:%M:%S"])
    confirmation_date = serializers.CharField(required=False, write_only=True, allow_blank=True)
    confirmation_date = serializers.DateTimeField(read_only=True)

    def validate_hospitalization_date(self, date):
        if "N/A" in date:
            return None
        elif date:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return None

    def validate_confirmation_date(self, date):
        if "N/A" in date:
            return None
        elif date:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return None

    def validate(self, data):
        if "state_id" not in data:
            raise ValidationError({"state": ["State Does not Exist"]})

        if "district_id" not  in data:
            raise ValidationError({"district": ["District Does not Exist"]})

        return data
    
    def create(self, validated_data):
        return PatientExternalTest(**validated_data)
    
    class Meta:
        list_serializer_class = ListPatientExternalTestICMRDataSerializer
