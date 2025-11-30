import base64
import json 
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZW1haWwiOiJ0ZW5pQGV4YW1wbGUuY29tIiwidXNlcl9pZCI6IjUiLCJleHAiOjE3NjQwNzcwNzV9.Yxu0780pUiBi8gZvVcdPspKTavJWC5jllQ7ZW6lkCBk" 

def decode_jwt_str(token_str: str):
    padding = '=' * (-len(token_str) % 4)

    return base64.urlsafe_b64decode(token_str + padding)

def decode_jwt(token: str):
    header_base64, payload_base64, sig = token.split(".")
    payload = json.loads(decode_jwt_str(payload_base64))

    return payload



print(decode_jwt_str(token))