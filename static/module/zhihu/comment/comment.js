require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js'], function (list) {
    list.active_list_with_history(
        "/module/zhihu/helper/ZhihuCommentHelper/get_history",
        "/module/zhihu/helper/ZhihuCommentHelper/set_history",
        "/module/zhihu/view/ZhihuCommentView/ajax_list"
    );

});