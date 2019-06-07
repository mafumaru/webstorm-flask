define(['./base.js', './list_core.js'], function (base, core) {
    function ajax_add_list(url) {
        if ($(window).scrollTop() + $(window).height() * 2 + 1 >= $(document).height()) {
            if (!core.is_load) {
                core.page += 1;
                if (core.start_read) {
                    url_attr = {table_name: core.url_name, history: core.start_read, offset: core.page};
                } else {
                    url_attr = {table_name: core.url_name, offset: core.page};
                }
                base.ajax_html(url, url_attr, function (data) {
                    $('.list').append(data);
                    core.is_load = false;
                });
                core.is_load = true;
            }
        }
    }

    return {
        active_list: function (ajax_list_url) {
            $(window).scroll(function () {
                ajax_add_list(ajax_list_url);
            });
        },
        ajax_add_list:ajax_add_list
    }

});