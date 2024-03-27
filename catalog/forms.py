from django import forms
from django.core.exceptions import ValidationError

import datetime

# Django Translations Functions (Other topic, only here for knowledge)
from django.utils.translation import gettext_lazy as _

from .models import BookInstance

class RenewBook(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    # Validate Renewal Date (standard: clean_fieldname())
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Validation of past dates
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        # Validation of longer dates (longer than 4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data
    

# Equivalent as RenewBook
class RenewBookModelForm(forms.ModelForm):
    
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New Renewal Date')}
        help_texts = {'due_back':_('Enter a date between now and 4 weeks (default 3).')}
