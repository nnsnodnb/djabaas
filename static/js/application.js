function shaping_json($this) {
    if ($this.value != '') {
        try {
            var json = $.parseJSON($this.value);
            $('#json_check').removeClass('has-error');
            $(this).attr('name', 'json');
        } catch (e) {
            $('#json_check').addClass('has-error');
            $(this).removeAttr('name');
            //alert('正しいJSON形式で入力してください');
        }
    } else {
        $('#json_check').removeClass('has-error');
        $(this).removeAttr('name');
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
            $('#input_json').attr('name', 'json');
            return true;
        } catch (e) {
            $('#json_check').addClass('has-error');
            $('#input_json').removeAttr('name');
            alert('正しいJSON形式で入力してください\n' + e);
            return false;
        }
    }
}
