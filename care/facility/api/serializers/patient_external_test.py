from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class PatientExternalTestICMRDataSerializer(serializers.Serializer):
    # local_body_object = LocalBodySerializer(source="local_body", read_only=True)
    # district_object = DistrictSerializer(source="district", read_only=True)

    srf_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    name = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    age_in = serializers.CharField(write_only=True)
    gender = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_repeat = serializers.BooleanField(write_only=True, required=False)
    patient_category = serializers.CharField(write_only=True, required=False, allow_blank=True)
    lab_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    sample_type = serializers.CharField(write_only=True, required=False, allow_blank=True)
    result = serializers.CharField(write_only=True)
    icmr_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    icmr_patient_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    contact_number_of = serializers.CharField(write_only=True, required=False, allow_blank=True)
    nationality = serializers.CharField(write_only=True, required=False, allow_blank=True)
    aadhar_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    passport_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    pincode = serializers.CharField(write_only=True, required=False, allow_blank=True)
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)
    village_town = serializers.CharField(write_only=True, required=False, allow_blank=True)
    underlying_medical_condition = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_hospitalized = serializers.BooleanField(write_only=True, required=False)
    is_repeat = serializers.BooleanField(write_only=True, required=False)
    sample_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    hospital_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    hospital_state = serializers.CharField(write_only=True, required=False, allow_blank=True)
    hospital_district = serializers.CharField(write_only=True, required=False, allow_blank=True)
    symptom_status = serializers.CharField(write_only=True, required=False, allow_blank=True)
    test_type = serializers.CharField(write_only=True, required=False, allow_blank=True)
    egene = serializers.CharField(write_only=True, required=False, allow_blank=True)
    rdrp = serializers.CharField(write_only=True, required=False, allow_blank=True)
    orf1b = serializers.CharField(write_only=True, required=False, allow_blank=True)
    remarks = serializers.CharField(write_only=True, required=False, allow_blank=True)
    state = serializers.CharField(write_only=True)
    district = serializers.CharField(write_only=True)

    sample_collection_date = serializers.DateField(input_formats=["%Y-%m-%d"], required=False)
    result_date = serializers.DateField(input_formats=["%Y-%m-%d %H-%M-%S"], required=False)

    def validate(self, data):
        data["is_hospitalized"] = False
        if data["is_hospitalized"] and "yes" in data["is_hospitalized"].lower():
            data["is_hospitalized"] = True

        data["is_repeat"] = False
        if data["is_repeat"] and "yes" in data["is_repeat"].lower():
            data["is_repeat"] = True

        # print(data.keys())
        state_obj = None

        if "state" in data:
            state = data["state"]
            state_obj = State.objects.filter(name__icontains=state).first()
            if state_obj:
                data["state"] = state_obj.id
            else:
                raise ValidationError({"state": ["State Does not Exist"]})
        else:
            raise ValidationError({"state": ["State Not Present in Data"]})

        if "district" in data:
            district = data["district"]
            district_obj = District.objects.filter(name__icontains=district, state=state_obj).first()
            if district_obj:
                data["district"] = district_obj.id
            else:
                raise ValidationError({"district": ["District Does not Exist"]})
        else:
            raise ValidationError({"district": ["District Not Present in Data"]})

        return data
