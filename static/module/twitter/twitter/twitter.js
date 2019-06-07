require(['/static/core/js/list_with_history.js', '/static/core/js/nav.js'], function (list) {
    list.active_list_with_history(
        "/module/twitter/helper/TwitterTwitterHelper/get_history",
        "/module/twitter/helper/TwitterTwitterHelper/set_history",
        "/module/twitter/view/TwitterTwitterView/ajax_list"
    );
    history.scrollRestoration = 'auto';
    // $('.ProfileTweet-action--reply').addClass('btn btn-info');
    // $('.ProfileTweet-action--favorite').addClass('btn btn-danger');
    //
    // $('.js-action-profile-avatar').addClass('img-circle');
    // $('.AdaptiveMedia-photoContainer img').addClass('img-responsive center-block');
    $('.ProfileTweet-action--retweet').on('click',function () {
        $('#rl_input').val("https://twitter.com/"+$(this).data('table_name')+"/status/"+$(this).data('id'));
        $('#rl_modal_trigger').click();
    })

});