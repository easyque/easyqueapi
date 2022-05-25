import random
from fastapi import Depends, FastAPI
from schemas import User, OtpSend
from databse import engine, SessionLocal
import models
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/api/users")
async def all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/api/send_otp")
async def send_otp(otpData: OtpSend, db: Session = Depends(get_db)):
    otp = random.randint(100000,999999)
    try:
        data = db.query(models.User).filter(models.User.contact == otpData.contact).first()
    except:
        return {"message":"Something went wrong", "status":False}
    is_registered = False
    if(data!= None):
        is_registered = True
    return {"message":"OTP created successfully", "otp":otp, "is_registered":is_registered, "status":True}


@app.post("/api/create_user")
async def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.contact = user.contact
    user_model.auth_token = user.auth_token
    user_model.is_active = user.is_active

    db.add(user_model)
    db.commit()
    return user