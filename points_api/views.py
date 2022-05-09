from functools import reduce
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Mock data 
mock_transaction = [
    {"payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z"},
    {"payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z"},
    {"payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z"},
    {"payer": "MILLER COORS", "points": 10000,
        "timestamp": "2020-11-01T14:00:00Z"},
    {"payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z"},
]


@csrf_exempt
def add_transaction(request):
    if request.method == "POST":
        # Confirm the request has input
        if not request.body:
            return HttpResponse('No transaction added')
        # convert input and save in mock data list
        req_body = json.loads(request.body)
        mock_transaction.append(req_body)
        return HttpResponse(json.dumps(req_body))


@csrf_exempt
def spend_points(request):
    if request.method == "POST":
        if not request.body:
            return HttpResponse("No points added")
        elif not mock_transaction:
            return HttpResponse("User have no points yet")
        points_to_spend = json.loads(request.body)['points']

        # Check if the amount of points to spend is more than user's points balance
        total_available_points = 0
        for i in mock_transaction:
            total_available_points += i['points']
        if total_available_points < points_to_spend:
            return HttpResponse("Required points is more than user's points balance!")

        # Sort transactions in ascending order based on timestamp
        sorted_data = sorted(mock_transaction, key=lambda i: i['timestamp'])

        # calculate how much each payer's points will be used
        i = 0
        spent_points_report = {}
        while points_to_spend > 0 and i < len(sorted_data):
            current_payer = sorted_data[i]['payer']
            points_spent_by_payer = min(
                points_to_spend, sorted_data[i]['points'])

            if not (current_payer in spent_points_report.keys()):
                spent_points_report[current_payer] = points_spent_by_payer
                sorted_data[i]['points'] -= points_spent_by_payer
            else:
                spent_points_report[current_payer] += points_spent_by_payer
                sorted_data[i]['points'] -= points_spent_by_payer
            points_to_spend -= points_spent_by_payer
            
            i += 1

        for key, value in spent_points_report.items():
            spent_points_report[key] = -1 * value

        return HttpResponse(json.dumps(spent_points_report))


def get_payer_balances(request):
    if not mock_transaction:
        return HttpResponse("User have no points yet")

    balances = {}
    for i in mock_transaction:
        if i['payer'] not in balances.keys():
            balances[i['payer']] = i['points']
        else:
            balances[i['payer']] += i['points']
    return HttpResponse(json.dumps(balances))
