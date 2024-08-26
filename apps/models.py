from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import TextChoices, CharField, CASCADE, Model, DateTimeField, ForeignKey, SlugField, ImageField, \
    TextField, FloatField, IntegerField, SET_NULL, BooleanField, PositiveIntegerField, Index
from django.template.defaultfilters import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        # user.save()
        return user


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", 'Admin'
        OPERATOR = "operator", 'Operator'
        MANAGER = "manager", 'Manager'
        DRIVER = "driver", 'Driver'
        USER = "user", 'User'

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone_number = CharField(max_length=12, unique=True)
    district = ForeignKey('apps.District', CASCADE, related_name='users', null=True)
    image = ImageField(upload_to='users/')

    @property
    def wishlist_all(self):
        return self.wishlists.values_list('product_id', flat=True)


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, unique=True)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_et = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Category(BaseSlugModel, BaseModel):
    image = ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseSlugModel, BaseModel):
    description = TextField()
    price = FloatField()
    quantity = IntegerField()
    payment = FloatField()
    for_stream_price = FloatField(default=1000)
    category = ForeignKey('apps.Category', CASCADE, to_field='slug', related_name='products')
    bonus = FloatField()

    @property
    def first_image(self):
        return self.images.first()

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')


class Stream(BaseModel):
    name = CharField(max_length=255)
    discount = FloatField()
    count = IntegerField(default=0)
    product = ForeignKey('apps.Product', SET_NULL, null=True, related_name='streams')
    owner = ForeignKey('apps.User', CASCADE, related_name='streams')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class Order(BaseModel):
    class StatusType(TextChoices):
        NEW = 'new', 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = "archived", 'Archived'

    quantity = IntegerField(default=1)
    status = CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW)
    full_name = CharField(max_length=255)
    stream = ForeignKey('apps.Stream', SET_NULL, null=True, blank=True, default=None, related_name='orders')
    phone_number = CharField(max_length=20)
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')
    user = ForeignKey('apps.User', CASCADE, related_name='orders')


class WishList(BaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='wishlists', to_field='slug')
    user = ForeignKey('apps.User', CASCADE, related_name='wishlists')


class Comment(Model):
    message = SlugField()
    content_type = ForeignKey(ContentType, CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.message

    class Meta:
        indexes = [
            Index(fields=["content_type", "object_id"]),
        ]


class SiteSettings(Model):
    deliver_price = FloatField(default=0)
