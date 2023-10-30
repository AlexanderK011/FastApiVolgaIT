import math
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from deps import get_current_user
from deps import db
from models.models import Transport, Rent
from schemas import TransportCoord, Renttype, Rentinfo



rentscontr = APIRouter(prefix="/api/Rent",
    tags=["RentController"],
    responses={404: {"description": "Not found"}})


#RentController
@rentscontr.get('/Transport')
async def getrenttransport(lat:float, long:float, radius:float, type:str):
    type = type.lower()
    if type in('car','bike','scooter','all'):
        long1 = long - radius/abs(math.cos(math.radians(long))*111.0)
        long2 = long + radius/abs(math.cos(math.radians(long))*111.0)
        lat1 = lat - (radius / 111.0)
        lat2 = lat + (radius / 111.0)
        if type == 'all':
            transp = db.query(Transport).filter(Transport.latitude.between(lat1, lat2)).filter(
                (Transport.latitude.between(long1, long2))).all()
        else:
            transp = db.query(Transport).filter(Transport.latitude.between(lat1,lat2)).filter((Transport.latitude.between(long1,long2))).filter(Transport.transportType == type).all()

        return transp

@rentscontr.get('/{rentId}',response_model=Rentinfo)
async def infoaborent(rentId:int,user = Depends(get_current_user)):
    if db.query(Rent).filter(Rent.id == rentId).filter(Rent.userId == user.id).first() and db.query(Transport).filter(Transport.ownerId == user.id).first():
        rent = db.query(Rent).filter(Rent.id == rentId).first()
        return rent
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='you dont have access'
        )

@rentscontr.get('/MyHistory/')
async def myrenthistory(user = Depends(get_current_user)):
    rent = db.query(Rent).filter(Rent.userId == user.id).all()
    return rent

@rentscontr.get('/TransportHistory/{transportId}')
async def historyrenttransp(transportId : int,user = Depends(get_current_user)):
    if db.query(Transport).filter(Transport.ownerId == user.id).filter(Transport.id == transportId).first():
        rent = db.query(Rent).filter(Rent.transport_id == transportId).all()
        return rent
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transport not in you own'
        )

@rentscontr.post('/New/{transportId}',response_model=Renttype)
async def createrent(transportId:int,rent: Renttype,user = Depends(get_current_user)):
    if db.query(Transport).filter(Transport.id == transportId).filter(Transport.ownerId == user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='you cant rent your own transport'
        )
    transport = db.query(Transport).filter(Transport.id == transportId).first()
    rent.rentType = rent.rentType.lower()
    if rent.rentType == 'minutes' and transport.minutePrice is not None:
        priceOfUnit = transport.minutePrice
    if rent.rentType == 'days' and transport.dayPrice is not None:
        priceOfUnit = transport.dayPrice
    if rent.rentType in ('minutes', 'days'):
        rent = Rent(
            rentType = rent.rentType,
            transport_id = transportId,
            userId = user.id,
            timeStart = datetime.utcnow(),
            priceOfUnit = priceOfUnit,
            finalPrice=0
        )
        try:
            db.add(rent)
            db.commit()
        except:
            db.rollback()
        return rent
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='rentType input minutes or days'
        )

@rentscontr.post('/End/{rentId}',response_model = TransportCoord)
async def rentend(rentId:int,transportcoord:TransportCoord, user = Depends(get_current_user)):
    rentdb= db.query(Rent).filter(Rent.userId == user.id).filter(Rent.id == rentId).first()
    if rentdb and rentdb.timeEnd is None:
        timeend = datetime.utcnow()
        rentdb.timeStart = datetime.fromisoformat(rentdb.timeStart)
        if rentdb.rentType == 'minutes':
            finalprice = round((timeend - rentdb.timeStart).total_seconds()/60*rentdb.priceOfUnit)
        elif rentdb.rentType == 'days':
            finalprice = (timeend - rentdb.timeStart).days()*rentdb.priceOfUnit
        else:
            finalprice = None
        tr = db.query(Transport).filter(Transport.id == rentdb.transport_id).first()
        tr.latitude=transportcoord.latitude
        tr.longitude=transportcoord.longitude
        rentdb.timeEnd = timeend
        rentdb.finalPrice = finalprice
        db.add(tr)
        db.commit()
        return transportcoord
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='not valid rentid or the rental has already been completed'
        )
