from django.db import models

# Create your models here.
class Message(models.Model):
  author = models.CharField(max_length=20)
  text = models.CharField(max_length=140)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
      return self.author

class Usage(models.Model):
    uid = models.CharField(max_length=32)           # md5 ex: "c5a9b601408709f47417bcba3571262b"
    host = models.CharField(max_length=32)          # md5 ex: "7defb184ceadab4e79eff323359ad373"
    dateTime = models.DateTimeField()               # ex: "2014-12-08T18:50:35.817942000"
    osName = models.CharField(max_length=32)        # ex: "Linux"
    osArch = models.CharField(max_length=16)        # ex: "x86_64"
    osVersion = models.CharField(max_length=32)     # ex: "3.17.4-200.fc20.x86_64"
    ParaView = models.CharField(max_length=16)      # ex: "3.98.1"
    mantidVersion = models.CharField(max_length=32) # ex: "3.2.20141208.1820"
    mantidSha1 = models.CharField(max_length=40)    # sha1 ex: "e9423bdb34b07213a69caa90913e40307c17c6cc"
    osReadable = models.CharField(max_length=80, default="", blank=True)    # ex: "Fedora 20 (Heisenbug)"
