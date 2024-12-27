from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hi"

from pto_upload_file import process_document
@app.route('/process_doc', methods=['POST'])
def call_process_document():
    return process_document()

from pto_erp_call import get_erp_data
@app.route('/erp_call', methods=['POST'])
def call_get_erp_data():
    return get_erp_data()

from pto_calculation import calculate_vacation
@app.route('/calculate_vacation_hours', methods=['POST'])
def call_calculate_vacation():
    return calculate_vacation()

if __name__ == "__main__":
    app.run(debug=True)
