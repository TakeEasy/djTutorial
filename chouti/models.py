from django.db import models


# Create your models here.

class EmailCode(models.Model):
    email = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    content = models.CharField(max_length=32)
    stime = models.DateTimeField('send date')
    status = models.IntegerField(default=0)
    times = models.IntegerField(default=0)

    def __str__(self):
        return '%s,%s,%s,%s,%s' % (self.email, self.category, self.content, self.stime, self.status)


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    sex = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    sign = models.CharField(max_length=200)
    ctime = models.DateTimeField('create time')

    def __str__(self):
        return self.username

    class Meta:
        indexes= [
            models.Index(fields=['username','password']),
            models.Index(fields=['email','password'])
        ]


class NewsType(models.Model):
    caption = models.CharField(max_length=32)
    ctime = models.DateTimeField('create tiem')

    def __str__(self):
        return self.caption


class News(models.Model):
    publishuser = models.ForeignKey(UserInfo, on_delete=models.CASCADE,related_name='publishNews')
    newstype = models.ForeignKey(NewsType, on_delete=models.CASCADE)
    favorusers = models.ManyToManyField(UserInfo,through='Favor',related_name='favorNews')

    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    content = models.CharField(max_length=150)
    ctime = models.DateTimeField('create time')

    def __str__(self):
        return self.title


class Favor(models.Model):
    favoruser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    ctime = models.DateTimeField('favor time')

    def __str__(self):
        return '%s like %s' % (self.favoruser.username, self.news.title)


class Comment(models.Model):
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    replay_id = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='replays')
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    device = models.CharField(max_length=32)
    content = models.CharField(max_length=150)
    ctime = models.DateTimeField('create time')

    def __str__(self):
        return '%s replay %s' % (self.userinfo.username, self.news.title)

