function shaping_json($this) {
    if ($this.value != '') {
        try {
            var json = $.parseJSON($this.value);
            $('#json_check').removeClass('has-error');
            $('#send_json').attr('name', 'json');
        } catch (e) {
            $('#json_check').addClass('has-error');
            $('#send_json').removeAttr('name');
            //alert('正しいJSON形式で入力してください');
        }
    } else {
        $('#json_check').removeClass('has-error');
        $('#send_json').removeAttr('name');
    }
}

function verification() {
    var input_json = $.trim($('#input_json').val());
    if (!input_json.length) {
        return true;
    } else {
        try {
            var json = $.parseJSON(input_json);
            $('#json_check').removeClass('has-error');
            $('#send_json').attr('name', 'json');
            var new_json = input_json.replace(/ /g, '');
            new_json = new_json.replace(/\n/g, '');
            new_json = new_json.replace(/\t/g, '');
            $('#send_json').attr('value', new_json);
            return true;
        } catch (e) {
            $('#json_check').addClass('has-error');
            $('#send_json').removeAttr('name');
            alert('正しいJSON形式で入力してください\n' + e);
            return false;
        }
    }
}

$("#show_password").change(function() {
    if ($('#input_password').attr('type') == 'password') {
        $('#input_password').attr('type', 'text');
    } else {
        $('#input_password').attr('type', 'password');
    }
});

$(function () {
    $("#datetimepicker").datetimepicker({
        language: "ja",
        format: "YYYY/MM/DD hh:mm a",
        minDate: moment(),
    });
});

$('tr[data-href]').addClass('clickable')
    .click(function(e) {
    if($(e.target).is('td,th')) {
        window.location = $(e.target).closest('tr').data('href');
    };
});

$('#destory_develop').click(function() {
    if (confirm('本当に削除しますか？')) {
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            type: "POST",
            data: {'pem_type': 'develop'},
            success: function (result) {
                location.href = url + "?result=develop_success";
            }
        });
    }
});

$('#destory_product').click(function() {
    if (confirm('本当に削除しますか？')) {
        var url = $(this).attr('data-url');
        $.ajax({
            url: url,
            type: "POST",
            data: {'pem_type': 'product'},
            success: function (result) {
                location.href = url + "?result=product_success";
            }
        });
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.notification_status_change').click(function () {
    var $button = $('#notification_status_change' + $(this).attr('data-id'));
    $.ajax({
        url: '/change_notification_status',
        type: 'PUT',
        data: {'notification_id': $button.attr('data-id'),
               'status': $button.attr('data-status')},
    }).done(function(data) {
        location.href = '/notification_list';
    });
});
