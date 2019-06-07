require(['/static/core/js/list.js','/static/core/js/nav.js'], function(list) {
    list.active_list("/module/collection/view/CollectionView/ajax_list");
    // $('.ProfileTweet-action--reply').addClass('btn btn-info');
    // $('.ProfileTweet-action--retweet').addClass('btn btn-warning');
    // $('.ProfileTweet-action--favorite').addClass('btn btn-danger');

    // $('.js-action-profile-avatar').addClass('img-circle');
    $('.delete-collection').click(function () {
        var del = ($(this).parent().parent());
        $.get('/module/collection/helper/CollectionHelper/delete_collection', {id: $(this).data('id')}, function (data) {
            if (data == 'true') {
                del.remove();
            }
        });
    });
});