import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Order

# Country choices with flag data attributes
COUNTRY_CHOICES = [
    ('', 'Select Country'),
    ('US', 'United States'),
    ('CA', 'Canada'),
]

# US States
US_STATES = [
    ('', 'Select State'),
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
    ('CA', 'California'), ('CO', 'Colorado'), ('CT',
                                               'Connecticut'), ('DE', 'Delaware'),
    ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN',
                                                  'Minnesota'), ('MS', 'Mississippi'),
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM',
                                                    'New Mexico'), ('NY', 'New York'),
    ('NC', 'North Carolina'), ('ND',
                               'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI',
                                               'Rhode Island'), ('SC', 'South Carolina'),
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA',
                                            'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
]

# Canadian Provinces
CA_PROVINCES = [
    ('', 'Select Province'),
    ('AB', 'Alberta'), ('BC', 'British Columbia'), ('MB', 'Manitoba'),
    ('NB', 'New Brunswick'), ('NL', 'Newfoundland and Labrador'),
    ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('PE', 'Prince Edward Island'),
    ('QC', 'Quebec'), ('SK', 'Saskatchewan'), ('NT', 'Northwest Territories'),
    ('NU', 'Nunavut'), ('YT', 'Yukon'),
]

def validate_phone(value):
    """Validate phone number: digits, spaces, dashes, parentheses, plus sign only."""
    if not value:
        return
    cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
    if not cleaned.isdigit():
        raise ValidationError(
            'Phone number can only contain digits, spaces, dashes, parentheses, and + sign.')
    if len(cleaned) < 7 or len(cleaned) > 15:
        raise ValidationError('Phone number must be between 7 and 15 digits.')


def validate_zip_code(value):
    """Validate zip/postal code format."""
    if not value:
        return
    # Accept US 5-digit or 5+4 format, or Canadian A#A #A# format
    us_pattern = r'^\d{5}(-\d{4})?$'
    ca_pattern = r'^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$'
    if not re.match(us_pattern, value) and not re.match(ca_pattern, value):
        raise ValidationError(
            'Enter a valid ZIP code (e.g. 12345 or 12345-6789) or Canadian postal code (e.g. A1A 1A1).'
        )


class OrderCreateForm(forms.ModelForm):
    """Checkout form with country/state dropdowns and proper validation."""

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        error_messages={'required': 'Please select a country.'},
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_country',
        })
    )

    first_name = forms.CharField(
        max_length=100,
        error_messages={'required': 'First name is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'First Name',
            'pattern': '[A-Za-zÀ-ÿ\-\'\s]+',
            'title': 'First name can only contain letters, spaces, hyphens, and apostrophes.',
        })
    )

    last_name = forms.CharField(
        max_length=100,
        error_messages={'required': 'Last name is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Last Name',
            'pattern': '[A-Za-zÀ-ÿ\-\'\s]+',
            'title': 'Last name can only contain letters, spaces, hyphens, and apostrophes.',
        })
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address (e.g. name@example.com).',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'Email',
        })
    )

    phone = forms.CharField(
        required=True,
        validators=[validate_phone],
        error_messages={'required': 'Phone number is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Phone',
            'type': 'tel',
            'pattern': '[\+\d\s\-\(\)]{7,20}',
            'title': 'Enter a valid phone number (7-15 digits).',
        })
    )

    address = forms.CharField(
        max_length=250,
        error_messages={'required': 'Street address is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Street Address',
        })
    )

    city = forms.CharField(
        max_length=100,
        error_messages={'required': 'City is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'City',
        })
    )

    zip_code = forms.CharField(
        max_length=20,
        validators=[validate_zip_code],
        error_messages={'required': 'ZIP / postal code is required.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'ZIP Code / Postal Code',
        })
    )

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'zip_code', 'country',
        ]
        widgets = {
            'state': forms.Select(choices=[], attrs={
                'class': 'form-control', 'id': 'id_state',
            }),
        }

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        if value and not re.match(r'^[A-Za-zÀ-ÿ\-\'\s]+$', value):
            raise ValidationError(
                'First name can only contain letters, spaces, hyphens, and apostrophes.')
        return value

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        if value and not re.match(r'^[A-Za-zÀ-ÿ\-\'\s]+$', value):
            raise ValidationError(
                'Last name can only contain letters, spaces, hyphens, and apostrophes.')
        return value

    def clean_email(self):
        value = self.cleaned_data.get('email', '').strip()
        return value

    def clean_phone(self):
        value = self.cleaned_data.get('phone', '').strip()
        if not value:
            raise ValidationError('Phone number is required.')
        return value

    def clean_zip_code(self):
        value = self.cleaned_data.get('zip_code', '').strip()
        country = self.cleaned_data.get('country', '')
        if country == 'US':
            if not re.match(r'^\d{5}(-\d{4})?$', value):
                raise ValidationError(
                    'Enter a valid US ZIP code (e.g. 12345 or 12345-6789).')
        elif country == 'CA':
            if not re.match(r'^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$', value):
                raise ValidationError(
                    'Enter a valid Canadian postal code (e.g. A1A 1A1).')
        return value

    def clean_state(self):
        value = self.cleaned_data.get('state', '')
        country = self.cleaned_data.get('country', '')
        if country == 'US':
            valid_states = [code for code, _ in US_STATES if code]
            if not value or value not in valid_states:
                raise ValidationError('Please select a valid US state.')
        elif country == 'CA':
            valid_provinces = [code for code, _ in CA_PROVINCES if code]
            if not value or value not in valid_provinces:
                raise ValidationError(
                    'Please select a valid Canadian province/territory.')
        else:
            raise ValidationError('Please select a country first.')
        return value

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        if not country:
            raise ValidationError('Please select a country.')
        return cleaned_data
