define(['jquery'], function ($) {

    function select_text() {
        var selection = window.getSelection();

        return selection;
    }

    var timeOutEvent = undefined;
    var timeOutEvent2 = undefined;
    function judge_select(e) {
        var e = $.event.fix(e);
        // console.log(e.originalEvent.targetTouches);
        if (e.originalEvent.targetTouches){
            // console.log(e);
            e = e.originalEvent.targetTouches[0]
        }
        // console.log(e);
        // console.log(e.originalEvent.targetTouches);
        var iX = e.pageX,
            iY = e.pageY;
        // console.log(select_text().length);
        if (select_text().toString().length > 0 && select_text().toString() !=' ') {
            // $("#word_base_bar button").css({
            //     "left": iX - 50 + "px",
            //     "top": iY + 30 + "px"
            // }).show();
            // $.get('/module/wordbase/translation/BaiduSelectTranslation/translate',{word:select_text().toString()},function (data) {
            $.get('/module/wordbase/translation/Translation/translate',{word:select_text().toString()},function (data) {
                $("#word_base_bar button").text(data);
                $("#word_base_bar").css({
                "left": iX - 50 + "px",
                "top": iY + 30 + "px"
            }).show();
            });



            // $("#word_base_bar").show();
                // }).toggle();
                // }).css({"display": "block"});
        } else {
            // $("#word_base_bar").css({"display": "none"});
            // $("#word_base_bar").toggle();
            $("#word_base_bar").hide();

        }
    }

    // $("#word_base_bar").hide();
    $(document).bind("mouseup", function (e) {
        judge_select(e);
    });

    $(document).on({
        touchstart: function (e) {
            timeOutEvent = setTimeout(function () {
               judge_select(e);
            }, 800);
        },
        touchmove: function () {
            clearTimeout(timeOutEvent);
            // timeOutEvent = 0;
            // e.preventDefault();
        },
        touchend: function (e) {
            clearTimeout(timeOutEvent);
            // if (timeOutEvent != 0) {//点击
            // }
            // return false;
        },
        selectionchange:function (e) {
            clearTimeout(timeOutEvent2);
            timeOutEvent2 = setTimeout(function () {
               judge_select(e);
            }, 800);
        }
    });

    $(document).click(function () {
        if (select_text().toString().length==0 || select_text().toString() ==' '){
        // $("#word_base_bar").css({"display": "none"});
        //     $("#word_base_bar").toggle();
            $("#word_base_bar").hide();
        }
            // $("#word_base_bar").hide();
    });

    return {
        select_text: select_text
    }
});