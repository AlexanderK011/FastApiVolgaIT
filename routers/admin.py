from datetime import datetime

from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from deps import get_current_user
from deps import db
from models.models import UserTable, Transport, Rent
from schemas import Balance, CreateUserAdm, TransportCreateAdmin, RentUpdAdm, TransportCoord, RentCrAdm
from utils import get_hashed_password

adminaccounts = APIRouter(prefix="/api/Admin",
    tags=["AdminAccountController"],
    responses={404: {"description": "Not found"}})

admintransp = APIRouter(prefix="/api/Admin",
    tags=["AdminTranstorController"],
    responses={404: {"description": "Not found"}})

adminrent = APIRouter(prefix="/api/Admin",
    tags=["AdminRentController"],
    responses={404: {"description": "Not found"}})


#AdminAccountController
@adminaccounts.get('/Account')
async def getAllusers(start:int,count:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        users = db.query(UserTable).filter(UserTable.id>=start)[:count]
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not admin'
        )

@adminaccounts.get('/Account/{id}')
async def getInfoabAcc(id :int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        user = db.query(UserTable).filter(UserTable.id == id).first()
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not admin'
        )

@adminaccounts.post('/Account',response_model=CreateUserAdm)
async def crNewAcc(newuser : CreateUserAdm,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if db.query(UserTable).filter(UserTable.username == newuser.username).all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with this username already exist'
            )
        newuser = UserTable(
            username = newuser.username,
            password = get_hashed_password(newuser.password),
            balance = newuser.balance,
            isAdmin = newuser.isAdmin
        )
        try:
            db.add(newuser)
            db.commit()
        except:
            db.rollback()
        return newuser
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not admin'
        )

@adminaccounts.put('/Account/{id}',response_model=CreateUserAdm)
async def updAcc(id :int,userupd:CreateUserAdm,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if db.query(UserTable).filter(UserTable.username == userupd.username).all():
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail='User with this username already exist'
            )
        user = db.query(UserTable).filter(UserTable.id == id).first()
        user.username = userupd.username
        user.password = get_hashed_password(userupd.password)
        user.isAdmin = userupd.isAdmin
        user.balance = userupd.balance
        db.add(user)
        db.commit()

        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User not admin'
        )

@adminaccounts.delete('/Account/{id}')
async def delAcc(id: int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if db.query(UserTable).filter(UserTable.id == id).first():
            user = db.query(UserTable).filter(UserTable.id == id).delete()
            db.commit()
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is not exist'
            )


#AdminTranstorController
@admintransp.get('/Transport')
async def allTransports(start:int,count:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        transport = db.query(Transport).filter(Transport.id>=start)[:count]
        return transport
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is not exist'
        )

