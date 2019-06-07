require(['/static/core/js/nav.js'], function() {
    // $.ajax({
    //         type: 'get',
    //         url: 'https://interface.bilibili.com/player?id=cid:10823027&aid=6649674',
    //         crossDomain: 'true',
    //         success: function (data) {
    //             console.log(data)
    //         }
    //     });
    $('#webstorm_nav').removeClass('navbar-fixed-top');
    $('#wordbase_upload').toggle();
    $('#wordbase_upload_byVideo').toggle();



    $(window).keypress(function (e) {
        var video = document.getElementById("myVideo");
        // console.log(e.which);
        if (e.which == 32) {
            e.preventDefault();
            if (video.paused)
                video.play();
            else
                video.pause();
        }
    });



    $('#chinese_upload').unbind('click').on('click', function () {
        var chinese_word = $('#chinese_word').val();
        var chinese_explanation = $('#chinese_explanation').val();
        var category_radio = $('#chinese_colletion_list input[name="chinese_colletion"]:checked');
        var collection = category_radio.val();
        $.post('/module/wordbase/helper/ChineseHelper/add_word', {word:chinese_word,collection:collection,explanation:chinese_explanation}, function (data) {
            if (data == 'true') {
                console.log('get_response');
            }
        });
        $('#chinese_word').val("");
        $('#chinese_explanation').val("");
    });

    $('.wb_search_v').unbind('click').click(function (e) {
        // e.preventDefault();
        $.get('/module/wordbase/helper/WordbaseHelper/search_view_proxy',
            {
                word: $('#wb_search_keyword').val(),
                search_type: $(this).text()
            }, function (data) {
                $('#wb_search_').html(data);
            });
    });

    $.get('/module/wordbase/helper/WordbaseHelper/get_groups_view_proxy', function (data) {
        $('#group_list').html(data);
    });

    $('#wb_group_add').unbind('click').on('click', function () {
        var group_name = $('#wb_group_input').val();
        $.get('/module/wordbase/helper/WordbaseHelper/add_group_proxy', {group_name: group_name}, function (data) {
            $('#group_list').append(data);
            $('#wb_group_input').val("");
        });
    });

    $('#wb_group_delete').unbind('click').on('click', function () {
        var group_radio = $('#group_list input[name="group"]:checked');
        var group_id = group_radio.val();
        $.get('/module/wordbase/helper/WordbaseHelper/delete_groups_proxy', {id: group_id}, function (data) {
            if (data == 'true') {
                group_radio.parent().parent().remove();
            }
        });
    });

});