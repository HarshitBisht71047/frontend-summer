from django import forms

class UploadPDFForm(forms.Form):
    pdf_file = forms.FileField(
        label='Upload your blood report PDF',
        widget=forms.FileInput(attrs={'accept': '.pdf'})
    )

    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return file

