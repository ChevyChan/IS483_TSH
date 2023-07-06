#test_invoke_http.py
from invokes import invoke_http
from flask import Flask
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# print("================== Invoking User Microservice ====================")

# print()

# print("==================== Create a User ======================")
# #invoke Users microservice to create a user
# user_uuid = str(uuid.uuid4())
# email = "john@tongtah.com.sg"
# user_details = {"name": "John",
#                 "email": email,
#                 "auth_provider": "Google",
#                 "member_type": "Employee",
#                 "CompanyID": 2
#                 }
# create_results = invoke_http("http://localhost:5001/v1/user/create_user/" + user_uuid + "/" + email, method='POST',
#                              json=user_details
#                              )

# print()
# print( create_results )
# print()

# print("============================ End of User Microservice =============================")

# print()

# print("================== Invoking Company Microservice ====================")

# print()

# print("==================== Create a Company ======================")
# #invoke Company microservice to create a company
# company_uuid = str(uuid.uuid4())
# company_email = "hello@tongtah.com.sg"
# company_details = {
#                 "company_id": company_uuid,
#                 "company_name": "Tong Tah Pte Ltd",
#                 "company_address": "1 Sims Ave #01-01, S(777777)",
#                 "company_email": company_email,
#                 "company_type": "Main"
#                 }
# create_results = invoke_http("http://localhost:5001/v1/company/create_company", method='POST',
#                              json=company_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Get selected company details ======================")
# # invoke company microservice to get selected company details
# company_uuid = '42f6d251-131e-4765-8da1-874d6fb8eec0'
# results = invoke_http("http://localhost:5001/v1/company/get_company_by_id/" + company_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("============================ End of Company Microservice =============================")

# print()

# print("================== Invoking Purchase Order Microservice ====================")

# print()

# #invoke purchase_order microservice to create a purchase order
# purchase_order_uuid = str(uuid.uuid4())
# purchase_order_details = {  "purchase_uuid": purchase_order_uuid,
#                             "purchase_date": str(datetime.now().date()),
#                             "purchase_order_file_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a",
#                             "UserUID": "89DzGgen05TSrQMeZbNOcytDfHj2"
#                          }
# create_results = invoke_http("http://localhost:5001/v1/purchase_order/create_purchase_order", method='POST',
#                              json=purchase_order_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all purchase orders ======================")
# #invoke purchase order microservice to get all purchase orders
# results = invoke_http("http://localhost:5001/v1/purchase_order/get_all_purchase_orders", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected purchase orders ======================")
# # invoke purchase order microservice to get selected purchase order
# purchase_order_uuid = '1'
# results = invoke_http("http://localhost:5001/v1/purchase_order/get_purchase_order_by_id/" + purchase_order_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("============================ End of Purchase Order Microservice =============================")

# print()

# print("================== Invoking Delivery Order Microservice ====================")

# print()

# print("==================== Create a Delivery Order ======================")
# # #invoke Delivery Order microservice to create a Delivery Order
# delivery_order_uuid = str(uuid.uuid4())
# purchase_uuid = "1"
# delivery_order_details = {"delivery_uuid": delivery_order_uuid,
#                     "delivery_date": str(datetime.now().date()),
#                     "delivery_time": "12:00pm",
#                     "delivery_order_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a",
#                     "delivery_status": "Ready to Ship",
#                     "bidding_uuid": "3ef26090-8b4c-41af-ab38-5266e8aa728e",
#                     "purchase_uuid": "1"
#                 }
# create_results = invoke_http("http://localhost:5001/v1/delivery_order/create_delivery_order/" + purchase_uuid, method='POST',
#                              json=delivery_order_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all delivery orders ======================")
# #invoke delivery order microservice to get all delivery order
# results = invoke_http("http://localhost:5001/v1/delivery_order/get_all_delivery_orders", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected delivery order ======================")
# # invoke delivery order microservice to get selected delivery order
# delivery_order_uuid = 'daef193a-2db4-4d35-8ba6-76b106115586'
# results = invoke_http("http://localhost:5001/v1/delivery_order/get_delivery_order_by_id/" + delivery_order_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Update Delivery Order Contents ======================")
# # invoke delivery order microservice to update a delivery order
# delivery_order_uuid = 'daef193a-2db4-4d35-8ba6-76b106115586'
# delivery_order_details = { "delivery_order_file_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a", "delivery_status": "Shipped"}
# create_results = invoke_http("http://localhost:5001/v1/delivery_order/update_delivery_order/" + delivery_order_uuid, method='PUT',
#                              json=delivery_order_details
#                              )

