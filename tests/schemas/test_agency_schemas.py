import pytest
from pydantic import ValidationError

from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeSaveDTO,
    PostalCodeListDTO
)

def test_auth_agency_dto_valid():
    data = {"accessKey": "key123", "nonce": "nonce123", "timestamp": "2023-01-01T12:00:00Z"}
    dto = AuthAgencyDTO(**data)
    assert dto.accessKey == data["accessKey"]
    assert dto.nonce == data["nonce"]
    assert dto.timestamp == data["timestamp"]

def test_auth_agency_dto_optional_fields():
    dto = AuthAgencyDTO() # All fields are optional
    assert dto.accessKey is None
    assert dto.nonce is None
    assert dto.timestamp is None

def test_delivery_agency_update_consign_dto_valid():
    data = {"extOrderId": "order1", "invoiceNumber": "inv123", "status": "updated"}
    dto = DeliveryAgencyUpdateConsignDTO(**data)
    assert dto.extOrderId == data["extOrderId"]
    assert dto.invoiceNumber == data["invoiceNumber"]
    assert dto.status == data["status"]

def test_delivery_invoice_number_dto_valid():
    data = {"invoiceNumber": "inv123"}
    dto = DeliveryInvoiceNumberDTO(**data)
    assert dto.invoiceNumber == data["invoiceNumber"]

def test_delivery_agency_flex_list_update_dto_valid():
    data = {"invoiceNumberList": ["inv123", "inv456"]}
    dto = DeliveryAgencyFlexListUpdateDTO(**data)
    assert dto.invoiceNumberList == data["invoiceNumberList"]

def test_delivery_agency_state_update_dto_valid():
    data = {"holdCode": "H01", "imgUrl": "http://example.com/img.png", "invoiceNumber": "inv789", "status": "pending"}
    dto = DeliveryAgencyStateUpdateDTO(**data)
    assert dto.holdCode == data["holdCode"]
    assert dto.imgUrl == data["imgUrl"]
    assert dto.invoiceNumber == data["invoiceNumber"]
    assert dto.status == data["status"]

# --- PostalCodeSaveDTO Tests ---
def test_postal_code_save_dto_valid():
    data = {
        "postNumber": "12345", 
        "sido": "서울", 
        "gugun": "강남구", 
        "possibleArea": "Y",
        "buildingCode": "bldg1", "buildingName": "빌딩", "legalDongCode": "dong1",
        "roadCode": "road1", "roadName": "강남대로", "deliveryGroup": "A",
        "adminDong": "역삼동", "legalDong": "역삼1동"
    }
    dto = PostalCodeSaveDTO(**data)
    assert dto.postNumber == "12345"
    assert dto.sido == "서울"
    assert dto.gugun == "강남구"
    assert dto.possibleArea == "Y"
    assert dto.buildingName == "빌딩"

def test_postal_code_save_dto_missing_required():
    data = {"sido": "서울", "gugun": "강남구"} # Missing postNumber, possibleArea
    with pytest.raises(ValidationError):
        PostalCodeSaveDTO(**data)

def test_postal_code_save_dto_invalid_possible_area():
    # Assuming possibleArea should be 'Y' or 'N', though not explicitly validated by Pydantic type yet
    # This test is more about structure. Specific enum validation could be added to schema.
    data = {"postNumber": "12345", "sido": "서울", "gugun": "강남구", "possibleArea": "Maybe"}
    dto = PostalCodeSaveDTO(**data) # Pydantic will accept any string for possibleArea
    assert dto.possibleArea == "Maybe" 

# --- PostalCodeListDTO Tests ---
def test_postal_code_list_dto_valid():
    save_data_1 = {"postNumber": "12345", "sido": "서울", "gugun": "강남구", "possibleArea": "Y"}
    save_data_2 = {"postNumber": "54321", "sido": "경기", "gugun": "분당구", "possibleArea": "N"}
    data = {
        "dawnDelivery": "Y",
        "postNumberSaveList": [save_data_1, save_data_2]
    }
    dto = PostalCodeListDTO(**data)
    assert dto.dawnDelivery == "Y"
    assert len(dto.postNumberSaveList) == 2
    assert dto.postNumberSaveList[0].postNumber == "12345"
    assert dto.postNumberSaveList[1].gugun == "분당구"

def test_postal_code_list_dto_missing_required_list():
    data = {"dawnDelivery": "N"} # Missing postNumberSaveList
    with pytest.raises(ValidationError):
        PostalCodeListDTO(**data)
        
def test_postal_code_list_dto_empty_list_allowed():
    # The field postNumberSaveList is required, but it can be an empty list.
    data = {"postNumberSaveList": []}
    dto = PostalCodeListDTO(**data)
    assert dto.dawnDelivery == "N" # Checks default value
    assert len(dto.postNumberSaveList) == 0

def test_postal_code_list_dto_invalid_item_in_list():
    data = {
        "postNumberSaveList": [
            {"postNumber": "12345", "sido": "서울", "gugun": "강남구", "possibleArea": "Y"},
            {"sido": "경기", "gugun": "분당구"} # Missing required fields for PostalCodeSaveDTO
        ]
    }
    with pytest.raises(ValidationError):
        PostalCodeListDTO(**data)
