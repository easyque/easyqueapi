import random
from fastapi import Depends, FastAPI
from schemas import User, OtpSend
from databse import engine, SessionLocal
import models
from sqlalchemy.orm import Session
import base64
import json
import time

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
    if(len(str(otpData.contact))<8):
        return {"message":"Please enter valid contact number", "status":False}

    return {"message":"OTP created successfully", "otp":otp, "status":True}


@app.post("/api/user_authication")
async def create_user(user: User, db: Session = Depends(get_db)):
    seconds = str(round(time.time()))+str(user.contact)
    sample_string = json.dumps({"contact":user.contact, "is_active":user.is_active, "loginuniqueKey":seconds})
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    userContact = user.contact
    if(len(str(userContact))<8):
        return {"message":"Please enter valid contact number", "status":False}

    try:
        data = db.query(models.User).filter(models.User.contact == user.contact).first()
        
        if(data!= None):
            update_user_token  = db.query(models.User).filter(models.User.contact == user.contact).update({models.User.auth_token:base64_string}, synchronize_session = False)
            db.commit()
            return {"status":True,"contact":user.contact, "is_active":user.is_active, "auth_token":base64_string, "activity":"login"}
        else:
            user_model = models.User()
            user_model.contact = user.contact
            user_model.auth_token = base64_string
            user_model.is_active = user.is_active 
            db.add(user_model)
            db.commit()
            return {"status":True, "contact":user.contact, "is_active":user.is_active, "auth_token":base64_string, "activity":"register"}
    except:
        return {"message":"Something went wrong", "status":False}