@admintransp.get('/Transport/{id}')
async def infoAbTranp(id :int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        transport = db.query(Transport).filter(Transport.id == id).first()
        return transport

@admintransp.post('/Transport',response_model=TransportCreateAdmin)
async def newTransp(transport: TransportCreateAdmin,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if transport.transportType in ('car', 'bike', 'scooter'):
            transport = Transport(
                canBeRented=transport.canBeRented,
                transportType=transport.transportType,
                models=transport.models,
                identifier=transport.identifier,
                description=transport.description,
                latitude=transport.latitude,
                longitude=transport.longitude,
                minutePrice=transport.minutePrice,
                dayPrice=transport.dayPrice,
                ownerId=transport.ownerId
            )
            try:
                db.add(transport)
                db.commit()
            except:
                db.rollback()
            return transport
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect transport_type'
            )
@admintransp.put('/Transport/{id}',response_model=TransportCreateAdmin)
async def updTransp(id:int, transport: TransportCreateAdmin, adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if transport.transportType not in ('car', 'bike', 'scooter'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect transport_type'
            )
        transpdb = db.query(Transport).filter(Transport.id == id).first()

        transpdb.canBeRented = transport.canBeRented
        transpdb.transportType = transport.transportType
        transpdb.models = transport.models
        transpdb.identifier = transport.identifier
        transpdb.description = transport.description
        transpdb.latitude = transport.latitude
        transpdb.longitude = transport.longitude
        transpdb.minutePrice = transport.minutePrice
        transpdb.dayPrice = transport.dayPrice
        transpdb.ownerId = transport.ownerId
        try:
            db.add(transpdb)
            db.commit()
        except:
            db.rollback()
        return transpdb

@admintransp.delete('/Transport/{id}')
async def delTransp(id:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        transport = db.query(Transport).filter(Transport.id == id).first()
        db.delete(transport)
        db.commit()
        return transport



#AdminRentController
@adminrent.get('/Rent/{rentId}')
async def getRentinfo(rentId:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        rent = db.query(Rent).filter(Rent.id == rentId).first()
        return rent

@adminrent.get('/UserHistory/{userId}')
async def userHistorRent(userId:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        rent = db.query(Rent).filter(Rent.userId == userId).all()
        return rent

@adminrent.get('/TransportHistory/{transportId}')
async def transpHistoryRent(transportId:int,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        rent = db.query(Rent).filter(Rent.transport_id == transportId).all()
        return rent

@adminrent.post('/Rent',response_model=RentCrAdm)
async def newRent(rent: RentCrAdm,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        transport = db.query(Transport).filter(Transport.id == rent.transport_id).first()
        rent.rentType = rent.rentType.lower()
        if rent.rentType == 'minutes' and transport.minutePrice is not None:
            priceOfUnit = transport.minutePrice
        if rent.rentType == 'days' and transport.dayPrice is not None:
            priceOfUnit = transport.dayPrice
        if rent.rentType in ('minutes', 'days'):
            rent = Rent(
                rentType=rent.rentType,
                transport_id=rent.transport_id,
                userId=rent.userId,
                timeStart=datetime.utcnow(),
                priceOfUnit=priceOfUnit,
                finalPrice=0
            )
            try:
                db.add(rent)
                db.commit()
            except:
                db.rollback()
            return rent

@adminrent.post('/Rent/End/{rentId}')
async def endRentAdm(rentId:int,transportcoord:TransportCoord, adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        rentdb = db.query(Rent).filter(Rent.id == rentId).first()
        if rentdb and rentdb.timeEnd is None:
            timeend = datetime.utcnow()
            rentdb.timeStart = datetime.fromisoformat(rentdb.timeStart)
            if rentdb.rentType == 'minutes':
                finalprice = round((timeend - rentdb.timeStart).total_seconds() / 60 * rentdb.priceOfUnit)
            elif rentdb.rentType == 'days':
                finalprice = (timeend - rentdb.timeStart).days() * rentdb.priceOfUnit
            else:
                finalprice = None
            user = db.query(UserTable).filter(UserTable.id == rentdb.userId).first()
            tr = db.query(Transport).filter(Transport.id == rentdb.transport_id).first()
            tr.latitude = transportcoord.latitude
            tr.longitude = transportcoord.longitude
            rentdb.timeEnd =datetime.utcnow()
            rentdb.finalPrice = finalprice
            user.balance = user.balance - finalprice
            db.add(tr)
            db.commit()
            return transportcoord
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='not valid rentid or the rental has already been completed'
            )

@adminrent.put('/Rent/{id}')
async def updRentAdm(id: int,rent : RentUpdAdm,adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        if rent.rentType in ('minutes', 'days'):
            rentdb = db.query(Rent).filter(Rent.id == id).first()
            if rentdb:
                rentdb.timeEnd = rent.timeEnd
                rentdb.transport_id = rent.transport_id
                rentdb.userId = rent.userId
                rentdb.timeStart = rent.timeStart
                rentdb.timeEnd = rent.timeEnd
                rentdb.priceOfUnit = rent.priceOfUnit
                rentdb.rentType = rent.rentType
                rentdb.finalPrice = rent.finalPrice
                db.commit()
                return rent
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='rent is not exist'
                )
@adminrent.delete('/Rent/{rentId}')
async def rentDelAdm(rentId:int, adminuser = Depends(get_current_user)):
    if adminuser.isAdmin:
        rent = db.query(Rent).filter(Rent.id == rentId).delete()
        if rent == 1:
            db.commit()
            return rent
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='rent is not exist'
            )

