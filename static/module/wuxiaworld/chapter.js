require(['/static/core/js/nav.js'], function() {
    $(".cross-p").each(function(){
        offset = $(this).prev().height();
        // $(this).css({'marginTop':20-offset})
        $(this).css({'marginTop':25-offset}) // cn 在上
    });

    $('.correct-btn').on('click', function () {
        $.get('/module/wuxiaworld/helper/NovelHelper/delete_p', {
            book_name: $(this).data('book_name'),
            id: $(this).data('chapter_id'),
            type: $(this).data('type'),
            p: $(this).data('pid')
        }, function (data) {
            if (data == 'true') {
                window.location.reload();
            }
        });
    });
    $('.page-down-btn').on('click', function () {
        $('html,body').animate({scrollTop: $(window).scrollTop() + $(window).height()*0.8}, 1);
    });


    $('#wordbase_upload').toggle();
    $('#wordbase_upload_by_novel').toggle();
});