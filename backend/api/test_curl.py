from security import create_access_token
token = create_access_token(data={"sub": "364", "role": "FACULTY"})
print(token)
