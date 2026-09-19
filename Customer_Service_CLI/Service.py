from exceptions import DuplicateCustomerError,CustomerNotFound
from model import Customer
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "customers.json")
ALLOWED_FIELDS = ("name","email","phone")

all_customers = {}

def validate_customer(name,email,phone):
    if not str(name).strip():
        raise ValueError("Please enter the name field.")
    email = str(email)
    if "@" not in email or "."not in email.split("@")[-1]:
        raise ValueError("Enter the valid email..")
    if not str(phone).isdigit() or not 10<= len(str(phone))<=15:
        raise ValueError("Enter the valid contact info..")

    
def create_customer(customer_id, name, email, phone):
    customer_id = str(customer_id)
    if customer_id in all_customers:
        raise DuplicateCustomerError(f"{customer_id}has already exist!")
    
    validate_customer(name,email,phone)
    new_customer = Customer(name,email,phone)
    all_customers[customer_id] = new_customer
    save_to_file()
    return new_customer

def save_to_file():
    data_to_save = {cid:{"name":c.name, "email":c.email, "phone":c.phone} for cid,c in all_customers.items()}
    tmp = DATA_FILE + ".tmp"
    with open(tmp,"w") as f:
        json.dump(data_to_save,f,indent=2)
    os.replace(tmp, DATA_FILE)

def list_all_customer():
    
    if  all_customers:
        return dict(all_customers)
    else:
        raise CustomerNotFound("There is no customer record!")

def load_data():
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)       
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        raise RuntimeError("Data file corrupt! fix it with backup..")
    for cid, info in data.items():
        all_customers[cid]= Customer(info["name"],info["email"],info["phone"])
    
def search(customer_id):
    customer_id = str(customer_id)
    if customer_id in all_customers:
        search_result = all_customers[customer_id]
        return search_result
    else:
        raise CustomerNotFound(f"CustomerID:{customer_id} not in the list!")

def update(customer_id,field_name,new_value):
    customer_id = str(customer_id)
    if customer_id not in all_customers:
        raise CustomerNotFound(f"{customer_id} not in the list")
    if field_name not in ALLOWED_FIELDS:
        raise ValueError(f"Invalid field :{field_name}")
    customer = all_customers[customer_id]
    values = {"name":customer.name, "email":customer.email, "phone":customer.phone}
    values[field_name] = new_value
    validate_customer(**values)
    setattr(customer,field_name,new_value)
    save_to_file()
    
def delete(customer_id):
    customer_id = str(customer_id)
    if customer_id in all_customers:
        rc=all_customers.pop(customer_id)
        save_to_file()
        return rc
    else:
        raise CustomerNotFound(f"There is no customer record in {customer_id}")
