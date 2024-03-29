from faker import Faker
import random
import string
import pandas as pd
from google.cloud import storage

fake = Faker()

def generate_employee_data(num_records):
    employee_data = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        #name = f"{first_name} {last_name}"
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.city()
        ssn = fake.ssn()
        job_title = fake.job() # Generate 
        department = fake.job() # Generate department-like data using the job() method
        #department = fake.random_element(elements=('HR', 'IT', 'Finance', 'Marketing', 'Operations'))  # Generate department-like data using the job() method
        #salary = random.randint(30000, 120000)
        salary = fake.random_number(digits = 5)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        employee_data.append({
            'First Name': first_name,
            'Last Name': last_name,
            'Job Title': job_title,
            'Department': department,
            'Email': email,
            'Address': address,
            'Phone Number': phone_number,            
            'Salary': salary,
            'Password': password
        })
    return employee_data


def save_to_csv_and_upload_to_gcs(filename, bucket_name, employee_data):

    df = pd.DataFrame(employee_data)
    df.to_csv(filename, index=False)

    #upload csv to GCS 

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print(f"File {filename} is uploaded to bucket {bucket_name}.")
    



# Example usage:
num_records = 50
employee_data = generate_employee_data(num_records)
csv_filename='employee_data.csv'
bucket_name = 'poc_storage_bkt' # storage bucket name

save_to_csv_and_upload_to_gcs(csv_filename, bucket_name, employee_data)

# for employee in employee_data:
#     print(employee)

#print(df)