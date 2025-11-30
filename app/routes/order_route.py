from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.models.user import User
from app.models.farmer import Farmer
from app.models.product import Product
from app.models.buyer import Buyer
from app.models.order import Order
from ..schemas.order_schema import OrderCreateRequest, OrderUpdateRequest, Order as OrderResponse
from app.database import SessionDep
from ..middleware.auth import AuthMiddleware
from datetime import datetime
from typing import List
import logging
import pymysql


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/orders", 
    tags=["Orders"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_request: OrderCreateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    buyer = db.query(Buyer).filter(Buyer.user_id == current_user.id).first()
    

    if not buyer:
        new_buyer = Buyer(
            user_id = current_user.id
        )
        try:
            db.add(new_buyer)
            db.commit()
            db.refresh(new_buyer)
            buyer = new_buyer
        except pymysql.DataError as e:
            raiseError(e, request)
    
    product = db.query(Product).filter(Product.id == order_request.product_id).first()

    if product.farmer.user == current_user:
        raiseError("Can't buy own product", request)

    unit_price = product.unit_price
    stock = product.quantity

    if order_request.quantity > stock:
        raiseError(f"Limited stock, available: {stock}", request)

    amount = unit_price * order_request.quantity

    new_order = Order(
        buyer_id = buyer.id,
        **order_request.dict(),
        unit_price = unit_price,
        amount = amount
    )
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
def get_all_orders(db: SessionDep, request: Request):
    orders = db.query(Order).all()

    if not orders:
        raiseError("No available orders", request)

    return orders


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def get_order(order_id: int, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raiseError("Order doesn't exist", request)

    order_owner = order.buyer.user

    if order_owner != current_user:
        raiseError("Unauthorized user", request)

    return order


@router.get("/me/", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
def get_user_orders(db: SessionDep, current_user = Depends(AuthMiddleware)):
    user = db.query(User).filter(User.id == current_user.id).first()
    user_orders = user.buyer.orders
    return user_orders


@router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def update_order(order_id: int, order_request: OrderUpdateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raiseError("Order doesn't exist", request)

    order_owner = order.buyer.user

    if order_owner != current_user:
        raiseError("Unauthorized user", request)


    product = order.product

    unit_price = product.unit_price
    stock = product.quantity

    if order_request.quantity > stock:
        raiseError(f"Limited stock, available: {stock}", request)

    amount = unit_price * order_request.quantity

    update_data = order_request.dict(exclude_unset=True)
    update_data["amount"] = amount
    
    try:
        for field, value in update_data.items():
            setattr(order, field, value)
        db.commit()
        db.refresh(order)
        return order
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def delete_order(order_id: int, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raiseError("Order doesn't exist", request)

    order_owner = order.buyer.user

    if order_owner != current_user:
        raiseError("Unauthorized user", request)

    try:
        deleted_order = order
        db.delete(order)
        db.commit()

        return deleted_order
    
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)


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
