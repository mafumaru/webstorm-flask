require.config({

    paths: {
        jquery: '/static/lib/jquery.min',
        bootstrap: '/static/lib/bootstrap/js/bootstrap',
        treeview:'/static/lib/bootstrap-treeview'
    },
    shim: {
        bootstrap: ['jquery'],
        treeview:['jquery']
    },
    waitSeconds: 0
});