#coding:utf-8

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from models import Operation, TaskModel
from celery.result import AsyncResult
from tasks import test, invoke_shell_remote


def index(request):
    operations = Operation.objects.all().order_by("-id")
    return render(request, "main.html", {"operations": operations})


def get_detail(request, pk):
    refresh_task_queue()
    op = get_object_or_404(Operation, pk=pk)
    tasks = op.taskmodel_set.all()
    return render(request, "detail.html", {"tasks": tasks})


def do_update(request):
    if request.method == "POST":
        ips = request.POST["ips"]
        op = Operation(o_ips=ips)
        op.save()
        op_id = op
        ip_list = ips.split(";")
        for ip in ip_list:
            if ip:
                per_ip(ip, op_id)
        resp = "success"
    else:
        resp = "GET not allowed"
    return HttpResponse(resp)


def per_ip(ip, op_id):
    result = invoke_shell_remote.delay(
        "/cygdrive/d/wintool/WinTool.exe -Patch:down && /cygdrive/d/wintool/WinTool.exe -Patch:ins", ip
    )
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    m_task = TaskModel(
        t_operation=op_id,
        t_content=ip,
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result
    )
    m_task.save()


def refresh_task_queue():
    import chardet
    pending = list(TaskModel.objects.filter(t_status="PENDING"))
    started = list(TaskModel.objects.filter(t_status="STARTED"))
    items = pending + started
    for item in items:
        result = AsyncResult(item.t_task_id)
        if not result.result:
            m_result = ""
        else:
            try:
                encoding = chardet.detect(result.result)['encoding']
                m_result = result.result.decode(encoding)
            except:
                m_result = result.result
        item.t_status = result.status
        item.t_result = m_result
        item.save()
    return
