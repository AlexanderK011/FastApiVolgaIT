from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Response,Request
from fastapi.security import OAuth2PasswordRequestForm

from deps import get_current_user
from deps import db
from models.models import Transport
from schemas import TransportUpdate, TransportCreate
from utils import create_refresh_token, create_access_token, verify_password, get_hashed_password

transportrout = APIRouter(prefix="/api/Transport",
    tags=["TransportController"],
    responses={404: {"description": "Not found"}})



#TransportController
@transportrout.get("/{id}")
async def transport_get_byid(id:int):
    trans = db.query(Transport).get(id)
    return trans

#только авторизованные пользователи
@transportrout.post('',response_model= TransportCreate)
async def transport_post(transport : TransportCreate,user = Depends(get_current_user)):
    if transport.transportType in('car','bike','scooter'):
        transpost = Transport(canBeRented = transport.canBeRented,
                         transportType = transport.transportType,
                         models = transport.models,
                         identifier = transport.identifier,
                         description= transport.description,
                         latitude = transport.latitude,
                         longitude = transport.longitude,
                         minutePrice = transport.minutePrice,
                         dayPrice = transport.dayPrice,
                         ownerId = user.id
                         )
        try:
            db.add(transport)
            db.commit()
        except:
            db.rollback()
        return transpost
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect transport_type'
        )

#только владелец транспорта
@transportrout.put('/{tid}', response_model = TransportUpdate)
async def updtrans(tid:int, transp: TransportUpdate,user = Depends(get_current_user)):
    # race_car_record = db.query(Transport).filter(Transport.id == tid).update(dict(transp))
    transpdb = db.query(Transport).filter(Transport.id==tid).filter(Transport.user_id == user.id).first()
    if not transpdb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not your transport'
        )
    if transp.transportType not in('car','bike','scooter'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect transport_type'
        )
    transpdb.canBeRented = transp.canBeRented
    transpdb.transportType = transp.transportType
    transpdb.models = transp.models
    transpdb.identifier = transp.identifier
    transpdb.description = transp.description
    transpdb.latitude = transp.latitude
    transpdb.longitude = transp.longitude
    transpdb.minutePrice = transp.minutePrice
    transpdb.dayPrice = transp.dayPrice
    try:
        db.add(transpdb)
        db.commit()
    except:
        db.rollback()
    return transpdb

#только владелец транспорта
@transportrout.delete('/{tr_id}')
async def deletetransp(tr_id:int, user = Depends(get_current_user)):
    if not db.query(Transport).filter(Transport.user_id == user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not your transport'
        )
    delet=db.query(Transport).filter(Transport.id == tr_id).filter(Transport.user_id == user.id).delete()
    db.commit()
    return db.query(Transport).all()


