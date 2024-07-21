from concurrent.futures import ThreadPoolExecutor


class Validation:
    def __init__(self):
        self.valid_forms = []
        self.invalid_forms = []

    def validate_form(self, form):
        if self.is_valid(form):
            self.valid_forms.append(form)
            print(f"Valid form: {form}")
        else:
            self.invalid_forms.append(form)
            print(f"Invalid form: {form}")

    def is_valid(self, form):
        return "valid" in form

    def process_forms(self, forms):
        with ThreadPoolExecutor() as executor:
            executor.map(self.validate_form, forms)

    def run(self, forms):
        self.process_forms(forms)
        print("Valid forms:", self.valid_forms)
        print("Invalid forms:", self.invalid_forms)


if __name__ == "__main__":
    forms = ["form1 valid", "form2 invalid", "form3 valid"]
    validation = Validation()
    validation.run(forms)
