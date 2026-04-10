from jose import jwt, JWTError
import datetime

# Replace with your actual secret key
SECRET_KEY = "UQs7-3Ccu1ZFiT4_RpytRBC6wzQLRw9uYQ0V1wL_BMU"
ALGORITHM = "HS256"

# Take token input from user
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuaWtoaWwiLCJyb2xlIjoidmlld2VyIiwiZXhwIjoxNzUxMzU3NTY2fQ.qWiWNENa2_s32dt8EEeKK3W7AMg8oTGgSs0azPxId78"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("\n✅ Token is valid!")
    print("🔓 Decoded Payload:")
    for key, value in payload.items():
        print(f"{key}: {value}")
        print(datetime.datetime.fromtimestamp(1751357566))
except JWTError as e:
    print("\n❌ Invalid or expired token.")
    print(f"Error: {e}")
