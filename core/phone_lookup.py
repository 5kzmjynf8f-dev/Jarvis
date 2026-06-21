import phonenumbers
from phonenumbers import geocoder, carrier


class PhoneLookup:

    def analyze(self, number):

        try:

            parsed = phonenumbers.parse(
                number,
                None
            )

            return (
                f"""
Number:
{number}

Valid:
{phonenumbers.is_valid_number(parsed)}

Country:
{geocoder.description_for_number(parsed,'en')}

Carrier:
{carrier.name_for_number(parsed,'en')}
"""
            )

        except Exception as e:

            return f"Error: {e}"