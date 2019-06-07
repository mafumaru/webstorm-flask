define(['jquery', 'bootstrap'], function ($) {
    return {
        ajax_html: function (url, data, success) {
            $.ajax({
                url: url,
                type: 'get',
                dataType: 'html',
                data: data,
                success: success
            });
        }
    }
});