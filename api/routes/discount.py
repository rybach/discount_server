import uuid
from fastapi import Request

from fastapi import Response, APIRouter, Body, status
from sqlalchemy import and_

from api.db.models import DiscountCodes

router = APIRouter()


@router.post("/{brand_id}/discount/generate")
async def generate(request: Request, response: Response, brand_id: int, count: int = Body(..., embed=True)):
    """
    Endpoint for generation discount codes for specific brand. If number of codes is ot specified, generates 1 code.

    :param response: Response parameter for access response information.
    :param request: Request parameter for access application configuration.
    :param brand_id: PK of a Brand in Brands Table.
    :param count: A number of codes needed to be generated.
    :return:
    """

    codes = []
    app_config = request.app.config
    if count > app_config.max_codes_per_request:
        response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    else:
        if not count:
            count = 1

        for c in range(count):
            code = str(uuid.uuid4())
            await DiscountCodes(brand_id=brand_id, code=code).create()
            codes.append(code)

    return {"discount_codes": codes}


@router.get("/{brand_id}/discount/fetch")
async def fetch(brand_id: int, user_id: int):
    """
    Endpoint for fetching available discount code for specific brand for user. Discount code is available if no user_id
    specified for the discount code.

    :param brand_id: PK of a Brand in Brands Table.
    :param user_id: PK of a User in Users Table.
    :return:
    """

    discount_code = None
    available_code = await DiscountCodes.query.where(
        and_(DiscountCodes.brand_id == brand_id, DiscountCodes.user_id.is_(None))).gino.first()

    if available_code:
        available_code.user_id = user_id
        await available_code.apply_updates()
        discount_code = available_code.code

    return {"found": available_code is not None, "discount_code": discount_code}
