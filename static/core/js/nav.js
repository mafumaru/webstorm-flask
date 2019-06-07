define(['./base.js', './wordbase.js', 'treeview'], function (base, wordbase) {
    // $.get('http://www.baidu.com',function (data) {
    //     console.log(data)
    // });

    $('#rl_dir_add').on('click', function () {
        var category = $('#rl_dir_input').val();
        $.get('/module/rl/helper/ReadLaterDirHelper/add_rl_list', {list_name: category}, function (data) {
            $('#dir_list').append(data);
            var list_id = $(data).find('input').attr('value');
            $('#rl_menu').append('<li><a href="/module/rl/view/ReadLaterListView/render?list_id=' + list_id + '">' + category + '</a></li>');
            $('#rl_dir_input').val("");
        });
    });

    $('#rl_dir_delete').on('click', function () {
        var category_radio = $('#dir_list input[name="list_id"]:checked');
        var category_id = category_radio.val();
        $.get('/module/rl/helper/ReadLaterDirHelper/delete_rl_list', {list_id: category_id}, function (data) {
            if (data == 'true') {
                category_radio.parent().parent().remove();
            }
        });
    });

    $('#rl_save').on('click', function () {
        var input_url = $('#rl_input').val();
        var category_radio = $('#dir_list input[name="list_id"]:checked');
        var category_id = category_radio.val();
        $.post('/module/rl/filter/Filter/route', {follow_url: input_url, list_id: category_id}, function (data) {
            if (data == 'true') {
                console.log('get_response');
            }
        });
        $('#rl_input').val("");
    });

//Collection JS

    $.get('/module/collection/helper/CollectionHelper/get_collection_tree', function (data) {
        var treedata = $.parseJSON(data);
        // var treedata = data;
        // console.log(treedata);

        $('#tree').treeview({
            data: treedata,
            levels: 3,
            highlightSelected: false,
            nodeIcon: "glyphicon glyphicon-unchecked",
            selectedIcon: 'glyphicon glyphicon-check',
            collapseIcon: "glyphicon glyphicon-menu-up",//可收缩的节点图标
            expandIcon: "glyphicon glyphicon-menu-down"
        });

        $('#collection_tree').treeview({
            data: treedata,
            levels: 3,
            highlightSelected: false,
            collapseIcon: "glyphicon glyphicon-resize-small",//可收缩的节点图标
            expandIcon: "glyphicon glyphicon-resize-full",
            enableLinks: true
        });

        // $('#tree').treeview('collapseAll');
    });

    $('#add_collection_dir').click(function () {
        var nodeData = $('#tree').treeview('getSelected')[0];
        var id;
        if (nodeData) {
            id = nodeData.self_id;
        } else {
            id = 0;
        }
        var new_name = $('#collection_dir_input').val();
        $.get('/module/collection/helper/CollectionHelper/add_dir', {name: new_name, parent_id: id}, function (data) {
            var addNode = {
                text: new_name,
                self_id: parseInt(data),
                parent_id: id,
                herf: '/module/collection/view/CollectionView/render?list_id=' + parseInt(data),
                icon: "glyphicon glyphicon-unchecked",
                selectedIcon: "glyphicon glyphicon-check"
            };
            if (nodeData) {
                $("#tree").treeview("addNode", [nodeData.nodeId, {node: {text: addNode}}]);
                addNode.icon = "";
                addNode.selectedIcon = "";
                $("#collection_tree").treeview("addNode", [nodeData.nodeId, {node: {text: addNode}}]);
            } else {
                $("#tree").treeview("addNode", [0, {node: {text: addNode}}]);
                addNode.icon = "";
                addNode.selectedIcon = "";
                $("#collection_tree").treeview("addNode", [0, {node: {text: addNode}}]);
            }
            $('#collection_dir_input').val("");
        });
    });

    $('#collection_dir_delete').on('click', function () {
        var nodeData = $('#tree').treeview('getSelected')[0];
        $.get('/module/collection/helper/CollectionHelper/delete_dir', {id: nodeData.self_id}, function (data) {
            if (data == 'true') {
                $("#tree").treeview("deleteNode", nodeData.nodeId);
            }
        });
    });

    $('#collection_choose').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // 触发事件的按钮 
        $("#collection_save").unbind('click').click(function () {
            var nodeData = $('#tree').treeview('getSelected')[0];
            data = {
                parent_id: nodeData.self_id,
                type: button.data('type'),
                table_name: button.data('table_name'),
                id: button.data('id')
            };
            $.get('/module/collection/helper/CollectionHelper/add_collection', data,function (data) {
                // $('#collection_dir_input').val("");
            });

        });
    });
