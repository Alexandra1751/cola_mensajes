from flask import Flask, request, jsonify
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
invalid_forms_path = "invalid_forms"
duplicate_forms_path = "duplicate_forms"
os.makedirs(invalid_forms_path, exist_ok=True)
os.makedirs(duplicate_forms_path, exist_ok=True)

class Validation:
    def __init__(self):
        self.valid_forms = []
        self.invalid_forms = []

    def validate_form(self, form):
        if self.is_valid(form):
            if self.is_duplicate(form):
                self.save_form(form, duplicate_forms_path)
                print(f"Duplicate form: {form}")
            else:
                self.valid_forms.append(form)
                print(f"Valid form: {form}")
                response = requests.post("http://localhost:5004/formulario", json=form)
                return response.json(), response.status_code
        else:
            self.invalid_forms.append(form)
            self.save_form(form, invalid_forms_path)
            print(f"Invalid form: {form}")

    def is_valid(self, form):
        return len(form.keys()) == 20

    def is_duplicate(self, form):
        response = requests.get(f"http://localhost:5004/formulario/{form['id']}")
        return response.status_code == 200

    def save_form(self, form, path):
        form_id = form.get('id')
        with open(os.path.join(path, f"{form_id}.json"), 'w') as f:
            json.dump(form, f)

    def process_forms(self, forms):
        with ThreadPoolExecutor() as executor:
            executor.map(self.validate_form, forms)

validation = Validation()

@app.route('/validate', methods=['POST'])
def validate_form():
    data = request.json
    validation.process_forms([data])
    return jsonify({'message': 'Validation completed'}), 200

if __name__ == "__main__":
    app.run(port=5003)
