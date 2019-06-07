define(['./list.js', './list_core.js'], function (list, core) {
    history.scrollRestoration = 'manual';
    function base_get_history(url) {
        $.get(url, {table_name: core.url_name}, function (response) {
            core.start_read = response;
        });
    }

    function base_set_history(url) {
        $.get(url, {history: core.is_last_read, table_name: core.url_name});
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
            if ($(this).offset().top+$(this).height() > $(window).scrollTop()) {
                last_read = $(this).attr('id');
                return false;
            }
        });

        return last_read;
    }

    core.is_last_read = get_last_read();

    return {
        active_list_with_history: function active_list_with_history(get_history_url, set_history_url, ajax_list_url) {
            base_get_history(get_history_url);

            $(window).scroll(function () {
                // console.log('scroll');
                base_get_last_read(set_history_url);
                list.ajax_add_list(ajax_list_url);
            });
        }
    }

});