from django.db import models

from care.facility.models import FacilityBaseModel, PatientRegistration, pretty_boolean
from care.users.models import User, Ward, LocalBody, District, State


class PatientExternalTest(FacilityBaseModel):
    srf_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=1000)
    age = models.IntegerField()
    age_in = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    mobile_number = models.CharField(max_length=15)
    is_repeat = models.BooleanField()
    patient_status = models.CharField(max_length=15, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    local_body = models.ForeignKey(
        LocalBody, on_delete=models.PROTECT, null=True, blank=True
    )
    district = models.ForeignKey(
        District, on_delete=models.PROTECT, null=False, blank=False
    )
    source = models.CharField(max_length=255, blank=True, null=True)
    patient_category = models.CharField(max_length=255, blank=True, null=True)
    lab_name = models.CharField(max_length=255)
    test_type = models.CharField(max_length=255)
    sample_type = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    sample_collection_date = models.DateField(blank=True, null=True)
    result_date = models.DateField(blank=True, null=True)

    # icmr attributes
    icmr_id = models.CharField(max_length=255, blank=True, null=True)
    icmr_patient_id = models.CharField(max_length=255, blank=True, null=True)
    contact_number_of = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    aadhar_number = models.CharField(max_length=255, blank=True, null=True)
    passport_number = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(
        State, on_delete=models.PROTECT, null=False, blank=False
    )
    village_town = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)
    sample_received_date = models.DateField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    sample_id = models.CharField(max_length=255, blank=True, null=True)
    underlying_medical_condition = models.CharField(max_length=255, blank=True, null=True)
    is_hospitalized = models.BooleanField(blank=True)
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    hospitalization_date = models.DateField(blank=True, null=True)
    hospital_state = models.CharField(max_length=255, blank=True, null=True)
    hospital_district = models.CharField(max_length=255, blank=True, null=True)
    testing_kit_used = models.CharField(max_length=255, blank=True, null=True)
    symptom_status = models.CharField(max_length=255, blank=True, null=True)
    symptoms = models.CharField(max_length=255, blank=True, null=True)
    egene = models.CharField(max_length=255, blank=True, null=True)
    rdrp = models.CharField(max_length=255, blank=True, null=True)
    orf1b = models.CharField(max_length=255, blank=True, null=True)
    is_repeat_sample = models.CharField(max_length=255, blank=True, null=True)
    confirmation_date = models.DateField(blank=True, null=True)
    date_of_sample_tested = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    CSV_MAPPING = {
        "id": "Care External Result ID",
        "name": "Patient Name",
        "age": "Age",
        "age_in": "Age In",
        "result": "Final Result",
        "srf_id": "SRF-ID",
        "gender": "Gender",
        "address": "Patient Address",
        "district__name": "District",
        "local_body__name": "LSGD",
        "ward__name": "Ward Name",
        "ward__number": "Ward Number",
        "mobile_number": "Contact Number",
        "is_repeat": "Is Repeat",
        "patient_status": "Patient Status",
        "sample_type": "Sample Type",
        "test_type": "Testing Kit Used",
        "sample_collection_date": "Sample Collection Date",
        "result_date": "Result Date",
        "lab_name": "LabName",
        "source": "Source",
        "patient_category": "Patient Category",
    }

    CSV_MAKE_PRETTY = {"is_repeat": pretty_boolean}

    HEADER_CSV_MAPPING = {
        "srf_id": "SRF-ID",
        "name": "Patient Name",
        "age": "Age",
        "age_in": "Age In",
        "gender": "Gender",
        "address": "Patient Address",
        "mobile_number": "Contact Number",
        "is_repeat": "Is Repeat",
        "patient_status": "Patient Status",
        "ward": "Ward",
        "district": "District",
        "result_date": "Result Date",
        "local_body": "LSGD",
        "local_body_type": "LSGD Type",
        "lab_name": "LabName",
        "test_type": "Testing Kit Used",
        "sample_type": "Sample Type",
        "result": "Final Result",
        "sample_collection_date": "Sample Collection Date",
        "source": "Source"
        # "result_date": "",
    }

    ICMR_EXCEL_HEADER_KEY_MAPPING = {
        "SRF ID": "srf_id",
        "Patient Name": "name",
        "Age":"age",
        "Age In": "age_in",
        "Gender": "gender",
        "Address": "address",
        "Contact Number": "mobile_number",
        "Patient Category": "patient_category",
        "Laboratory Name": "lab_name",
        "Sample Type": "sample_type",
        "Final Result Sample": "result",
        "Icmr ID": "icmr_id",
        "Patient ID": "icmr_patient_id",
        "Contact Number Belongs To": "contact_number_of",
        "Nationality": "nationality",
        "Aadhar Card Number": "aadhar_number",
        "Passport Number": "passport_number",
        "Pin Code": "pincode",
        "Village Town": "village_town",
        "Underlying Medical Condition": "underlying_medical_condition",
        "Sample ID": "sample_id",
        "Hospital Name": "hospital_name",
        "Hospital State": "hospital_state",
        "Hospital District": "hospital_district",
        "Symptoms Status": "symptom_status",
        "symptoms": "symptoms",
        "Testing Kit Used": "test_type",
        "Egene": "egene",
        "RDRP": "rdrp",
        "ORF1B": "orf1b",
        "Remarks": "remarks",
        "State of Residence": "state",
        "District of Residence": "district",
        "Hospitalized": "is_hospitalized",
        "Repeat Sample": "is_repeat",

        # date fields
        "Date of Sample Collection": "sample_collection_date",
        "Date of Sample Received": "sample_received_date",
        "Entry Date": "entry_date",
        "Hospitalization Date": "hospitalization_date",
        "Date of Sample Tested": "date_of_sample_tested",
        "Confirmation Date": "confirmation_date",
    }
