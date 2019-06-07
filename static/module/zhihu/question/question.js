require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js','/static/module/zhihu/share/bar.js'], function (list) {
    list.active_list_with_history(
        "/module/zhihu/helper/ZhihuQuestionHelper/get_history",
        "/module/zhihu/helper/ZhihuQuestionHelper/set_history",
        "/module/zhihu/view/ZhihuQuestionView/ajax_list"
    );

});