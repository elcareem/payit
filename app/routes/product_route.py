from fastapi import APIRouter, Depends, Request, HTTPException, status, File, UploadFile, Form
from app.models.user import User
from app.models.farmer import Farmer
from app.models.product import Product
from app.models.product_category import ProductCategory
from ..enums import ProductCategory as ProductCategoryEnum
from ..schemas.product_schema import ProductCreateRequest, ProductUpdateRequest, Product as ProductResponse
from app.database import SessionDep
from ..middleware.auth import AuthMiddleware
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
import aiofiles
import logging 
import pymysql
import os


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
# def create_product(product_request: ProductCreateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
#     farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()

#     if not farmer:
#         new_farmer = Farmer(
#             user_id = current_user.id
#         )
#         try:
#             db.add(new_farmer)
#             db.commit()
#             db.refresh(new_farmer)
#             farmer = new_farmer
#         except pymysql.DataError as e:
#             raiseError(e, request)
#         except Exception as e:
#             raiseError(e, request)

#     new_product = Product(
#         farmer_id = farmer.id,
#         **product_request.dict() 
#         ) 
#     try:
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)

#         return new_product
#     except pymysql.DataError as e:
#         raiseError(e, request)
#     except Exception as e:
#         raiseError(e, request)


@router.post("/", status_code=status.HTTP_200_OK)
async def upload_product(
                db: SessionDep,
                request: Request,
                category: ProductCategoryEnum = Form(...),
                name: str= Form(...),
                description: Optional[str] = Form(...),
                unit_price: int = Form(...),
                quantity: int = Form(...),
                image: UploadFile = File(None),
                current_user = Depends(AuthMiddleware),
            ):

    farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
    category = db.query(ProductCategory).filter(ProductCategory.name == category).first()

    if not farmer:
        new_farmer = Farmer(
            user_id = current_user.id
        )
        try:
            db.add(new_farmer)
            db.commit()
            db.refresh(new_farmer)
            farmer = new_farmer
        except pymysql.DataError as e:
            raiseError(e, request)
        except Exception as e:
            raiseError(e, request)


    allowed_ext = ["png", "jpeg", "jp"]
    file_ext = image.filename.split(".")[-1].lower()

    if not file_ext in  allowed_ext:
        raise_error("Invalid file extension", status.HTTP_400_BAD_REQUEST)

    max_image_size = 1024 * 1024
    content = await image.read()
    if len(content) > max_image_size:
        raise_error("File too large. Maximum size allowed is 1 MB.", status.HTTP_400_BAD_REQUEST)

    await image.seek(0)

    try:
    
        file_name = f"{uuid4()}.{file_ext}"

        file_path = f"{UPLOAD_DIR}/{file_name}"
        print(file_path)

        async with aiofiles.open(file_path, "wb") as output_file:
            content = await image.read()
            await output_file.write(content)

    except:
        raise_error("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        image_url = f"static/uploads/{file_name}"

        new_product = Product(
            farmer_id = farmer.id,
            category_id = category.id,
            name= name,
            description= description,
            unit_price = unit_price,
            quantity = quantity,
            image_url = image_url
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {
            "success": True,
            "data": new_product,
            "message": "Product uploaded successfully"
        }

    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
def get_all_products(db: SessionDep, request: Request):
    products = db.query(Product).all()

    if not products:
        raiseError("No available products", request)

    return products

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product(product_id: int, db: SessionDep, request: Request):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raiseError("Product doesn't exist", request)
    return product

@router.get("/me/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
def get_user_products(db: SessionDep, current_user = Depends(AuthMiddleware)):

    user = db.query(User).filter(User.id == current_user.id).first()
    user_products = user.farmer.products
    return user_products

@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(product_id: int, product_request: ProductUpdateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raiseError("Product doesn't exist", request)

    product_owner = product.farmer.user

    if product_owner != current_user:
        raiseError("Unauthorized user", request)

    update_data = product_request.dict(exclude_unset=True)
    

    try:
        for field, value in update_data.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def delete_product(product_id: int, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raiseError("Product doesn't exist", request)

    product_owner = product.farmer.user

    if product_owner != current_user:
        raiseError("Unauthorized user", request)

    try:
        deleted_product = product
        db.delete(product)
        db.commit()

        return deleted_product
    
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)



def raiseError(e: str, request: Request):
 
    method = request.method.upper()

    if method == "POST":
        message = f"Failed to create record: {e}"
    elif method == "GET":
        message = f"Failed to fetch record: {e}"
    elif method in ("PUT", "PATCH"):
        message = f"Failed to update record: {e}"
    elif method == "DELETE":
        message = f"Failed to delete record: {e}"
    else:
        message = f"Error: {e}"

    logger.error(message)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "status": "error",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def raise_error(e, status_code = status.HTTP_400_BAD_REQUEST):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status_code,
        detail = {
            "status": "error",
            "message": f"{e}", 
            "timestamp": f"{datetime.utcnow()}"
        }
    )

