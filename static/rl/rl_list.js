// require(['/static/core/js/list.js','/static/core/js/nav.js'], function(list) {
require(['/static/core/js/nav.js'], function(list) {
    // history.scrollRestoration = 'manual';
    // list.active_list("/module/rl/view/ReadLaterListView/ajax_list");

    $('.delete_rl_btn').on('click',function () {
        $.get('/module/rl/helper/ReadLaterHelper/delete',{row_name:$(this).data('row_name'),type:$(this).data('type')},function (data) {
            window.location.reload()
        })
    })
});