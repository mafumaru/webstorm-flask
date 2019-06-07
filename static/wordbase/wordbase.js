// require(['/static/core/js/list.js','/static/core/js/nav.js'], function (list) {
require(['/static/core/js/nav.js'], function (list) {
    // list.active_list("/module/wordbase/view/WordbaseView/ajax_list");


    $.get('/module/wordbase/helper/WordbaseHelper/get_groups_view', function (data) {
        $('#tag_group_list').html(data);
    });

    $('#tag_group_group_add').on('click', function () {
        var group_name = $('#tag_group_input').val();
        $.get('/module/wordbase/helper/WordbaseHelper/add_group', {group_name: group_name}, function (data) {
            $('#tag_group_list').append(data);
            $('#tag_group_input').val("");
        });
    });

    $('#tag_group_delete').on('click', function () {
        var group_radio = $('#tag_group_list input[name="group"]:checked');
        var group_id = group_radio.val();
        $.get('/module/wordbase/helper/WordbaseHelper/delete_groups', {id: group_id}, function (data) {
            if (data == 'true') {
                group_radio.parent().parent().remove();
            }
        });
    });


    $('#wordbase_tag_group').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // 触发事件的按钮 
        $("#tag_group_").unbind('click').click(function () {
            var new_group = $('#tag_group_list input[name="group"]:checked').parent();
            data = {
                word_type: button.data('type'),
                word_id: button.data('word_id'),
                group_name: new_group.text().trim()
            };
            $.get('/module/wordbase/helper/WordbaseHelper/tag', data,function (data) {
                // $('#collection_dir_input').val("");
                new_tag = '<button class="btn btn-default"><span class="glyphicon glyphicon-tag"></span> '+new_group.text()+'</button>';
                button.prev().append(new_tag);
            });

        });
    });

    $('#pure_update_modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // 触发事件的按钮 
        $('#pure_update_label').text(button.text());
        $("#pure_update").unbind('click').click(function () {
            var value = $('#pure_update_input').val();
            data = {
                add_type: 'wordlang',
                word_type: button.data('type'),
                word_id: button.data('word_id'),
                word:value.trim()
            };
            $.get('/module/wordbase/helper/WordbaseHelper/inner_add', data, function (data) {
                // $('#collection_dir_input').val("");
                new_tag = '<h3>'+value+'</h3>';
                button.parent().append(new_tag);
                button.remove()
            });

        });
    });

    $(".cross-p").each(function(){
        offset = $(this).prev().height();
        $(this).css({'marginTop':25-offset})
    });

    $('.reply-sign').on('click', function () {
        if($(this).hasClass('glyphicon-menu-down')){
            $(this).removeClass('glyphicon-menu-down');
            $(this).addClass('glyphicon-menu-up');
        }else {
            $(this).removeClass('glyphicon-menu-up');
            $(this).addClass('glyphicon-menu-down');
        }
        $(this).next().toggle();
    });

    $('.reply-end-sign').on('click', function () {
        $(this).parent().prev().click();
    });

    $('.update_translate_btn').on('click', function () {

    });


});