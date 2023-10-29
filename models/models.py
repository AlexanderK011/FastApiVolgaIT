from sqlalchemy import MetaData, Table, Integer, Column, String, TIMESTAMP, ForeignKey, Boolean, Float, Double, \
    CheckConstraint, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

from database import Base
#openssl rand -hex 32 -generate random secret key
metadata = MetaData()

# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key = True),
#     Column('hashed_password',String,nullable = False),
#     Column('username',String,nullable=False),
#     Column('is_active', Boolean),
#     Column('is_superuser', Boolean),
#     Column('is_verified', Boolean))

class UserTable(Base):
    __tablename__ = 'usertable'
    id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String)
    password = Column(String)
    disabled = Column(Boolean, default= False)
    isAdmin = Column(Boolean,default=False)
    balance = Column(Double, default=0)

class Transport(Base):
    __tablename__ = 'transport'
    # Base.metadata,
    id = Column(Integer,primary_key=True,autoincrement=True)
    canBeRented = Column(Boolean) # можно ли арендовать?
    transportType = Column(String,CheckConstraint('TransportType IN(car,bike,scooter)')) # type transport[car,bike,scooter]
    models = Column(String)# модель транспорта
    identifier = Column(String) #Номерной знак
    description = Column(String) # описание, может быть null
    latitude = Column(Double)# Географическая широта местонахождения транспорта
    longitude = Column(Double) # Географическая долгота местонахождения транспорта
    minutePrice = Column(Double)#Цена аренды за минуту (может быть null)
    dayPrice = Column(Double)#Цена аренды за сутки (может быть null)
    ownerId = Column(BigInteger, ForeignKey('usertable.id'))
    __table_args__ = (
        CheckConstraint('TransportType IN(car,bike,scooter)'),
    )

class Rent(Base):
    __tablename__ = 'rent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rentType = Column(String) # [minutes,days]
    transport_id = Column(BigInteger, ForeignKey('transport.id'))
    userId = Column(BigInteger, ForeignKey('usertable.id'))
    timeStart = Column(String, default=0,nullable=False)
    timeEnd = Column(String,nullable=True)
    priceOfUnit = Column(Double) # цена единицы времени аренды
    finalPrice = Column(Double, default=None)






# class Renttransp(Base):
#     __tablename__ = 'renttransp'
#     id = Column(Integer, primary_key = True, autoincrement = True)
#     rentType = Column(String) # type rent [Minutes, Days]




