#coding:utf-8

from django.db import models


class Operation(models.Model):
    o_ips = models.CharField(max_length=1000, verbose_name="IP List")
    o_time = models.DateTimeField(auto_now=True)


class Password(models.Model):
    p_ip = models.IPAddressField(unique=True)
    p_password = models.CharField(max_length=16)
    p_time = models.DateTimeField(auto_now=True)


class TaskModel(models.Model):
    t_operation = models.ForeignKey('Operation')
    t_content = models.CharField(max_length=500, verbose_name="执行操作")
    t_task_id = models.CharField(max_length=50, verbose_name="任务ID")
    t_status = models.CharField(max_length=50, verbose_name="任务状态")
    t_result = models.TextField(verbose_name="执行结果")
    t_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.t_service + ": " + self.t_content


class PasswordModel(models.Model):
    t_operation = models.ForeignKey('Password')
    t_content = models.CharField(max_length=500, verbose_name="执行操作")
    t_task_id = models.CharField(max_length=50, verbose_name="任务ID")
    t_status = models.CharField(max_length=50, verbose_name="任务状态")
    t_result = models.TextField(verbose_name="执行结果")
    t_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.t_service + ": " + self.t_content