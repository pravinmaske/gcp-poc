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
        address = fake.address()
        ssn = fake.ssn()
        job_title = fake.job()
        department = fake.random_element(elements=('HR', 'IT', 'Finance', 'Marketing', 'Operations'))
        salary = random.randint(30000, 120000)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        employee_data.append({
            'First Name': first_name,
            'Last Name': last_name,
            #'Name': name,
            'Email': email,
            'Phone Number': phone_number,
            'Address': address,
            'SSN': ssn,
            'Job Title': job_title,
            'Department': department,
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
num_records = 3
employee_data = generate_employee_data(num_records)
csv_filename='employee_data.csv'
bucket_name = 'stage_bucket'

save_to_csv_and_upload_to_gcs(csv_filename, bucket_name, employee_data)

# for employee in employee_data:
#     print(employee)

#print(df)