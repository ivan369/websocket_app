
$(function () {

    /*==================================================================
    [ Validate ]*/
    var username = $('.validate-input input[name="username"]');
    var favorite_number = $('.validate-input input[name="favorite_number"]');


    function validate_input_value_is_integer(check_value){
        let validation_status = true;
        if (Number.isInteger(Number(check_value))){
            validation_status = true;
        }else{
            validation_status = false;
        }
        return validation_status
    }



    function basic_validation_for_input_fields(){
        var check = true;

        if($(username).val() == ''){
            showValidate(username);
            check=false;
        }

        if($(favorite_number).val() == ''){
            showValidate(favorite_number);
            check=false;
        }
        if (!validate_input_value_is_integer($(favorite_number).val() )){
            showValidate(favorite_number);
            $('#favorite_number_error_message').show();
            check=false;

        }
        return check;
    }


    $('.validate-form').on('submit',function(){
        let validation_status = basic_validation_for_input_fields();
        if (!validation_status){
            return false;
        }
    });


    $('.validate-form .input1').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    var uTable = $('#user_table').DataTable({
        "bLengthChange": false,
        "language": {
            "sEmptyTable":     "No data available in table",
            "sInfo":           "Showing _START_ to _END_ of _TOTAL_ entries",
            "sInfoEmpty":      "Showing 0 to 0 of 0 entries",
            "sInfoFiltered":   "(filtered from _MAX_ total entries)",
            "sInfoPostFix":    "",
            "sInfoThousands":  ",",
            "sLengthMenu":     "Show _MENU_ entries",
            "sLoadingRecords": "Loading...",
            "sProcessing":     "Processing...",
            "sSearch":         "Search:",
            "sZeroRecords":    "No matching records found",
            "oPaginate": {
                "sFirst":    "First",
                "sLast":     "Last",
                "sNext":     "Next",
                "sPrevious": "Previous"
            },
            "oAria": {
                "sSortAscending":  ": activate to sort column ascending",
                "sSortDescending": ": activate to sort column descending"
            }
        },
        "searching": true,
        "bInfo": true,
        "bAutoWidth": false,
        "processing": true,
        'ajax':{
            'url': '/get_all_users',
            'type':'get',
            'data':function(){
            }
        },
        'iDisplayLength':10,

    });

    $('#submit_form_btn_web_server').on('click',function(){
        let username = $('#username').val();
        let favorite_number = $('#favorite_number').val();

        $.ajax({
            'type':'POST',
            'url':'/set_data_to_redis',
            'data':{
                'username': username,
                'favorite_number': favorite_number
            },
            'success':function(d){
                if(d != "success"){
                    alert(d)
                }
            }
        });
    });
    $( "#user_button_flask" ).click(function() {
        uTable.ajax.reload();
    });

    $( "#delete_data_table_content" ).click(function() {
        var table = $('#user_table').DataTable();
        table.clear().draw();
    });


    function fill_user_datatable(data){
        var table = $('#user_table').DataTable();
        table.clear().draw();

        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                let my_value = data[key];
                var myJSON = JSON.parse(my_value);
                if(myJSON){
                    let datatable_values = myJSON['data'];
                    if(datatable_values){

                        for (var i=0; i<datatable_values.length; i++){
                            let username = datatable_values[i][0];
                            let favorite_number = datatable_values[i][1];

                                $('#user_table').DataTable().row.add([
                                  username, favorite_number
                                ]).draw();
                        }
                    }
                }
            }
        }
    }

    var socket;
    socket = io.connect('http://' + document.domain + ':' + location.port + '/socket_app');

    socket.on('connect', function(data) {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('status', function(data) {
        fill_user_datatable(data);

    });

    socket.on('message', data => {
        fill_user_datatable(data);
    });

    socket.on('get_user_list', data => {
        fill_user_datatable(data);
    });

    socket.on('my response', data => {
        fill_user_datatable(data);
    });

    $( "#submit_form_btn_socekt_io_server" ).click(function() {
        let username = $("#username").val();
        let favorite_number = $("#favorite_number").val();
        let validation_status = basic_validation_for_input_fields();
        if (!validation_status){
            return false;
        }
        if(username && favorite_number){
            socket.send({'message': 'create_user', 'username': username, 'favorite_number': favorite_number});
        }else{
            alert("Ops something go wrong, your input data doesn't  passed validation!!")
        }
    });

    $( "#user_button_flask_socekt_io" ).click(function() {
        var table = $('#user_table').DataTable();
        table.clear().draw();
        socket.send({'message': 'get_user_list'});
    });

});





