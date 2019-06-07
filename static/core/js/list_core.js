define(['jquery'], function ($) {
    function get_single_url() {
        var url = location.search;
        var str = url.substr(1);
        var strs = str.split("=");
        return strs[1];
    }
    var url_name = get_single_url();

    return {
        page: 0,
        is_load: false,
        url_name: url_name,
        start_read:null,
        is_last_read:false
    };
});