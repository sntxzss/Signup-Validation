from pydantic import BaseModel, ValidationError, Field, field_validator, EmailStr

class Adress(BaseModel):
    city: str = Field(min_length=2)
    zip: str = Field(min_length=5, max_length=5)

class SignUp(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(ge=13, le=120)
    password: str = Field(min_length=8)
    address: Adress
    interests: list[str] = []

@field_validator("username")
def validation(cls, v):
    v = v.lower()
    if not v.replace("_", "").isalnum():
        raise ValueError("Only numbers, letters and underscores")
    return v

@field_validator("password")
def pass_valid(cls, v):
    if not any(ch.isdigit() for ch in v):
        raise ValueError("Password must contain at least one digit")
    return v


import json

with open("signupts.json", "r") as f:
    data = json.load(f)

accepted = []
rejected = []

for i, signup_data in enumerate(data):
    try:
        signup = SignUp(**signup_data)
        accepted.append(signup)
    except ValidationError as e:
        errors = []
        for err in e.errors():
            field_path = ".".join(str(x) for x in err["loc"])
            error_msg = f"{field_path}: {err['msg']}"
            errors.append(error_msg)
        rejected.append({"index": i, "errors": errors})

print(f"Прийнято: {len(accepted)}, відхилено: {len(rejected)}")
for entry in rejected:
    print(f"  Заявка {entry['index']}: {', '.join(entry['errors'])}")
