#coding:utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from models import Operation, TaskModel, Password, PasswordModel
from celery.result import AsyncResult
from tasks import invoke_shell_remote


@login_required
def index(request):
    operations = Operation.objects.all().order_by("-id")
    return render(request, "main.html", {"operations": operations})


@login_required
def get_detail(request, pk):
    refresh_task_queue()
    op = get_object_or_404(Operation, pk=pk)
    tasks = op.taskmodel_set.all()
    return render(request, "detail.html", {"tasks": tasks})


@login_required
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
    try:
        cur_pass = Password.objects.get(p_ip=ip).p_password
    except:
        cur_pass = "1qazXSW@"
    result = invoke_shell_remote.delay(
        shell_path="/cygdrive/d/wintool/WinTool.exe -Patch:down && /cygdrive/d/wintool/WinTool.exe -Patch:ins",
        ip=ip,
        password=cur_pass
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

    pending = list(PasswordModel.objects.filter(t_status="PENDING"))
    started = list(PasswordModel.objects.filter(t_status="STARTED"))
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


@login_required
def change_password(request):
    refresh_task_queue()
    items = []
    operations = Password.objects.all().order_by("-id")
    for op in operations:
        task = op.passwordmodel_set.all()[0]
        items.append((op, task))
    return render(request, "password.html", {"items": items})


@login_required
def do_change_pass(request):
    if request.method == "POST":
        ips = request.POST["ips"]
        new_password = request.POST["password"]
        ip_list = ips.split(";")
        for ip in ip_list:
            if ip:
                try:
                    op = Password.objects.get(p_ip=ip)
                    cur_pass = op.p_password
                    op.p_password = new_password
                except:
                    cur_pass = "1qazXSW@"
                    op = Password(p_ip=ip, p_password=new_password)
                op.save()
                op_id = op
                per_ip_pass(ip, cur_pass, new_password, op_id)
        resp = "success"
    else:
        resp = "GET not allowed"
    return HttpResponse(resp)


def per_ip_pass(ip, cur_pass, new_password, op_id):
    c = Context({
        "password": new_password,
    })
    t = get_template("chpasswd.txt")
    command = t.render(c)
    result = invoke_shell_remote.delay(shell_path=command, ip=ip, password=cur_pass)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    m_task = PasswordModel(
        t_operation=op_id,
        t_content=ip,
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result
    )
    m_task.save()

