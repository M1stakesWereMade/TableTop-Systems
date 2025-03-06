from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    items_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Пример: Пицца - 500\nКофе - 150'
        }),
        label="Блюда (название - цена)"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'status']

    def clean_items_text(self):
        items_text = self.cleaned_data['items_text']
        items = []
        for line in items_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                name, price = line.split(' - ')
                price = float(price)
                items.append({'name': name, 'price': price})
            except ValueError:
                raise forms.ValidationError(
                    f"Неверный формат строки: '{line}'. Используйте 'Название - Цена'"
                )
        return items

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.items = self.cleaned_data['items_text']
        if commit:
            instance.save()
        return instance