# print()
# print( create_results )
# print()

# print("============================ End of Delivery Order Microservice =============================")

# print()

print("================== Invoking Schedule Microservice ====================")

print()

print("==================== Create a Schedule ======================")
# #invoke schedule microservice to create a schedule for delivery
# #purchase_delivery_order_uuid = str(uuid.uuid4())
PurchaseUID = "1"
DeliveryUID = "3da304f1-8788-43f8-9ce2-f7856ebd274f"
scheduling_details = {
                    "schedule_date": str(datetime.now().date()), 
                    "schedule_time": str(datetime.now().time()),
                    "schedule_from_location": "6 Sim Drive", 
                    "schedule_to_location": "100 Hospital Way", 
                    "priority_level": "Low", 
                    "purchase_uid": PurchaseUID, 
                    "delivery_uid": DeliveryUID
                    }
create_results = invoke_http("http://localhost:5001/v1/schedule/create_schedule/" + PurchaseUID + "/" + DeliveryUID, method='POST',
                             json=scheduling_details
                             )

print()
print( create_results )
print()

print("==================== Getting all Schedules ======================")
#invoke schedule microservice to get all schedules
results = invoke_http("http://localhost:5001/v1/schedule/get_all_schedule", method='GET')

print( type(results) )
print()
print( results )
print()

print("==================== Get selected Schedule ======================")
# invoke schedule microservice to get selected schedule
purchase_uid = '0c4fdbe8-dc67-4f20-8849-83c96951dfe3'
delivery_uid = '1582aa22-8619-465c-aaad-ae20422a4e28'
results = invoke_http("http://localhost:5001/v1/schedule/get_schedule_by_id/" + purchase_uid + "/" + delivery_uid, method='GET')

print( type(results) )
print()
print( results )
print()

print()

print("============================ End of Schedule Microservice =============================")

# print()

# print("================== Invoking Bidding Microservice ====================")

# print()

# print("==================== Create a Bid ======================")
# # #invoke Bidding microservice to create a bid
# bidding_uuid = str(uuid.uuid4())
# bidding_details = {"bidding_uuid": bidding_uuid,
#                     "title": "Delivery to NUS",
#                     "description": "Testing",
#                     "bidding_date": "12-12-2023",
#                     "bidding_time": "12:00pm",
#                     "num_of_vehicles": 15
#                 }
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
# bidding_details = { "bidding_date": "24-12-2023", "bidding_time": "03:00pm", "num_of_vehicles": 10}
# create_results = invoke_http("http://localhost:5001/v1/bidding/update_bidding/" + bidding_uuid, method='PUT',
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()

# print("============================ End of Bidding Microservice =============================")


# print()


# print("================== Invoking Bidding Offer Microservice ====================")

# print()

# print("==================== Create a Bidding Offer ======================")
# # #invoke Bidding microservice to create a bid
# bidding_offer_uuid = str(uuid.uuid4())
# UserUID = "89DzGgen05TSrQMeZbNOcytDfHj2"
# BiddingUID = "3ef26090-8b4c-41af-ab38-5266e8aa728e"
# bidding_offer_details = {"bidding_offer_uuid": bidding_offer_uuid,
#                         "bid_price": "1000",
#                         "UserUID": UserUID,
#                         "BiddingUID": BiddingUID,
#                         "Bidding_Offer_Result": "Review"
#                 }
# create_results = invoke_http("http://localhost:5001/v1/bidding_offer/create_bidding_offer/" + UserUID + "/" + BiddingUID, method='POST',
#                              json=bidding_offer_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all biddings bid by Bidding======================")
# #invoke bidding microservice to get all biddings
# BiddingUID = "3ef26090-8b4c-41af-ab38-5266e8aa728e"
# results = invoke_http("http://localhost:5001/v1/bidding_offer/get_all_bidding_offers/" + BiddingUID, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected bidding bid ======================")
# # invoke bidding microservice to get selected bidding
# bidding_bid_uuid = '5ed1d1d1-dfa5-4373-bdc4-fe4dd0add17f'
# results = invoke_http("http://localhost:5001/v1/bidding_offer/get_bidding_offer_by_id/" + bidding_bid_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Update bidding bid ======================")
# # invoke bidding microservice to update a bid
# bidding_bid_uuid = '5ed1d1d1-dfa5-4373-bdc4-fe4dd0add17f'
# bidding_details = { "bid_price": "1200"}
# create_results = invoke_http("http://localhost:5001/v1/bidding_offer/update_bidding_offer/" + bidding_bid_uuid, method='PUT',
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Update bidding bid status (Acceptance) ======================")
# # invoke bidding microservice to update a bid
# bidding_offer_uuid = '3ef26090-8b4c-41af-ab38-5266e8aa728e'
# bidding_details = { "Bidding_Offer_Result": "Accepted"}
# create_results = invoke_http("http://localhost:5001/v1/bidding_offer/update_bidding_offer_status/" + bidding_offer_uuid, method='PUT',
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()


