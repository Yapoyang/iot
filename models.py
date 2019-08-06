from django.db import models
import datetime
from collections import OrderedDict
# Create your models here.

class sensor_data(models.Model):
      id=models.AutoField(primary_key=True)
      temperature=models.CharField(max_length=200)
      humidity=models.CharField(max_length=200)
      pir=models.CharField(max_length=200)
      savetime=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='sensor_data'
class light_control(models.Model):
      id=models.AutoField(primary_key=True)
      value=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='light_control'

class er(models.Model):
      id=models.AutoField(primary_key=True)
      type=models.CharField(max_length=200)
      macid=models.CharField(max_length=200)
      loc=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='er_test'
      def toDict(count,tag):
          dict_tag=OrderedDict()
          ls_member=[]
          i=0
          while i<count:
                  dict_member=OrderedDict()
                  dict_member['id']=tag[i].id
                  dict_member['name']=tag[i].type
                  dict_member['macid']=tag[i].macid
                  dict_member['loc']=tag[i].loc
                  ls_member.append(dict_member)
                  i+=1
          dict_tag['member']=ls_member
          return dict_tag

class oc(models.Model):
      id=models.AutoField(primary_key=True)
      bed=models.CharField(max_length=200)
      room=models.CharField(max_length=200)
      time=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='occupiedroom'
      def toDict(count,tag):
          dict_tag=OrderedDict()
          ls_member=[]
          i=0
          while i<count:
                  dict_member=OrderedDict()
                  dict_member['id']=tag[i].id
                  dict_member['iv']=tag[i].bed
                  dict_member['room']=tag[i].room
                  dict_member['status']=tag[i].time
                  ls_member.append(dict_member)
                  i+=1
          dict_tag['member']=ls_member
          return dict_tag
     

class summary(models.Model):
      temp=models.FloatField()
      humi=models.FloatField()
      class Meta:
          managed=False
          db_table='summary'
class light_positioning(models.Model):
      id=models.AutoField(primary_key=True)
      DriverID=models.CharField(max_length=200)
      DriverMAC=models.CharField(max_length=200)
      DriverIPV6=models.CharField(max_length=200)
      DateTime=models.CharField(max_length=200)
      DriverType=models.CharField(max_length=200)
      Brightness=models.CharField(max_length=200)
      ColorTemperature=models.CharField(max_length=200)
      ColorX=models.CharField(max_length=200)
      ColorY=models.CharField(max_length=200)
      Power=models.CharField(max_length=200)
      Status=models.CharField(max_length=200)
      DeviceMemberNumber=models.CharField(max_length=200)
      DriverMember=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='light_position_203'

class sensor_max(models.Model):
      id=models.AutoField(primary_key=True)
      DriverMAC=models.CharField(max_length=200)
      DateTime=models.CharField(max_length=200)
      devicemac=models.CharField(max_length=200)
      g_x=models.CharField(max_length=200)
      g_y=models.CharField(max_length=200)
      devicetype=models.CharField(max_length=200)
      g_z=models.CharField(max_length=200)
      devicegetlightid1=models.CharField(max_length=200)
      devicegetbrightness1=models.CharField(max_length=200)
      devicegetlightid2=models.CharField(max_length=200)
      devicegetbrightness2=models.CharField(max_length=200)
      deviceseq=models.CharField(max_length=200)
      positionid=models.CharField(max_length=200)
      battery=models.CharField(max_length=200)
      rssi=models.CharField(max_length=200)
      bri_adjust=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='sensor_max'
      def toDict(count,tag):
          dict_tag=OrderedDict()
          ls_member=[]
          i=0
          while i<count:
                  dict_member=OrderedDict()
                  dict_member['DriverMAC']=tag[i].DriverMAC
                  dict_member['tagid']=tag[i].devicemac
                  dict_member['lightid1']=tag[i].devicegetlightid1
                  dict_member['lightid2']=tag[i].devicegetlightid2
                  dict_member['adjust']=tag[i].bri_adjust
                  dict_member['time']=str(tag[i].DateTime)
                  ls_member.append(dict_member)
                  i+=1
          dict_tag['member']=ls_member
          return dict_tag
      def toDict_2(count,tag):
          dict_tag=OrderedDict()
          ls_member=[]
          i=0
          while i<count:
                  dict_member=OrderedDict()
                  dict_member['DriverMAC']=tag[i]['DriverMac']
                  dict_member['tagid']=tag[i]['devicemac']
                  dict_member['lightid1']=tag[i]['positionid']
                  dict_member['lightid2']=tag[i]['devicegetlightid2']
                  dict_member['adjust']=tag[i]['bri_adjust']
                  dict_member['time']=str(tag[i]['dt'])
                  ls_member.append(dict_member)
                  i+=1
          dict_tag['member']=ls_member
          return dict_tag

class medical_record(models.Model):
      id=models.AutoField(primary_key=True)
      name=models.CharField(max_length=200)
      age=models.CharField(max_length=200)
      gender=models.CharField(max_length=200)
      clinic=models.CharField(max_length=200)
      blood_pressure=models.CharField(max_length=200)
      body_temperature=models.CharField(max_length=200)
      class Meta:
          managed=False
          db_table='medical_record'
      def toDict(count,tag):
          dict_tag=OrderedDict()
          ls_member=[]
          i=0
          while i<count:
                  dict_member=OrderedDict()
                  dict_member['name']=tag[i].name
                  dict_member['age']=tag[i].age
                  dict_member['gender']=tag[i].gender
                  dict_member['clinic']=tag[i].clinic
                  dict_member['blood_pressure']=tag[i].blood_pressure
                  dict_member['body_temperature']=tag[i].body_temperature
                  ls_member.append(dict_member)
                  i+=1
          dict_tag['member']=ls_member
          return dict_tag

