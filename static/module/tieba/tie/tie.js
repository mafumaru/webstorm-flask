require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js'], function (list) {
    list.active_list_with_history(
        "/module/tieba/helper/TiebaTieHelper/get_history",
        "/module/tieba/helper/TiebaTieHelper/set_history",
        "/module/tieba/view/TiebaTieView/ajax_list"
    );

});