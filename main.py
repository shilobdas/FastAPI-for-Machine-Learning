from fastapi import FastAPI,Path,HTTPException,Query

import json

app = FastAPI()
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data
@app.get("/")
def read_root():
    return {"Hello": "Patients management system API"}

@app.get("/about")
def about():
    return {"A fully functional api to manage patients records" }

@app.get("/view")
def view_patients():
    data = load_data()
    return data 

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description="The ID of the patient in the DB" , example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")
    

# @app.get("/sort")
# def sort_patients(sort_by:str = Query(..., description="The field to sort the patients by", example="age", enum=["name", "age", "gender","bmi","height","city"]),order:str=Query(enum=["asc","desc"],description='sort in asc or desc order')):
#     data = load_data()
#     valid_fields=["name","age","gender","bmi","height","city"]
#     if sort_by not in valid_fields:
#         raise HTTPException(status_code=400, detail="Invalid sort field")
    
#     if order not in ['asc','desc']:
#         raise HTTPException (status_code=400,detaile="invalid format")
    
#     sort_order = True if order =='desc' else False
#     sorted_patients = sorted(data.values(), key=lambda x: x[sort_by,0],reverse=False)
#     return sorted_patients

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi',example="age",enum=["name", "age", "gender","bmi","height","city"]), order: str = Query(enum=["asc","desc"], description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi',"name","city"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


