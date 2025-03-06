from django import forms
from .models import Order
from decimal import Decimal


class OrderForm(forms.ModelForm):
    items_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Пример: Пицца - 500\nКофе - 150'
        }),
        label="Блюда (название - цена)"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'status', 'items_text']

    def clean_items_text(self):
        items_text = self.cleaned_data['items_text']
        items = []
        for line in items_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                name, price = line.split(' - ')
                # Преобразуем в Decimal для точности, затем в float для JSON
                price = float(Decimal(price).quantize(Decimal('0.00')))
                items.append({'name': name, 'price': price})
            except ValueError:
                raise forms.ValidationError(f"Неверный формат строки: '{line}'")
        return items

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.items = self.cleaned_data['items_text']
        # Теперь calculate_total_price() возвращает Decimal
        instance.total_price = instance.calculate_total_price().quantize(Decimal('0.00'))
        if commit:
            instance.save()
        return instance