from uuid import UUID

from pydantic import BaseModel

class TransportCreate(BaseModel):
    canBeRented : bool
    transportType : str
    models : str
    identifier : str
    description : str
    latitude : float
    longitude : float
    minutePrice : float
    dayPrice : float

class TransportUpdate(BaseModel):
    canBeRented: bool
    transportType: str
    models: str
    identifier: str
    description: str
    latitude: float
    longitude: float
    minutePrice: float
    dayPrice: float

class TransportCreateAdmin(BaseModel):
    canBeRented: bool
    transportType: str
    models: str
    identifier: str
    description: str
    latitude: float
    longitude: float
    minutePrice: float
    dayPrice: float
    ownerId:int

class Renttype(BaseModel):
    rentType: str

class RentCrAdm(BaseModel):
    rentType: str
    transport_id: int
    userId: int

class RentUpdAdm(BaseModel):
    rentType:str
    transport_id:int
    userId:int
    timeStart:str
    timeEnd:str
    priceOfUnit:float
    priceType:str
    finalPrice:float

class Rentinfo(BaseModel):
    rentType:str
    transport_id:int
    userId:int

class TransportCoord(BaseModel):
    latitude:float
    longitude:float

class Usercr(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class CreateUserAdm(BaseModel):
    username: str
    password: str
    isAdmin:bool
    balance:float

class TokenData(BaseModel):
    username:str| None =None

class Userout(BaseModel):
    id: int
    username:str

class Balance(BaseModel):
    balance:int
    # class Config:
    #     orm_mode = True
