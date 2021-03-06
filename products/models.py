from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """A model for product categories"""
    name = models.CharField(max_length=250, db_index=True)
    objects = models.Manager()

    class Meta:
        """ Correct plural for category in admin"""
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """A model for the products"""
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        """Order by product created"""
        ordering = ('-created',)

    def get_absolute_url(self):
        """
        Creates dynamic urls for products
        """
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return str(self.name)


class ProductReview(models.Model):
    """A model for product reviews"""
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='reviews')
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    select_rating = (
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )
    rating = models.IntegerField(choices=select_rating, default=3)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Data ordering"""
        ordering = ['-date_added']

    def __str__(self):
        return str(self.title)
