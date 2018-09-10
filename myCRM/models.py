from django.db import models
from django.contrib.auth.models import User,BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
# class UserProfile(models.Model):
#     '''用户信息表'''
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     name=models.CharField(max_length=32)
#     roles=models.ManyToManyField("Role",null=True,blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name="用户信息表"
#         verbose_name_plural="用户信息表"

class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role", null=True, blank=True)
    password = models.CharField(_('password'), max_length=128,help_text=mark_safe("<a href='change/password'>修改密码</a>"))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=64, unique=True)
    menus=models.ManyToManyField('Menu',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="角色表"
        verbose_name_plural="角色表"


class Customer(models.Model):
    '''客户表'''
    name = models.CharField(max_length=32, null=True, blank=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, null=True, blank=True)
    wechat = models.CharField(max_length=64, unique=True)
    weChar_name = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    source_choice = ((0, '转介绍'),
                     (1, 'QQ群'),
                     (2, '官网'),
                     (3, '百度推广'),
                     (4, '51CTO'),
                     (5, '知乎'),
                     (6, '市场推广'),
                     (7, '其他'))
    source = models.SmallIntegerField(choices=source_choice)
    referral_from = models.CharField(verbose_name='介绍人', max_length=64, null=True, blank=True)
    consult_course = models.ForeignKey("Course", verbose_name='咨询课程', null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField("Tag", null=True, blank=True)
    content = models.TextField(verbose_name='咨询详情')
    consultant = models.ForeignKey("UserProfile",null=True, on_delete=models.SET_NULL)
    memo = models.TextField(null=True, blank=True)
    status_choice=((0,'未报名'),
                   (1,'已报名'),
                   (2,'已GG'))
    status = models.SmallIntegerField(choices=status_choice,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def enroll(self,id):
        return mark_safe("<a href='/mycrm/customer/%s/enroll'>报名</a>"%id)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name="客户表"
        verbose_name_plural="客户表"


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="标签"
        verbose_name_plural="标签"


class CustomerFollowUp(models.Model):
    '''客户追踪表'''
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", null=True,on_delete=models.SET_NULL)
    intention_choices = ((0, '2周内报名'),
                         (1, '1个月内报名'),
                         (2, '近期无报名计划'),
                         (3, '已报名'),
                         (4, '已在其他地方报名'),
                         (5, '已拉黑'),)
    intention = models.SmallIntegerField(choices=intention_choices)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<%s : %s>" % (self.customer, self.intention)

    class Meta:
        verbose_name="客户追踪表"
        verbose_name_plural="客户追踪表"


class Enrollment(models.Model):
    '''报名表'''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey('ClassList', null=True,on_delete=models.SET_NULL, verbose_name='所报班级')
    consulant = models.ForeignKey('UserProfile', null=True,on_delete=models.SET_NULL, verbose_name='课程顾问')
    contract_agreed = models.BooleanField(default=False, verbose_name='学生已同意条款')
    contract_approved = models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name="报名表"
        verbose_name_plural="报名表"


class Payment(models.Model):
    '''交钱记录'''
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", null=True,on_delete=models.SET_NULL)
    amout = models.PositiveIntegerField(default=500, verbose_name="数额")
    consultant = models.ForeignKey("UserProfile", null=True,on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.amout)

    class Meta:
        verbose_name="交钱表"
        verbose_name_plural="交钱表"


class Course(models.Model):
    '''课程表'''
    name = models.CharField(unique=True, max_length=64)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="课程周期(月)")
    outline = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="课程表"
        verbose_name_plural="课程表"


class Branch(models.Model):
    '''校区'''
    name = models.CharField(unique=True, max_length=128)
    address = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="校区表"
        verbose_name_plural="校区表"


class ClassList(models.Model):
    '''班级表'''
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE, verbose_name='分校')
    category_choices = ((0, '面授()'),
                        (1, '面授(周末)'),
                        (2, '网络班'),)
    category = models.SmallIntegerField(choices=category_choices)
    course = models.ForeignKey("Course", null=True,on_delete=models.SET_NULL)
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    start_date = models.DateTimeField(verbose_name='开班日期')
    end_date = models.DateTimeField(verbose_name='结束日期', null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name="班级表"
        verbose_name_plural="班级表"


class CourseRecord(models.Model):
    '''上课记录表'''
    witch_class = models.ForeignKey('ClassList', verbose_name='班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几天")
    teacher = models.ForeignKey('UserProfile', null=True,on_delete=models.SET_NULL)
    has_homwork = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, null=True, blank=True)
    homework_content = models.TextField(null=True, blank=True)
    outline = models.TextField(verbose_name='课程大纲')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.witch_class, self.day_num)

    class Meta:
        unique_together = ('witch_class', 'day_num')
        verbose_name="上课记录表"
        verbose_name_plural="上课记录表"


class StudyRecord(models.Model):
    '''学习记录'''
    student = models.ForeignKey("Enrollment", on_delete=models.CASCADE)
    course_record = models.ForeignKey('CourseRecord', null=True,on_delete=models.SET_NULL)
    attendence_choises = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '迟到'),)
    attendence = models.IntegerField(choices=attendence_choises)

    score_choises = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'C+'),
                     (60, 'C'),
                     (40, 'C-'),
                     (-50, 'D'),
                     (-100, 'Copy'),
                     (0, 'N/A'),)
    score = models.SmallIntegerField(choices=score_choises)
    memo = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together=("student","course_record")
        verbose_name="学习记录"
        verbose_name_plural="学习记录"

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)


class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_type_choices=((0,'pathname'),(1,'url'))
    url_type=models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return '%s:%s' % (self.name, self.url_name)

    class Meta:
        verbose_name='菜单表'
        verbose_name_plural='菜单表'
