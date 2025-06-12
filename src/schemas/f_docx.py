from pydantic import BaseModel

class ApplicationData(BaseModel):
    employer_name : str
    full_name : str
    position : str
    date : str


class VacationData(BaseModel):
    supervisor : str
    full_name : str
    reason : str
    date_from : str
    date_till : str


class DismissalData(ApplicationData):
    reason : str


class TransferData(ApplicationData):
    department_1 : str
    department_2 : str



