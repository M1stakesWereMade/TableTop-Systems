from django import forms
from .models import Order
from decimal import Decimal


class OrderForm(forms.ModelForm):
    """
    Форма для создания/редактирования заказа.

    Attributes:
        items_text (CharField): Поле для ввода списка блюд в текстовом формате.
    """
    items_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Пример: Пицца - 500\nКофе - 150',
            }
        ),
        label="Блюда (название - цена)",
    )

    class Meta:
        model = Order
        fields = [
            'table_number',
            'status',
            'items_text',
        ]

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['items_text'] = self.instance.items_text

    def clean_items_text(self):
        """
        Валидация и парсинг поля items_text.

        Преобразует текст в формате "Название - Цена" в список словарей.

        Returns:
            list: Список блюд в формате [{'name': str, 'price': float}].

        Raises:
            ValidationError: При некорректном формате строки.
        """
        items_text = self.cleaned_data['items_text']
        items = []
        for line in items_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                name, price = line.split(' - ')
                price = float(
                    Decimal(price).quantize(Decimal('0.00'))
                )
                items.append({'name': name, 'price': price})
            except ValueError:
                raise forms.ValidationError(
                    f"Неверный формат строки: '{line}'"
                )
        return items

    def save(self, commit=True):
        """
        Переопределенный метод сохранения формы.

        Args:
            commit (bool): Флаг сохранения в БД.

        Returns:
            Order: Сохраненный экземпляр заказа.
        """
        instance = super().save(commit=False)
        instance.items = self.cleaned_data['items_text']
        instance.total_price = (
            instance.calculate_total_price().quantize(Decimal('0.00'))
        )
        if commit:
            instance.save()
        return instance
