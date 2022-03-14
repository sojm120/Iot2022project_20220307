from django.db import models


class Cust(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    pwd = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    birth = models.DateField()
    gender = models.CharField(max_length=1)
    email = models.CharField(unique=True, max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(unique=True, max_length=13)
    host_flag = models.IntegerField()

    class Meta:
        db_table = 'db_cust'


class Cate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'db_cate'


class Rest(models.Model):
    id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Cust, on_delete=models.CASCADE)
    cate = models.ForeignKey(Cate, on_delete=models.CASCADE)
    rest_name = models.CharField(max_length=20)
    reg_num = models.CharField(unique=True, max_length=10)
    host_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    restindex = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    openhour = models.CharField(max_length=100, blank=True, null=True)
    breakhour = models.CharField(max_length=100, blank=True, null=True)
    restimg = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'db_rest'


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE)
    cust = models.ForeignKey(Cust, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    regdate = models.DateField(auto_now=True)
    s_rating = models.IntegerField()
    m_rating = models.IntegerField()
    p_rating = models.IntegerField()
    menu = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    purpose = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'db_review'


class Imgpath(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    path = models.CharField(max_length=100)

    class Meta:
        db_table = 'db_imgpath'


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    cust = models.ForeignKey('Cust', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = 'db_board'


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    rest = models.ForeignKey('Rest', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    menuimg = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'db_menu'
