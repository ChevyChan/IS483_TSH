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
# email = "max@tongtah.com.sg"
# user_details = {"name": "Max",
#                 "email": email,
#                 "auth_provider": "Google",
#                 "member_type": "Employee",
#                 "company_name": "Tong Tah",
#                 "company_address": "123 Adam Rd #01-01",
#                 "company_contact": "63219876",
#                 "company_email": "support@tongtah.sg"
#                 }
# create_results = invoke_http("http://localhost:5001/v1/user/create_user/" + user_uuid + "/" + email, method='POST', 
#                              json=user_details
#                              )

# print()
# print( create_results )
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
# delivery_order_details = {"delivery_uuid": delivery_order_uuid, 
#                     "delivery_date": str(datetime.now().date()), 
#                     "delivery_time": "12:00pm", 
#                     "delivery_order_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a", 
#                     "bidding_uuid": "3ef26090-8b4c-41af-ab38-5266e8aa728e",
#                 }
# create_results = invoke_http("http://localhost:5001/v1/delivery_order/create_delivery_order", method='POST', 
#                              json=delivery_order_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all delivery orders ======================")
# #invoke bidding microservice to get all biddings
# results = invoke_http("http://localhost:5001/v1/delivery_order/get_all_delivery_orders", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected delivery order ======================")
# # invoke bidding microservice to get selected bidding 
# delivery_order_uuid = 'daef193a-2db4-4d35-8ba6-76b106115586'
# results = invoke_http("http://localhost:5001/v1/delivery_order/get_delivery_order_by_id/" + delivery_order_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Update Delivery Order Contents ======================")
# # invoke bidding microservice to update a bid
# delivery_order_uuid = 'daef193a-2db4-4d35-8ba6-76b106115586'
# delivery_order_details = { "delivery_order_file_url": "https://firebasestorage.googleapis.com/v0/b/is483-tsh.appspot.com/o/files%2F1_A%20Simple%20Five-Step%20Framework%20To%20Launching%20A%20Mobile%20App%20People%20Actually%20Want%20To%20Use.pdf?alt=media&token=acab169f-ac2d-4eb8-a53c-e086ce0f027a"}
# create_results = invoke_http("http://localhost:5001/v1/delivery_order/update_delivery_order/" + delivery_order_uuid, method='PUT', 
#                              json=delivery_order_details
#                              )

# print()
# print( create_results )
# print()

# print("============================ End of Delivery Order Microservice =============================")

# print()

# print("================== Invoking Purchase Delivery Microservice ====================")

# print()

# print("==================== Create a Purchase Delivery Order ======================")
# # #invoke Purchase Delivery Order microservice to create a Purchase Delivery Order
# purchase_delivery_order_uuid = str(uuid.uuid4())
# purchase_delivery_order_details = {"Purchase_Delivery_uuid": purchase_delivery_order_uuid, 
#                     "PurchaseUID": "0c4fdbe8-dc67-4f20-8849-83c96951dfe3", 
#                     "DeliveryUID": "1582aa22-8619-465c-aaad-ae20422a4e28", 
#                 }
# create_results = invoke_http("http://localhost:5001/v1/purchase_delivery/create_purchase_delivery_order", method='POST', 
#                              json=purchase_delivery_order_details
#                              )

# print()
# print( create_results )
# print()

# print("==================== Getting all purchase_delivery_order ======================")
# #invoke bidding microservice to get all biddings
# results = invoke_http("http://localhost:5001/v1/purchase_delivery/get_all_purchase_delivery_orders", method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print("==================== Get selected purchase_delivery_order ======================")
# # invoke bidding microservice to get selected bidding 
# purchase_delivery_order_uuid = 'd831d411-d467-4f40-a87b-27c732274577'
# results = invoke_http("http://localhost:5001/v1/purchase_delivery/get_purchase_delivery_order_by_id/" + purchase_delivery_order_uuid, method='GET')

# print( type(results) )
# print()
# print( results )
# print()

# print()

# print("============================ End of Purchase Delivery Microservice =============================")

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



print("================== Invoking Bidding Offer Microservice ====================")

print()

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

print("==================== Getting all biddings bid by Bidding======================")
#invoke bidding microservice to get all biddings
BiddingUID = "3ef26090-8b4c-41af-ab38-5266e8aa728e"
results = invoke_http("http://localhost:5001/v1/bidding_offer/get_all_bidding_offers/" + BiddingUID, method='GET')

print( type(results) )
print()
print( results )
print()

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

print("==================== Update bidding bid status ======================")
# invoke bidding microservice to update a bid
bidding_offer_uuid = '3dcb7c86-4a4a-4a52-9210-d74d68085091'
bidding_details = { "Bidding_Offer_Result": "Accepted"}
create_results = invoke_http("http://localhost:5001/v1/bidding_offer/update_bidding_offer_status/" + bidding_offer_uuid, method='PUT', 
                             json=bidding_details
                             )

print()
print( create_results )
print()

print("============================ End of Bidding Offer Microservice =============================")


print()
