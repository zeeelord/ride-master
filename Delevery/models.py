from django.db import models
from Userprofile.models import UserModel
from background_task import background
# from django.contrib.auth.models import User
import requests
# Create your models here.


class Order(models.Model):

    CHOICES = {
        ('1', 'Pending'),
        ('2', 'Failed'),
        ('3', 'Successful'),
    }

    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField()
    sender_name = models.CharField(max_length=225)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=225)
    sender_address = models.CharField(max_length=225)

    receiver_name = models.CharField(max_length=225)
    receiver_email = models.EmailField()
    receiver_phone = models.CharField(max_length=225)
    receiver_address = models.CharField(max_length=225)

    content = models.TextField()

    created = models.DateTimeField(auto_now=True)


class BaseModel(models.Model):
    # id = models.IntegerField()
    deleted = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    by = models.CharField(max_length=50, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    dead = models.CharField(max_length=50, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    kid = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=225, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=225, blank=True, null=True)
    parts = models.CharField(max_length=225, blank=True, null=True)
    descendants = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)

    # test = models.CharField(max_length=250)
    # text = models.TextField()

    def __str__(self):
        return self.title


def get_data(id):

    url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"

    payload = "{}"
    response = requests.request("GET", url, data=payload)
    # print(response.json())
    data = response.json()
    # print(data)
    return data


def get_all_jobs():

    try:
        urls = ["https://hacker-news.firebaseio.com/v0/jobstories.json", "https://hacker-news.firebaseio.com/v0/topstories.json",
                "https://hacker-news.firebaseio.com/v0/askstories.json", "https://hacker-news.firebaseio.com/v0/showstories.json"]

        payload = "{}"
        for url in urls:
            response = requests.request("GET", url, data=payload)

            data = response.json()

            for i in data:
                stories = get_data(id=i)
                if BaseModel.objects.all().exists():
                    for k in BaseModel.objects.all():
                        if stories['type'] == 'job':
                            if k.id != stories['id']:
                                BaseModel.objects.create(by=stories['by'], id=stories['id'], time=stories['time'],
                                                         title=stories['title'], type=stories['type'], url=stories['url'],
                                                         score=stories['score'])
                        elif stories['type'] == 'story':
                            if k.id != stories['id']:
                                BaseModel.objects.create(by=stories['by'], id=stories['id'], type=stories['type'],
                                                         descendants=stories['descendants'], score=stories['score'],
                                                         time=stories['time'], title=stories['titles'],
                                                         url=stories['url'])
                        elif stories['type'] == 'comment':
                            if k.id != stories['id']:
                                BaseModel.objects.create(by=stories['by'], id=stories["id"], parent=stories['parent'],
                                                         text=stories['text'], time=stories['time'], type=stories['type'])
                        elif stories['type'] == 'poll':
                            if k.id != stories['id']:
                                BaseModel.objects.create(by=stories['by'], descendants=stories['descendants'], id=stories['id'],
                                                         score=stories['score'], text=stories['text'], time=stories['time'],
                                                         title=stories['title'], type=stories['type'])
                        elif stories['type'] == 'pollopt':
                            if k.id != stories['id']:
                                BaseModel.objects.create(by=stories['by'], id=stories['id'], parent=stories['parent'],
                                                         score=stories['score'], text=stories['text'], time=stories['time'],
                                                         type=stories['type'])
                else:
                    if stories['type'] == 'job':
                        # if k.id != stories['id']:
                        BaseModel.objects.create(by=stories['by'], id=stories['id'], time=stories['time'],
                                                 title=stories['title'], type=stories['type'], url=stories['url'],
                                                 score=stories['score'])
                    elif stories['type'] == 'story':
                        # if k.id != stories['id']:
                        BaseModel.objects.create(by=stories['by'], id=stories['id'], type=stories['type'],
                                                 descendants=stories['descendants'], score=stories['score'],
                                                 time=stories['time'], title=stories['titles'],
                                                 url=stories['url'])
                    elif stories['type'] == 'comment':
                        # if k.id != stories['id']:
                        BaseModel.objects.create(by=stories['by'], id=stories["id"], parent=stories['parent'],
                                                 text=stories['text'], time=stories['time'], type=stories['type'])
                    elif stories['type'] == 'poll':
                        # if k.id != stories['id']:
                        BaseModel.objects.create(by=stories['by'], descendants=stories['descendants'],
                                                 id=stories['id'],
                                                 score=stories['score'], text=stories['text'], time=stories['time'],
                                                 title=stories['title'], type=stories['type'])
                    elif stories['type'] == 'pollopt':
                        # if k.id != stories['id']:
                        BaseModel.objects.create(by=stories['by'], id=stories['id'], parent=stories['parent'],
                                                 score=stories['score'], text=stories['text'], time=stories['time'],
                                                 type=stories['type'])

    except:
        data = "Can't Reach"


@background
def notify_user():
    get_all_jobs()
    print("Done")


notify_user(repeat=30000)
