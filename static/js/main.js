/**
 * Created by shuangluo on 13-10-10.
 */

$(function(){

    var csrf = $(":input[name='csrfmiddlewaretoken']").val();

    $("#new-update").click(function(){
        $("#modal-new-update").modal();
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
        setTimeout(reload, 2000)
    });

    function reload() {
        location.reload();
    }

});