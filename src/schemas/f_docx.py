from pydantic import BaseModel

class ApplicationData(BaseModel):
    employer_name : str
    full_name : str
    position : str
    date : str
