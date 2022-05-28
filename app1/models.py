from django.db import models
# Create your models here.

class Company(models.Model):
    company_name=models.CharField(default="", max_length=200)
    company_email=models.EmailField(default="", max_length=200)
    company_cno=models.PositiveIntegerField(default=0)
    company_add=models.TextField(default="")
    join_date=models.DateField(auto_now=True,blank=True, null=True)
    profile=models.ImageField(upload_to="comp_profile/",default="",max_length=200,blank=True,null=True)
    company_pass=models.CharField(default="",max_length=200)
    def __str__(self):
        return self.company_name

class CompanyCustomer(models.Model):
    comp=models.ForeignKey('Company', on_delete=models.CASCADE, blank=True,null=True)
    cust_name=models.CharField(default="", max_length=200)
    cust_email=models.EmailField(default="", max_length=200)
    cust_con=models.PositiveIntegerField(default=0)
    cust_add1=models.TextField(default="")
    cust_add2=models.TextField(default="")
    regi_date=models.DateTimeField(auto_now_add=True,blank=True, null=True)
    cust_profile=models.ImageField(upload_to="comp_profile/",default="",max_length=200,blank=True,null=True)
    cust_pass=models.CharField(default="",max_length=200)
    def __str__(self):
        return self.cust_name

class CompanyProduct(models.Model):
    comp=models.ForeignKey('Company', on_delete=models.CASCADE, blank=True,null=True)
    pro_name=models.CharField(default="", max_length=200)
    pro_price=models.PositiveIntegerField(default=0)
    pro_qty=models.PositiveIntegerField(default=0)
    pro_img=models.ImageField(upload_to="product_img/",default="",max_length=200,blank=True,null=True)
    def __str__(self):
        return self.pro_name

class CustomerOrder(models.Model):
    comp = models.ForeignKey('Company',on_delete=models.CASCADE,blank=True,null=True)
    cust = models.ForeignKey('CompanyCustomer',on_delete=models.CASCADE,blank=True,null=True)
    prod = models.ForeignKey('CompanyProduct',on_delete=models.CASCADE,blank=True,null=True)
    tot_price = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    order_dt = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.CharField(default=False,max_length=20)
