from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd

# importing ml model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()

#building pydantic model to validate incoming data

class UserInput(BaseModel):
    age:Annotated[int, Field(...,gt =0 , lt=120, description= 'age of the user')]
    weight:Annotated[float, Field(...,gt =0 ,description= 'weight of the user')]
    height:Annotated[float, Field(...,gt =0 , lt=2.5, description= 'height of the user')]
    income_lpa:Annotated[float, Field(...,gt =0 , description= 'annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description= 'Is the user a smoker')]
    city:Annotated[str, Field(..., description= 'city of the user')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
