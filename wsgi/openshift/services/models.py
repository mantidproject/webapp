from django.db import models
import os
import settings
import json
import requests
import hashlib

# Create your models here.


class Location(models.Model):
    ip = models.CharField(max_length=32, unique=True)
    city = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)

    def __unicode__(self):
        return "IP: " + self.ip + " City/Region/Country: " + self.city + "/" \
            + self.region + "/" + self.country

    def create(self, ip):
        jsonData = requests.get("http://ipinfo.io/%s/json/" % ip).content
        apiReturn = json.loads(jsonData)
        print 'Location:', jsonData
        if apiReturn.has_key('loc'):
            latitude, longitude = apiReturn['loc'].strip().split(',')
        else:
            latitude, longitude = ('0','0') # default is in the Gulf of Guinea
        city = apiReturn.get('city', '')
        region = apiReturn.get('region', '')
        country_code = apiReturn.get('country', '')
        if len(country_code) > 0:
            with open(os.path.join(settings.PROJECT_DIR, \
                                   'countrynames.json'), 'r') as country_code_file:
                      country_IDs = json.loads(country_code_file.read())
            country = country_IDs[country_code]
        else:
            country = ''
        ipHash = hashlib.md5(ip).hexdigest()
        entry = Location(ip=ipHash, city=city, region=region,
                         country=country, longitude=longitude, latitude=latitude)
        entry.save()


class Message(models.Model):
    author = models.CharField(max_length=20)
    text = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.author


class Usage(models.Model):
    # md5 ex: "c5a9b601408709f47417bcba3571262b"
    uid = models.CharField(max_length=32, help_text="md5 version of username")
    # md5 ex: "7defb184ceadab4e79eff323359ad373"
    host = models.CharField(max_length=32, help_text="md5 version of hostname")
    # ex: "2014-12-08T18:50:35.817942000"
    dateTime = models.DateTimeField(db_index=True)
    osName = models.CharField(max_length=32)        # ex: "Linux"
    osArch = models.CharField(max_length=16)        # ex: "x86_64"
    # ex: "3.17.4-200.fc20.x86_64"
    osVersion = models.CharField(max_length=32)
    ParaView = models.CharField(max_length=16)      # ex: "3.98.1"
    mantidVersion = models.CharField(max_length=32)  # ex: "3.2.20141208.1820"
    # sha1 ex: "e9423bdb34b07213a69caa90913e40307c17c6cc"
    mantidSha1 = models.CharField(
        max_length=40, help_text="sha1 for specific mantid version")
    # ex: "Fedora 20 (Heisenbug)"
    osReadable = models.CharField(max_length=80, default="", blank=True)
    application = models.CharField(max_length=80, default="", blank=True)
    component = models.CharField(max_length=80, default="", blank=True)
    ip = models.CharField(max_length=32, default="", blank=True)


class FeatureUsage(models.Model):
    # type ex: "Algorithm,Interface, Feature"
    type = models.CharField(
        max_length=32, help_text="Algorithm,Interface, Feature")
    name = models.CharField(max_length=80)        # ex: "Rebin.v2"
    internal = models.BooleanField(default=False)    # ex: "False"
    count = models.IntegerField()        # ex: "3"
    mantidVersion = models.CharField(max_length=32)  # ex: "3.2.20141208.1820"

    class Meta:
        unique_together = ('mantidVersion', 'type', 'name', 'internal')
