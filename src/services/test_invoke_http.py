#test_invoke_http.py
from invokes import invoke_http
from flask import Flask
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

print("================== Invoking Bidding Microservice ====================")

print()

print("==================== Create a User ======================")
# #invoke Users microservice to create a user
user_uuid = str(uuid.uuid4())
email = "max@tongtah.com.sg"
user_details = {"name": "Max",
                "email": email,
                "auth_provider": "Google",
                "member_type": "Employee",
                "company_name": "Tong Tah",
                "company_address": "123 Adam Rd #01-01",
                "company_contact": "63219876",
                "company_email": "support@tongtah.sg"
                }
create_results = invoke_http("http://localhost:5001/v1/user/create_user/" + user_uuid + "/" + email, method='POST', 
                             json=user_details
                             )

print()
print( create_results )
print()

# print("==================== Create a Bid ======================")
# # #invoke Bidding microservice to create a bid
# bidding_uuid = str(uuid.uuid4())
# bidding_details = {"bidding_uuid": bidding_uuid, "title": "Delivery to NUS", "description": "Testing", "delivery_date": "12-12-2023", "delivery_time": "13:00:00", "bidding_time": "24:00:00", "delivery_address": "123 Adam Rd #01-01", "poc_name": "Tom", "poc_email": "tom@tongtah.com.sg", "poc_contact": "63219876", 
# "purchase_order_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a&_gl=1*1op31q7*_ga*MTc2MTM4OTg1Mi4xNjg0NzI0NDYw*_ga_CW55HF8NVT*MTY4NTQxMzI3My4xNi4xLjE2ODU0MTQ1NTQuMC4wLjA."}
# create_results = invoke_http("http://localhost:5001/v1/bidding/create_bidding", method='POST', 
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all biddings ======================")
# #invoke bidding microservice to get all biddings
# results = invoke_http("http://localhost:5001/v1/bidding/get_all_biddings", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected bidding ======================")
# # invoke bidding microservice to get selected bidding 
# bidding_uuid = '920c3fcd-2965-4826-9651-a2e97b9d814f'
# results = invoke_http("http://localhost:5001/v1/bidding/get_bidding_published_by_id/" + bidding_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Update bidding ======================")
# # invoke bidding microservice to update a bid
# bidding_uuid = '920c3fcd-2965-4826-9651-a2e97b9d814f'
# bidding_details = { "delivery_date": "24-12-2023", "delivery_time": "13:00:00", "delivery_address": "123 Adam Rd #01-01", "poc_name": "Adam", "poc_email": "adam@tongtah.com.sg", "poc_contact": "65430987" }
# create_results = invoke_http("http://localhost:5001/v1/bidding/update_bidding/" + bidding_uuid, method='PUT', 
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()

# # print("==================== Delete events ======================")

# # EventID = 'aa71abc0-861e-42a0-8176-585a2be14e8e'
# # create_results = invoke_http("http://localhost:5000/v1/events/delete_event/" + EventID, method='DELETE'
# #                             )

# # print()
# # print( create_results )
# # print()

# print("============================ End of Events Microservice =============================")


# print()