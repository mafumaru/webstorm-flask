require(['/static/core/js/nav.js'], function () {
    $('#make_workflow').on('click', function () {
        var todolist_workflow_item = $('#todolist_show input[name="todolist_item"]:checked');
        $.post('/module/todolist/helper/TodolistWorkFlowHelper/add', {
            content: todolist_workflow_item.parent().text().trim(),
            id: todolist_workflow_item.val()
        }, function (data) {
            todolist_workflow_item.parent().parent().remove();
        });
    });

    $('#todolist_done').on('click', function () {
        var todolist_delete_item = $('#todolist_show input[name="todolist_item"]:checked');
        $.post('/module/todolist/helper/DailyTodolistHelper/delete', {
            id: todolist_delete_item.val()
        }, function (data) {
            todolist_delete_item.parent().parent().remove();
        });
    });

    $.get('/module/todolist/view/TodolistView/get_frequent_domain_view', function (data) {
        $('#frequent_domain_btns').html(data);

        $('.frequent_domain_btn').on('click', function (e) {
            // e.preventDefault();
            // console.log('hi');
            $.get('/module/todolist/view/TodolistView/get_frequent_domain_set_view?id=' + $(this).data('domain_id'), function (data) {
                $('#frequent_todolist').html(data);
            });
        });

    });

    $.get('/module/todolist/view/TodolistView/get_frequent_todolist_view', function (data) {
        $('#frequent_todolist').html(data);
    });

    $.get('/module/todolist/view/TodolistView/get_undolist_view', function (data) {
        $('#undolist_view').html(data);
    });



    $('#frequent_todolist_add').on('click', function () {
        var frequent_todolist_input = $('#frequent_todolist_input').val();
        $.get('/module/todolist/helper/FrequentTodolistHelper/add', {content: frequent_todolist_input}, function (data) {
            $('#frequent_todolist').append(data);
            $('#frequent_todolist_input').val("");
        });
    });

    $('#frequent_todolist_delete').on('click', function () {
        var frequent_todolist_radio = $('#frequent_todolist input[name="frequent_todolist_radio"]:checked');
        var frequent_todolist_id = frequent_todolist_radio.val();

        $.get('/module/todolist/helper/FrequentTodolistHelper/delete', {id: frequent_todolist_id}, function (data) {
            frequent_todolist_radio.parent().parent().remove();
        });
    });

    var url = location.search;
    var str = url.substr(1);
    var parent_id = str.split("=")[1];

    $('#add_todolist').on('click', function () {
        var todolist_input = $('#todolist_input').val();

        var frequent_todolist = $('#frequent_todolist input[name="frequent_todolist_radio"]:checked');
        // console.log(frequent_todolist);
        if (frequent_todolist.length != 0) {
            todolist_input = frequent_todolist.parent().text().trim()
        }

        $.post('/module/todolist/helper/DailyTodolistHelper/add', {
            content: todolist_input,
            parent_id: parent_id
        }, function (data) {
            $('#todolist_input').val("");
        });
    });

    $('#frequent_domain_add').on('click', function () {
        var frequent_domain_todolist_input = $('#frequent_domain_input').val();
        $.get('/module/todolist/helper/FrequentDomainTodolistHelper/add', {domain: frequent_domain_todolist_input}, function (data) {
            $('#frequent_domain_input').val("");
        });
    });

    $('#handle_undolist').on('click', function () {
        // var todolist_input = $('#todolist_input').val();

        var undolist_radio = $('#undolist_view input[name="undolist_radio"]:checked');

        $.post('/module/todolist/helper/DailyTodolistHelper/add', {
            content: undolist_radio.parent().text().trim(),
            parent_id: parent_id
        }, function (data) {
            $.get('/module/todolist/helper/UndoTodolistHelper/delete', {id: undolist_radio.val()}, function (data) {
                undolist_radio.parent().parent().remove();
                window.location.reload();
            });
        });
    });


});