# print("==================== Update bidding bid status (Rejection) ======================")
# # invoke bidding microservice to update a bid
# bidding_offer_uuid = '3ef26090-8b4c-41af-ab38-5266e8aa728e'
# bidding_details = { "Bidding_Offer_Result": "Rejected"}
# create_results = invoke_http("http://localhost:5001/v1/bidding_offer/update_bidding_offer_status_rejection/" + bidding_offer_uuid, method='PUT',
#                              json=bidding_details
#                              )

# print()
# print( create_results )
# print()

# print("============================ End of Bidding Offer Microservice =============================")


print()

# print("================== Invoking Calendar Microservice ====================")

# print()

# print("==================== Create a Calendar ======================")
# # #invoke Calendar microservice to create a Calendar
# user_uuid = "879067b9-1faa-4fdf-bd05-918b162f2c55"
# calendar_details = {
#                     "calendar_name": "My Calendar", 
#                     "provider_name": "google", 
#                     "user_uuid": user_uuid
#                 }
# create_results = invoke_http("http://localhost:5001/v1/calendar/create_calendar", method='POST',
#                              json=calendar_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all Calendars ======================")
# #invoke Calendar microservice to get all Calendars
# results = invoke_http("http://localhost:5001/v1/calendar/get_all_calendars", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected calendar ======================")
# # invoke calendar microservice to get selected calendar
# calendar_uuid = 'c7bc9c51-a9d6-4c3e-87a2-7e2dd982f441'
# results = invoke_http("http://localhost:5001/v1/calendar/get_calendar_by_id/" + calendar_uuid, method='GET')

# print( type(results) )
# print()
# print( results )

# print("============================ End of Calendar Microservice =============================")

# print()

# print("================== Invoking Calendar Tasks Microservice ====================")

# print()

# print("==================== Create a Calendar Tasks ======================")
# # #invoke Calendar Tasks microservice to create a Calendar Tasks
# purchase_uuid = "0c4fdbe8-dc67-4f20-8849-83c96951dfe3"
# delivery_uuid = "1582aa22-8619-465c-aaad-ae20422a4e28"
# calendar_details = {
#                     "task_name": "Create Delivery Order for TSH Group", 
#                     "task_date": str(datetime.now().date()), 
#                     "task_time": str(datetime.now().time()), 
#                     "task_description": "Context will be: Delivery 3 goods to TSH Group. Contact Mr Max",
#                     "task_completed": "Pending", 
#                     "user_uid": "879067b9-1faa-4fdf-bd05-918b162f2c55", 
#                     "calendar_uid": "045d064e-a770-41a8-b23f-14b8c01d0cd5"
#                 }
# create_results = invoke_http("http://localhost:5001/v1/calendar_tasks/create_calendar_task", method='POST',
#                              json=calendar_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all Calendar Tasks ======================")
# #invoke Calendar Tasks microservice to get all Calendar Tasks
# results = invoke_http("http://localhost:5001/v1/calendar_tasks/get_all_calendar_tasks", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected Calendar Tasks ======================")
# # invoke Calendar Tasks microservice to get selected Calendar Tasks
# calendar_task_id = 'ad63d6f7-fd4c-4465-bc3f-1605b55d3c68'
# results = invoke_http("http://localhost:5001/v1/calendar_tasks/get_calendar_tasks_by_id/" + calendar_task_id, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Update Calendar Tasks ======================")
# # invoke calendar task microservice to update a task
# calendar_task_id = 'ad63d6f7-fd4c-4465-bc3f-1605b55d3c68'
# task_details = { "task_completed": "Completed"}
# create_results = invoke_http("http://localhost:5001/v1/calendar_tasks/update_calendar_tasks/" + calendar_task_id, method='PUT',
#                              json=task_details
#                              )

# print()
# print( create_results )
# print()


# print("============================ End of Calendar Tasks Microservice =============================")