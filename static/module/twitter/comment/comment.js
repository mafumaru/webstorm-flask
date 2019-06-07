require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js'], function (list) {
    list.active_list_with_history(
        "/module/twitter/helper/TwitterCommentHelper/get_history",
        "/module/twitter/helper/TwitterCommentHelper/set_history",
        "/module/twitter/view/TwitterCommentView/ajax_list"
    );
});