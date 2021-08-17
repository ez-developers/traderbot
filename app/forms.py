from django import forms

class CustomActionForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput,
                             initial='delete_selected',
                             label='Delete Selected'
                             )
    select_across = forms.BooleanField(
                                       label='',
                                       required=False,
                                       initial=0,
                                       widget=forms.HiddenInput({'class': 'select-across'}),
                                       )