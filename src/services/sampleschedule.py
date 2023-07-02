# 3.3 https://docs.google.com/spreadsheets/d/1cJPvlwikNdK-L1NOOQnjlZrsX2pb-wTRb2WdoNIvTHs/edit#gid=0
# based on the forecast result
# Database tbc again

availableVehicle = 12  # this is the default no. as per 3.3 https://docs.google.com/spreadsheets/d/1cJPvlwikNdK-L1NOOQnjlZrsX2pb-wTRb2WdoNIvTHs/edit#gid=0
forecast = 13  # FORECAST: based on BA algo
# we will then have to sync with schedule


def checkIfEnough():
    if (forecast <= 12):  # case1
        print("no need for bidding")
        # ***************************************************************************
        # PLANNING: Generation of schedule logic (UI to see schedule) AND for dashboard UI AND UI to view report generated
        # BA input for calculation capacity n schedule for next week to "Query"

        # CONFIRM: Delivery partner UI to CONFIRM
        # Tricky part where we have to query the Database and plan based on the empty slots/ time

        # ***************************************************************************

        # To put the AMQP email here
        # Delivery partner to confirm (need UI)

    else:  # case2
        # this will trigger bidding where bidding will compare lowest bid
        print("trigger bidding")
        # Need UI for external delivery to bid
        # To put the AMQP email here for lowest bid


checkIfEnough()


# def invoke_http(url, method='GET', json=None, **kwargs):
#     """A simple wrapper for requests methods.
#        url: the url of the http service;
#        method: the http method;
#        data: the JSON input when needed by the http method;
#        return: the JSON reply content from the http service if the call succeeds;
#             otherwise, return a JSON object with a "code" name-value pair.
#     """
#     code = 200
#     result = {}

#     try:
#         print("")
#     except Exception as e:
#         code = 500
#         result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
#     if code not in range(200,300):
#         return result

#     ## Check http call result
#     if r.status_code != requests.codes.ok:
#         code = r.status_code
#     try:
#         result = r.json() if len(r.content)>0 else ""
#     except Exception as e:
#         code = 500
#         result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

#     return result
