from django import forms
from edc_appointment.form_validators import AppointmentFormValidator
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Appointment


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    appointment_model = 'flourish_child.appointment'

    form_validator_cls = AppointmentFormValidator

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earlist_appt_date = (self.instance.timepoint_datetime -
                                 visit_definition.rlower)
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper)

            if (cleaned_data.get('appt_datetime') < earlist_appt_date
                    or cleaned_data.get('appt_datetime') > latest_appt_date):
                raise forms.ValidationError(
                            'The appointment datetime cannot be outside the window period, '
                            'please correct. See earliest, ideal and latest datetimes below.')
        super().clean()

    class Meta:
        model = Appointment
        fields = '__all__'
