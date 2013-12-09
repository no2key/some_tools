/**
 * Created by shuangluo on 13-10-10.
 */

$(function(){

    var csrf = $(":input[name='csrfmiddlewaretoken']").val();

    $("#new-update").click(function(){
        $("#modal-new-update").modal();
    });
    $("#change-password").click(function(){
        $("#modal-change-password").modal();
    });

    $("#do_update").click(function(){
        var ip_list = $("#ip-list").val();
        var ips = ip_list.replace(/\r?\n/g, ";");
        $.ajax(
            {
                'type': 'post',
                'url': '/do_update/',
                'data': {
                    ips: ips,
                    csrfmiddlewaretoken: csrf
                },
                'dataType': 'json',
                success: function (resp) {
                    console.log(resp);
                }
            }
        );
        $("#modal-new-update").modal('hide');
        $("#modal-circle").modal();
        setTimeout(reload, 2000)
    });

    $("#do_change_pass").click(function(){
        var ip_list = $("#ip-list-password").val();
        var ips = ip_list.replace(/\r?\n/g, ";");
        var old_password = $("#old_password").val();
        var password = $("#password").val();
        $.ajax(
            {
                'type': 'post',
                'url': '/do_change_pass/',
                'data': {
                    ips: ips,
                    old_password: old_password,
                    password: password,
                    csrfmiddlewaretoken: csrf
                },
                'dataType': 'json',
                success: function (resp) {
                    console.log(resp);
                }
            }
        );
        $("#modal-change-password").modal('hide');
        $("#modal-circle").modal();
        setTimeout(reload, 5000)
    });

    function reload() {
        $("#modal-circle").modal('hide');
        location.reload();
    }

});