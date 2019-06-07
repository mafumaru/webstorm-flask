define(['jquery'], function ($) {
    function comment() {
        // alert('comment');
    }

    function show() {
        $(this).toggle();
        $(this).next().next().find(".shut").toggle();
        $(this).next().next().css({'position': 'fixed', 'bottom': 0}); //固定bar
        $(this).next().css({"display": "block"});
        float(this);
        // console.log($(window).scrollTop());
        $('html,body').animate({scrollTop: $(window).scrollTop()}, 1);
    }

    function float(obj) {
        $(window).bind('scroll', function () {
            if ($(window).scrollTop() + $(window).height() >= $(obj).next().height() + $(obj).next().offset().top) {
                $(obj).next().next().css({'position': 'relative'});
            }
        });
    }

    function hide() {
        $(this).toggle();
        $(this).parent().css({'position': 'relative'});//解除固定bar
        $(this).parent().prev().toggle();
        $(this).parent().prev().prev().toggle();
        $('html,body').animate({scrollTop: $(this).parent().prev().prev().offset().top-140}, 1);
    }

    // $('.shut').click(hide);
    // $('.main-content').click(show);

    $(document).on('click','.shut',hide);
    $(document).on('click','.main-content',show);


    $(document).on('click','.rl_comment',function () {
        $('#rl_input').val("https://www.zhihu.com/question/294919712/answer/"+$(this).data('id'));
        // $('#rl_input').val("https://twitter.com/"+$(this).data('table_name')+"/status/"+$(this).data('id'));
        $('#rl_modal_trigger').click();
    });
});

