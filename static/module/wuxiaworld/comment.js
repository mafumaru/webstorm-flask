require(['/static/core/js/nav.js'], function() {
    $('#wordbase_upload').toggle();
    $('#wordbase_upload_by_novel_comment').toggle();
    $('.reply-sign').on('click', function () {
        if($(this).hasClass('glyphicon-menu-down')){
            $(this).removeClass('glyphicon-menu-down');
            $(this).addClass('glyphicon-menu-up');
        }else {
            $(this).removeClass('glyphicon-menu-up');
            $(this).addClass('glyphicon-menu-down');
        }
        $(this).next().toggle();
    });

    $('.reply-end-sign').on('click', function () {
        $(this).parent().prev().click();
    });
});