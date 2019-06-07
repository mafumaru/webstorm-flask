require(['/static/core/js/nav.js'], function (list) {
    $.get('/module/wordbase/helper/WordbaseHelper/get_groups_view', function (data) {
        $('#pure_add_group_list').html(data);
    });

    $('#wb_pure_add_group_add').on('click', function () {
        var group_name = $('#wb_pure_add_group_input').val();
        $.get('/module/wordbase/helper/WordbaseHelper/add_group', {group_name: group_name}, function (data) {
            $('#pure_add_group_list').append(data);
            $('#wb_pure_add_group_input').val("");
        });
    });

    $('#wb_pure_add_group_delete').on('click', function () {
        var group_radio = $('#pure_add_group_list input[name="group"]:checked');
        var group_id = group_radio.val();
        $.get('/module/wordbase/helper/WordbaseHelper/delete_groups', {id: group_id}, function (data) {
            if (data == 'true') {
                group_radio.parent().parent().remove();
            }
        });
    });

    $('.wb_index_search_v').click(function (e) {
        // e.preventDefault();
        var keyword = $('#wordbase_pure_add_search_input').val();
        $('#wordbase_pure_add_search_input').val('');
        window.open('/module/wordbase/view/WordbaseView/wordbase_search?word='+keyword+'&search_type='+$(this).text());
    });

    $('#wb_pure_add').on('click', function () {
        var cn = $('#pure_add_cn').val();
        var en = $('#pure_add_en').val();
        var jp = $('#pure_add_jp').val();

        var word_collection_radio = $('#pure_add_word_collection_list input[name="word_collection"]:checked');
        var word_collection_type = word_collection_radio.val();

        var word_type = $('#pure_add_word_type_list input[name="word_type"]:checked').val();
        var group = $('#pure_add_group_list input[name="group"]:checked').val();


        params = {
            cn:cn,
            en:en,
            jp:jp,
            wordbase_collection: word_collection_type,
            word_type: word_type,
            group: group
        };

        $.post('/module/wordbase/helper/WordbaseHelper/add_pure_word', params, function (data) {

        });
    });
});