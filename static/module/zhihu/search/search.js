require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js','/static/module/zhihu/share/bar.js'], function (list) {
    list.active_list_with_history(
        "/module/zhihu/helper/ZhihuSearchHelper/get_history",
        "/module/zhihu/helper/ZhihuSearchHelper/set_history",
        "/module/zhihu/view/ZhihuSearchHelper/ajax_list"
    );

});