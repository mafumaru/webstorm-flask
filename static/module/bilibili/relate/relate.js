require(['/static/core/js/nav.js'], function () {
    var id = $('#root_flag').data('history');
    if (id != '0') {
        $('html,body').animate({scrollTop: $('#'+id).offset().top}, 0);
    }

    window.onbeforeunload = function (e) {
        var flag = $('#root_flag');
        //DEBUG
        $.get('/module/bilibili/helper/BilibiliRelateHelper/set_resume', {
            id: flag.data('root_id'),
            resume_id: flag.data('id')
        });

        var history;
        $('.relates_list').children(".list-group-item").each(function () {
            if ($(this).offset().top+$(this).height() > $(window).scrollTop()) {
                history = $(this).data('id');
                return false;
            }
        });

        $.get('/module/bilibili/helper/BilibiliRelateHelper/set_history', {
            id: flag.data('id'),
            history: history
        })
    };


});