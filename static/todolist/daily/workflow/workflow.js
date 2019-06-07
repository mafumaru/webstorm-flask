require(['/static/core/js/nav.js'], function () {
    $('#clear_to_undo').on('click', function () {
        $.get('/module/todolist/helper/TodolistWorkFlowHelper/clear_to_undo', function (data) {
            window.location.href="/module/todolist/view/TodolistView/homepage"
            // window.open('/module/todolist/view/TodolistView/homepage')
        });
    });

    $('#workflow_done').on('click', function () {
        var todolist_delete_item = $('#workflow_ul input[name="workflow_item"]:checked');
        $.post('/module/todolist/helper/TodolistWorkFlowHelper/delete', {
            id: todolist_delete_item.val()
        }, function (data) {
            todolist_delete_item.parent().parent().remove();
        });
    });

    $('#exchange_workflow').on('click', function () {
        var workflow_delete_item = $('#workflow_ul input[name="workflow_item"]:checked');
        var prev_workflow_delete_item = workflow_delete_item.parent().parent().prev().find('input');
        $.post('/module/todolist/helper/TodolistWorkFlowHelper/exchange', {
            id: workflow_delete_item.val(),
            exchange_id: prev_workflow_delete_item.val()
        }, function (data) {
            window.location.reload();
        });
    });
});