from fastapi import APIRouter
from fastapi import Depends
from deps import get_current_user
from deps import db
from models.models import UserTable
from schemas import Balance


paymrout = APIRouter(prefix="/api/Payment",
    tags=["PaymentController"],
    responses={404: {"description": "Not found"}})


#PaymentController
@paymrout.post('/Hesoyam/{accountId}',response_model=Balance)
async def paymentadd(accountId:int,user = Depends(get_current_user)):
    user1 = db.query(UserTable).filter(UserTable.id == accountId).filter(UserTable.id == user.id).first()
    if user1:
        user1.balance = user1.balance + 250000
        db.add(user1)
        db.commit()
    return user1
