import uuid

from fastapi import APIRouter, Body
from sqlalchemy import and_

from api.db.models import DiscountCodes

router = APIRouter()


@router.post("/{brand_pk}/discount/generate")
async def generate(brand_pk: int, count: int = Body(..., embed=True)):
    """
    Endpoint for generation discount codes for specific brand. If number of codes is ot specified, generates 1 code.

    :param brand_pk: PK of a Brand in Brands Table.
    :param count: A number of codes needed to be generated.
    :return:
    """

    codes = []
    if not count:
        count = 1

    for c in range(count):
        code = str(uuid.uuid4())
        await DiscountCodes(brand_id=brand_pk, code=code).create()
        codes.append(code)

    return {"discount_codes": codes}


@router.get("/{brand_pk}/discount/fetch")
async def fetch(brand_pk: int, user_id: int):
    """
    Endpoint for fetching available discount code for specific brand for user. Discount code is available if no user_id
    specified for the code.

    :param brand_pk: PK of a Brand in Brands Table.
    :param user_id: PK of a User in Users Table.
    :return:
    """

    available_code = await DiscountCodes.query.where(
        and_(DiscountCodes.brand_id == brand_pk, DiscountCodes.user_id.is_(None))).gino.first()
    if available_code:
        available_code.user_id = user_id
        await available_code.apply_updates()
        return {"found": True, "discount_code": available_code.code}

    return {"found": False, "discount_code": None}
