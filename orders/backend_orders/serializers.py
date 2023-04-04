from rest_framework import serializers

from .models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели контакта.
    Атрибуты:
        model (Contact): модель контакта
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
        extra_kwargs (dict): дополнительные аргументы
    """
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Атрибуты:
        model (User): модель пользователя
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
    """
    contacts = ContactSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'company', 'position', 'contacts')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели категории.
    Атрибуты:
        model (Category): модель категории
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
    """
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ShopSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели магазина.
    Атрибуты:
        model (Shop): модель магазина
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
    """
    class Meta:
        model = Shop
        fields = ('id', 'name', 'state',)
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели продукта.
    Атрибуты:
        model (Product): модель продукта
        fields (tuple): поля сериализации
        category (StringRelatedField): категория продукта
    """
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели параметра продукта.
    Атрибуты:
        model (ProductParameter): модель параметра продукта
        fields (tuple): поля сериализации
        parameter (StringRelatedField): параметр продукта
    """
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели информации о продукте.
    Атрибуты:
        product (ProductSerializer): сериализатор продукта, связанного с информацией о продукте
        product_parameters (ProductParameterSerializer): сериализатор списка параметров продукта
        model (str): модель продукта
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
    """
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели элемента заказа.
    Атрибуты:
        model (OrderItem): модель элемента заказа
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
        extra_kwargs (dict): дополнительные настройки полей
    """
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):
    """
    Сериализатор для создания элемента заказа.
    Атрибуты:
        product_info (ProductInfoSerializer): сериализатор информации о продукте (только для чтения)
    """
    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели заказа.
    Атрибуты:
        model (Order): модель заказа
        fields (tuple): поля сериализации
        read_only_fields (tuple): только для чтения поля
    """
    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)

    total_sum = serializers.IntegerField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'total_sum', 'contact',)
        read_only_fields = ('id',)
