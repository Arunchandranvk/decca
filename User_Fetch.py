import requests
import pandas as pd
import json
import time

# ✅ API Endpoint
url = "https://api.crm.luminartechnolab.com/api/student"

# ✅ Your JWT Token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MzhhYTdkZjM3Mjc1MzBiNDZkM2MwZSIsInJvbGUiOiI2NTNiZDUwNjE0NDJmYjZjODI1MTViOWEiLCJpYXQiOjE3NTEwOTIzOTJ9.pJh-xS2NaPcqyM57-8xnaLuB09IQQYQvcbfz4k78Ysw"

# ✅ Path to CSV file with phone numbers
csv_path = "user_project.csv"

# ✅ Read phone numbers
df = pd.read_csv(csv_path)

# ✅ Assuming the column name is 'phone'
if 'phone' not in df.columns:
    raise ValueError("CSV file must have a column named 'phone'.")

phone_numbers = df['phone'].astype(str).tolist()

# ✅ Headers
headers = {
    "Authorization": f"Bearer {jwt_token}"
}

# ✅ Store final results
final_data = []

# ✅ Loop through each phone number
for phone in phone_numbers:
    filter_payload = [
        {"field": "status", "operation": "not_equal", "value": ["67650a82d0de5212ac6ed087"]},
        {"operation": "search", "value": [phone]}
    ]

    params = {
        "_start": 0,
        "_end": 15,
        "_order": "DESC",
        "_sort": "createdAt",
        "filter": json.dumps(filter_payload)
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        
        for student in data:
            student_name = student.get("name", "")
            phone_number = student.get("contactNumber", {}).get("phoneNumber", "")
            joining_date = student.get("batch", {}).get("startDate", "")
            batch_name = student.get("batch", {}).get("name", "")
            course_name = student.get("batch", {}).get("course", {}).get("name", "")
            
            trainers = student.get("batch", {}).get("trainers", [])
            trainer_name = trainers[0].get("username", "") if trainers else ""

            final_data.append({
                "Batch Name": batch_name,
                "Course Name": course_name,
                "Student Name": student_name,
                "Phone": phone_number,
                "Joining Date": joining_date,
                "Trainer": trainer_name
            })
    else:
        print(f"Failed for phone {phone}: {response.status_code}")
    
    # Optional: Delay to avoid overwhelming the API
    time.sleep(1)

# ✅ Save to Excel
if final_data:
    output_df = pd.DataFrame(final_data)
    output_df.to_excel("student_details2.xlsx", index=False)
    print("Data saved to 'student_details.xlsx'")
else:
    print("No matching data found.")
