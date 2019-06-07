require(['/static/core/js/nav.js', '/static/core/js/list_core.js'], function (nav, core) {
    history.scrollRestoration = 'manual';
    var url = location.search;
    var str = url.substr(1);
    var twin = str.split("&");
    var postbar = twin[0].split("=")[1];
    var identity = twin[1].split("=")[1];
    var m_identity=new Date().getTime();
    $('#go_to_mark').attr('href','/module/tieba/view/TiebaPostbarView/mark_view?m_identity='+m_identity.toString()+'&postbar='+postbar);

    $(document).on('click','.postbar_mark_btn',function () {
        var btn = $(this);
        $.get('/module/tieba/helper/TiebaPostbarHelper/mark',{'id':$(this).data('id'),postbar: postbar,identity:identity,m_identity:m_identity},function (data) {
            btn.remove();
        });
    });

    function base_get_history(url) {
        $.get(url, {postbar: postbar,identity:identity}, function (response) {
            core.start_read = response;
        });
    }

    function base_set_history(url) {
        $.get(url, {history: core.is_last_read, postbar: postbar,identity:identity});
    }

    function base_get_last_read(url) {
        if (core.is_last_read != get_last_read()) {
            core.is_last_read = get_last_read();
            base_set_history(url);
        }
    }

    function get_last_read() {
        var last_read;
        $('.list').children(".list_item").each(function () {
            if ($(this).offset().top + $(this).height() > $(window).scrollTop()) {
                last_read = $(this).attr('id');
                return false;
            }
        });

        return last_read;
    }

    core.is_last_read = get_last_read();

    active_list_with_history(
        "/module/tieba/helper/TiebaPostbarHelper/get_identity_history",
        "/module/tieba/helper/TiebaPostbarHelper/set_identity_history",
        "/module/tieba/view/TiebaPostbarView/postbar_single_day_ajax"
    );

    function ajax_html(url, data, success) {
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'html',
            data: data,
            success: success
        });
    }

    function ajax_add_list(url) {
        if ($(window).scrollTop() + $(window).height() * 2 + 1 >= $(document).height()) {
            if (!core.is_load) {
                core.page += 1;
                console.log(core.page);
                if (core.start_read) {
                    url_attr = {postbar: postbar,identity:identity, history: core.start_read, offset: core.page,limit:20};
                } else {
                    url_attr = {postbar: postbar,identity:identity, offset: core.page,limit:20};
                }
                ajax_html(url, url_attr, function (data) {
                    $('.list').append(data);
                    core.is_load = false;
                });
                core.is_load = true;
            }
        }
    }

    function active_list_with_history(get_history_url, set_history_url, ajax_list_url) {
        base_get_history(get_history_url);

        $(window).scroll(function () {
            // console.log('scroll');
            base_get_last_read(set_history_url);
            ajax_add_list(ajax_list_url);
        });
    }


});