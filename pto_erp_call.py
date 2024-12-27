import requests
from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

def erp_call_from_json(input_json):
    # Extract required fields from the input JSON
    employee_id = input_json.get('EmployeeId')
    start_date = input_json.get('StartDate')
    end_date = input_json.get('EndDate')

    if not employee_id or not start_date or not end_date:
        return 0, 0, "Missing required fields in input JSON"

    # Convert string dates to datetime objects
    try:
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
    except ValueError:
        return 0, 0, "Invalid date format in input JSON"

    # ERP Integration
    tenant_id = "371cb917-b098-4303-b878-c182ec8403ac"
    client_id = "95faa8e8-8062-4e79-bd72-93d0ab4d0bf4"
    client_secret = "qYn8Q~4P05hz~hLOiqleInGu8AgOCTHhuNyqEaMh"
    resource = "45fedc21-15c5-40d8-83d2-0a5d20694717"

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': resource,  # Use 'scope' if required by your API
    }

    response = requests.post(token_url, data=payload)
    token_response = response.json()

    if 'access_token' in token_response:
        access_token = token_response['access_token']
    else:
        return 0, 0, "Failed to obtain access token"

    # Web service URL
    api_url = 'https://allegismulesoft.allegisgroup.com/allegis-prod-psemployeetimedataapi/v1/timecode/summary'
    
    # Parameters for the GET request
    params = {
        'EmployeeId': employee_id,
        'StartDate': start_date.strftime('%Y-%m-%d'),
        'EndDate': end_date.strftime('%Y-%m-%d')
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    try:
        # Make the GET request to the web service
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Check if data is empty
        if not data:
            return 0, 0, "No Data"

        # Process the data and extract relevant information
        for item in data:
            # Assuming the required fields are 'TotalHrsWorked', 'TotalHrsVacUsed', and 'State'
            total_hrs_worked = item.get('TotalHrsWorked', 0)
            total_hrs_vac_used = item.get('TotalHrsVacUsed', 0)
            state = item.get('State', "Unknown")
            return total_hrs_worked, total_hrs_vac_used, state

    except requests.exceptions.RequestException as e:
        return 0, 0, f"An error occurred while calling the web service: {e}"

    except ValueError as ve:
        return 0, 0, f"Invalid input: {ve}"


@app.route('/erp_call', methods=['POST'])
def get_erp_data():
    try:
        # Get JSON data from the POST request
        input_json = request.get_json()

        # Call the ERP data function with the JSON input
        regular_hours_worked, used_vacations, emp_state = erp_call_from_json(input_json)

        if emp_state != "Error" and emp_state != "Missing required fields in input JSON":
            # Return the results in a JSON response
            return jsonify({
                'Regular Hours Worked': regular_hours_worked,
                'Used Vacations Till Now': used_vacations,
                'State': emp_state
            })
        else:
            # Return an error message if something went wrong
            return jsonify({'Error': emp_state}), 400

    except Exception as e:
        return jsonify({'Error': str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