//Word Base

    $('.wb_search_v').click(function (e) {
        // e.preventDefault();
        $.get('/module/wordbase/helper/WordbaseHelper/search_view',
            {
                word: $('#wb_search_keyword').val(),
                search_type: $(this).text()
            }, function (data) {
                $('#wb_search_').html(data);
            });
    });

    $.get('/module/wordbase/helper/WordbaseHelper/get_groups_view', function (data) {
        $('#group_list').html(data);
    });

    $('#wb_group_add').on('click', function () {
        var group_name = $('#wb_group_input').val();
        $.get('/module/wordbase/helper/WordbaseHelper/add_group', {group_name: group_name}, function (data) {
            $('#group_list').append(data);
            $('#wb_group_input').val("");
        });
    });

    $('#wb_group_delete').on('click', function () {
        var group_radio = $('#group_list input[name="group"]:checked');
        var group_id = group_radio.val();
        $.get('/module/wordbase/helper/WordbaseHelper/delete_groups', {id: group_id}, function (data) {
            if (data == 'true') {
                group_radio.parent().parent().remove();
            }
        });
    });

    $('#wordbase_choose').on('show.bs.modal', function (event) {
        var selection = wordbase.select_text();
        // console.log(selection);
        // console.log(selection.getRangeAt(0));
        // console.log($(selection.getRangeAt(0).commonAncestorContainer));
        // console.log($(selection.getRangeAt(0).commonAncestorContainer).hasClass('list_item'));
        var recipient = selection.toString();
        // console.log(recipient);
        var context = $(selection.getRangeAt(0).commonAncestorContainer);


        // console.log(collection.data('type'));
        // console.log(collection.data('table_name'));
        // console.log(collection.data('id'));

        var modal = $(this);
        // $.get('/module/wordbase/translation/BaiduSelectTranslation/translate',{word:recipient},function (data) {
        modal.find('.modal-body .selected_word').text(recipient);
        $('#wb_search_keyword').val(recipient);
        // $.get('/module/wordbase/translation/Translation/translate',{word:recipient},function (data) {
        //     modal.find('.modal-body .translate').text(data);
        // });
        modal.find('.modal-body .translate').text($("#word_base_bar button").text());
        $('#wordbase_upload').unbind('click').on('click', function () {
            while (!context.hasClass('list_item')) {
                context = context.parent();
            }
            var collection = context.find("[data-target='#collection_choose']");
            // var collection = $("[data-target='#collection_choose']");

            var word_collection_radio = $('#word_collection_list input[name="word_collection"]:checked');
            var word_collection_type = word_collection_radio.val();

            var word_type = $('#word_type_list input[name="word_type"]:checked').val();
            var group = $('#group_list input[name="group"]:checked').val();

            var word_id_radio = $('#wb_search_ input[name="word_id"]:checked');
            var word_id = word_id_radio.val();
            var wordset_id = $('#wb_search_ input[name="wordset_id"]:checked').val();

            params = {
              add_type:'',
              word:recipient,
              wordbase_collection:word_collection_type,
              source_type:collection.data('type'),
              source_table_name:collection.data('table_name'),
              source_id:collection.data('id'),
              word_type:word_type,
              group:group,
              word_id:word_id,  //
              wordset_id:wordset_id //
            };
            if(!word_id && !wordset_id){
                params.add_type='first'
            }else if(word_id_radio && word_id_radio.data('type')==='word') {
                params.add_type='wordlang';
                params.word_type='word';
                params.wordset_id=word_id_radio.data('wordset_id');
            }else if (wordset_id){
                params.word_type='word';
                params.add_type='word'
            }else {
                params.add_type='wordlang'
            }

            // console.log(word_collection_type);
            $.post('/module/wordbase/helper/WordbaseHelper/add', params, function (data) {

            });
        });

        $('#wordbase_upload_by_novel').unbind('click').on('click', function () {
            var button = context.parent().find("button");

            var word_collection_radio = $('#word_collection_list input[name="word_collection"]:checked');
            var word_collection_type = word_collection_radio.val();

            var word_type = $('#word_type_list input[name="word_type"]:checked').val();
            var group = $('#group_list input[name="group"]:checked').val();

            var word_id_radio = $('#wb_search_ input[name="word_id"]:checked');
            var word_id = word_id_radio.val();
            var wordset_id = $('#wb_search_ input[name="wordset_id"]:checked').val();

            params = {
                add_type: '',
                word: recipient,
                wordbase_collection: word_collection_type,
                word_type: word_type,
                group: group,
                word_id: word_id,  //
                wordset_id: wordset_id,
                book_name: button.data('book_name'),
                chapter_id: button.data('chapter_id'),
                p: button.data('pid')
            };
            if(!word_id && !wordset_id){
                params.add_type='first'
            }else if(word_id_radio && word_id_radio.data('type')==='word') {
                params.add_type='wordlang';
                params.word_type='word';
                params.wordset_id=word_id_radio.data('wordset_id');
            }else if (wordset_id){
                params.word_type='word';
                params.add_type='word';
                params.word_id = '';
            }else {
                params.add_type='wordlang'
            }

            // console.log(word_collection_type);
            $.post('/wuxiaworld/chapter', params, function (data) {

            });

            // $.post('/wuxiaworld/chapter', {
            //     word: recipient,
            //     collection: word_collection_type,
            //     book_name: button.data('book_name'),
            //     chapter_id: button.data('chapter_id'),
            //     p: button.data('pid')
            // }, function (data) {
            //
            // });
        });

        $('#wordbase_upload_by_novel_comment').unbind('click').on('click', function () {
            var reply_id = '';
            console.log(context.parent());
            if(context.parent().hasClass('reply_comment')){
                reply_id=context.parent().data('id')
            }
            while (!context.hasClass('wordbase_container')) {
                context = context.parent();
            }

            var word_collection_radio = $('#word_collection_list input[name="word_collection"]:checked');
            var word_collection_type = word_collection_radio.val();

            var word_type = $('#word_type_list input[name="word_type"]:checked').val();
            var group = $('#group_list input[name="group"]:checked').val();

            var word_id_radio = $('#wb_search_ input[name="word_id"]:checked');
            var word_id = word_id_radio.val();
            var wordset_id = $('#wb_search_ input[name="wordset_id"]:checked').val();

            params = {
                add_type: '',
                word: recipient,
                wordbase_collection: word_collection_type,
                word_type: word_type,
                group: group,
                word_id: word_id,  //
                wordset_id: wordset_id,
                novel: context.data('novel'),
                chapter_id: context.data('chapter_id'),
                page: context.data('page'),
                comment_id: context.data('id'),
                reply_id: reply_id
            };
            if(!word_id && !wordset_id){
                params.add_type='first'
            }else if(word_id_radio && word_id_radio.data('type')==='word') {
                params.add_type='wordlang';
                params.word_type='word';
                params.wordset_id=word_id_radio.data('wordset_id');
            }else if (wordset_id){
                params.word_type='word';
                params.add_type='word'
            }else {
                params.add_type='wordlang'
            }

            // console.log(word_collection_type);
            $.post('/wuxiaworld/comment', params, function (data) {

            });

            // $.post('/wuxiaworld/comment', {
            //     word: recipient,
            //     collection: word_collection_type,
            //     novel: context.data('novel'),
            //     chapter_id: context.data('chapter_id'),
            //     page: context.data('page'),
            //     comment_id: context.data('id'),
            //     reply_id:reply_id
            // }, function (data) {
            //
            // });
        });

    });

});

