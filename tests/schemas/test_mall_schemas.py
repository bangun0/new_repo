import pytest
from pydantic import ValidationError

from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    GoodsNoDawnDTO,
    MallApiReturnDTO,
    MallApiDeliveryDTO,
    GoodsDTO
)

# --- GoodsReturnRequestDTO Tests ---
def test_goods_return_request_dto_valid():
    data = {"invoiceNumber": "INV12345"}
    dto = GoodsReturnRequestDTO(**data)
    assert dto.invoiceNumber == data["invoiceNumber"]

def test_goods_return_request_dto_missing_invoice():
    with pytest.raises(ValidationError):
        GoodsReturnRequestDTO(**{})

# --- GoodsNoDawnDTO Tests ---
def test_goods_no_dawn_dto_valid():
    data = {
        "deliveryAddress": "123 Main St",
        "deliveryName": "John Doe",
        "deliveryPhone": "555-1234",
        "mallName": "MyMall",
        "childrenMallId": "ChildMall01",
        "deliveryAddressEng": "123 Main St",
        "deliveryMessage": "Leave at front door",
        "deliveryPostal": "90210",
        "deliveryTel": "555-5678",
        "goodsName": "Widget",
        "invoiceNumber": "INVWIDGET001",
        "invoicePrintYn": "Y",
        "optionName": "Blue",
        "orderNumber": "ORD001",
        "quantity": 2,
        "reserveDt": "2024-01-15"
    }
    dto = GoodsNoDawnDTO(**data)
    assert dto.deliveryAddress == data["deliveryAddress"]
    assert dto.deliveryName == data["deliveryName"]
    assert dto.deliveryPhone == data["deliveryPhone"]
    assert dto.mallName == data["mallName"]
    assert dto.quantity == 2

def test_goods_no_dawn_dto_missing_required():
    data = {"deliveryAddress": "123 Main St", "deliveryName": "John Doe"} # Missing phone and mallName
    with pytest.raises(ValidationError) as excinfo:
        GoodsNoDawnDTO(**data)
    errors = excinfo.value.errors()
    assert any(e['loc'] == ('deliveryPhone',) for e in errors)
    assert any(e['loc'] == ('mallName',) for e in errors)


def test_goods_no_dawn_dto_defaults():
    data = {
        "deliveryAddress": "123 Main St",
        "deliveryName": "John Doe",
        "deliveryPhone": "555-1234",
        "mallName": "MyMall",
    }
    dto = GoodsNoDawnDTO(**data)
    assert dto.invoicePrintYn == "N" # Default value

# --- MallApiReturnDTO Tests ---
def test_mall_api_return_dto_valid():
    goods_data = {
        "deliveryAddress": "Return St", "deliveryName": "Jane Return", 
        "deliveryPhone": "555-return", "mallName": "ReturnMall"
    }
    data = {"goodsList": [goods_data]}
    dto = MallApiReturnDTO(**data)
    assert len(dto.goodsList) == 1
    assert dto.goodsList[0].deliveryName == "Jane Return"

def test_mall_api_return_dto_missing_goods_list():
    with pytest.raises(ValidationError):
        MallApiReturnDTO(**{})

def test_mall_api_return_dto_empty_goods_list():
    # goodsList is required, but can be an empty list
    data = {"goodsList": []}
    dto = MallApiReturnDTO(**data)
    assert len(dto.goodsList) == 0
    
def test_mall_api_return_dto_invalid_item_in_list():
    data = {
        "goodsList": [
            {"deliveryAddress": "Valid Addr", "deliveryName": "Valid Name", "deliveryPhone": "Valid Phone", "mallName": "Valid Mall"},
            {"deliveryName": "Incomplete Item"} # Missing required fields for GoodsNoDawnDTO
        ]
    }
    with pytest.raises(ValidationError):
        MallApiReturnDTO(**data)

# --- MallApiDeliveryDTO Tests ---
def test_mall_api_delivery_dto_valid():
    goods_data = {
        "deliveryAddress": "Deliver St", "deliveryName": "John Deliver", 
        "deliveryPhone": "555-deliver", "mallName": "DeliverMall"
    }
    data = {"dawnDelivery": "Y", "goodsList": [goods_data]}
    dto = MallApiDeliveryDTO(**data)
    assert dto.dawnDelivery == "Y"
    assert len(dto.goodsList) == 1
    assert dto.goodsList[0].mallName == "DeliverMall"

def test_mall_api_delivery_dto_optional_dawn_delivery():
    goods_data = {
        "deliveryAddress": "Deliver St", "deliveryName": "John Deliver", 
        "deliveryPhone": "555-deliver", "mallName": "DeliverMall"
    }
    data = {"goodsList": [goods_data]} # dawnDelivery is optional
    dto = MallApiDeliveryDTO(**data)
    assert dto.dawnDelivery is None # Default value is None

# --- GoodsDTO Tests ---
def test_goods_dto_valid():
    data = {
        "deliveryAddress": "456 Oak Ave",
        "deliveryName": "Jane Smith",
        "deliveryPhone": "555-8765",
        "mallName": "SuperMall",
        "dawnDelivery": "Y", # Specific to GoodsDTO
        "childrenMallId": "ChildMall02",
        "invoiceNumber": "INVGOODS002"
    }
    dto = GoodsDTO(**data)
    assert dto.deliveryAddress == data["deliveryAddress"]
    assert dto.dawnDelivery == "Y"
    assert dto.invoiceNumber == data["invoiceNumber"]

def test_goods_dto_missing_required():
    data = {"deliveryAddress": "456 Oak Ave", "dawnDelivery": "N"} # Missing name, phone, mallName
    with pytest.raises(ValidationError) as excinfo:
        GoodsDTO(**data)
    errors = excinfo.value.errors()
    required_fields = {'deliveryName', 'deliveryPhone', 'mallName'}
    missing_fields = {e['loc'][0] for e in errors}
    assert required_fields.issubset(missing_fields)

def test_goods_dto_inherits_defaults():
    data = {
        "deliveryAddress": "456 Oak Ave",
        "deliveryName": "Jane Smith",
        "deliveryPhone": "555-8765",
        "mallName": "SuperMall",
    }
    dto = GoodsDTO(**data)
    assert dto.invoicePrintYn == "N" # Default from GoodsNoDawnDTO (implicitly, as GoodsDTO has same fields)
    assert dto.dawnDelivery is None # Optional field in GoodsDTO
