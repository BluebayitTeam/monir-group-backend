from PIL import Image
from django.db import models
from django.conf import settings

from authentication.models import Role
from phonenumber_field.modelfields import PhoneNumberField
import os
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.

class MenuItem(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    position = models.IntegerField(unique=True, null=True, blank=True)
    menu_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    translate = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    exact = models.BooleanField(default=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'MenuItems'
        ordering = ['position']

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.title()
        if self.translate:
            self.translate = self.translate.title()
        super().save(*args, **kwargs)





class RoleMenu(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'RoleMenus'
        ordering = ('-id', )

    def __str__(self):
        return str(self.id)




class GeneralSetting(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    site_name = models.CharField(max_length=100, null=True, blank=True)
    site_address = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email2 = models.EmailField(null=True, blank=True)
    email3 = models.EmailField(null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    phone3 = models.CharField(max_length=20, null=True, blank=True)


    favicon = models.ImageField(upload_to='favicons/', null=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    footer_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    address = models.TextField( null=True, blank=True)
    address2 = models.TextField( null=True, blank=True)

    google_url = models.CharField(max_length=500, null=True, blank=True)
    facebook_url = models.CharField(max_length=500, null=True, blank=True)
    twitter_url = models.CharField(max_length=500, null=True, blank=True)
    linkedin_url = models.CharField(max_length=500, null=True, blank=True)
    instagram_url = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        get_latest_by = 'created_at'
        verbose_name_plural = 'GeneralSettings'
        ordering = ('-id', )

    def __str__(self):
        return str(self.id)




class HomePageSlider(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    subtitle = models.CharField(max_length=500, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='siteSettings/homePageSlider/', null=True, blank=True)
    details = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'HomepageSliders'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)




class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=500, null=True, blank=True)


    message = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Contacts'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    






class ServiceSlider(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/homePageSlider/', null=True, blank=True)
    details = models.TextField( null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Service Sliders'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)



class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    title = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='siteSettings/portfolio/', null=True, blank=True)

    is_portfolio = models.BooleanField(default=False)
    serial_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)


    

class About(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/about/', null=True, blank=True)
    icon = models.TextField( null=True, blank=True)
    content_type = models.TextField( null=True, blank=True)

    details = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'About'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    

class MissionVission(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/mission/', null=True, blank=True)
    icon = models.TextField( null=True, blank=True)

    details = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'MissionVission'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    

class Client(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='siteSettings/client/', null=True, blank=True)
    site_link = models.CharField(max_length=200, null=True, blank=True)
    country_name = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Client'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    


class Testimonial(models.Model):
    review = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='siteSettings/testimonial/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Testimonial'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    


class Gallery(models.Model):
    image = models.FileField(upload_to='siteSettings/gallery/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Gallery'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.image:
            # Open image from in-memory file
            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((1080, 1080))

            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=50)
            buffer.seek(0)

            filename = os.path.splitext(os.path.basename(self.image.name))[0] + ".webp"
            self.image.save(filename, ContentFile(buffer.read()), save=False)
            buffer.close()

        super().save(*args, **kwargs)
        

class Profile(models.Model):
    image = models.FileField(upload_to='siteSettings/profile/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Profile'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.image:
            # Open image from in-memory file
            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((1080, 1080))

            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=50)
            buffer.seek(0)

            filename = os.path.splitext(os.path.basename(self.image.name))[0] + ".webp"
            self.image.save(filename, ContentFile(buffer.read()), save=False)
            buffer.close()

        super().save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/product/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    serial_number = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    


class Team(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    employee_id = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=500, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/team/', null=True, blank=True)

    designation = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Team'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)
    
class OurCompanyMessage(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/our_company_message/', null=True, blank=True)
    description = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'OurCompanyMessage'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)


class SisterConcern(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='siteSettings/sister_concern_image/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'SisterConcern'
        get_latest_by = 'created_at'
        ordering = ('-id', )
    
    def __str__(self):
        return str(self.id)


class SisterConcernImage(models.Model):
    sister_concern = models.ForeignKey(SisterConcern, on_delete=models.CASCADE, related_name='sister_concern_images')
    image = models.FileField(upload_to='siteSettings/sister_concern_image/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'SisterConcernImages'
        ordering = ('-id', )

    def __str__(self):
        return str(self.id)
        