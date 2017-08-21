$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

$('form').on('submit', function() {
    $(document).find('#loading').show();
});

$('body').append('<div id="loading" class="loading"></div>');


$('.status_select').on('change', function() {

    var post_id = $(this).attr('data-post_id');
    var status = $(this).val();
    var endpoint = '/post/status/' + post_id;

    $.ajax({
        type: 'POST',
        url: endpoint,
        cache: false,
        data: {
            'status': status
        },
        context: this

    }).done(function(data) {
        $('.header_status_text').text('更新しました');
        $('.header_status').addClass('_show _success');

    }).fail(function(data) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function(data) {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _success _error');
    	},1000);

    });

});

if ($('#tinymce_textarea').length != 0) {
    tinymce.init({
        selector: "textarea",
        plugins: [
            "advlist autolink lists link image charmap preview hr",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime nonbreaking save table contextmenu directionality",
            "paste textcolor colorpicker textpattern codesample"
        ],
        codesample_languages: [
            {text: 'HTML/XML', value: 'markup'},
            {text: 'JavaScript', value: 'javascript'},
            {text: 'CSS', value: 'css'},
            {text: 'PHP', value: 'php'},
            {text: 'Ruby', value: 'ruby'},
            {text: 'Python', value: 'python'},
            {text: 'Bash', value: 'bash'}
        ],
        default_link_target: "_blank",
        language: "ja",
        toolbar1: "undo redo | bold italic | bullist numlist",
        toolbar2: "link image forecolor backcolor codesample",
        link_title: false,
        link_list: '/api/pdf',
        image_list: '/api/image',
        file_picker_callback: function(callback, value, meta) {
            if (meta.filetype == 'file') {
                $('#pdf_uploader').trigger('click');
                $('#pdf_uploader').on('change', function() {
                    var file = this.files[0];
                    if ($("input[name='pdf_file']").val() == '') {
                        return false
                    }
                    $('#loading').show();
                    var fd = new FormData($('#pdf_form').get(0));
                    fd.append('file', file);
                    $.ajax({
                        type: 'POST',
                        url: '/pdf/add',
                        cache: false,
                        data: fd,
                        processData: false,
                        contentType: false
                    }).done(function(data) {
                        callback(data.pdf_url, {text: data.title})
                    }).fail(function(data) {
                        $('.header_status_text').text('通信エラー');
                        $('.header_status').addClass('_show _error');

                    }).always(function(data) {
                        $('#loading').hide();
                        setTimeout(function() {
                            $('.header_status_text').text('');
                            $('.header_status').removeClass('_show _success _error');
                        },1000);

                    });
                });
            }
            if (meta.filetype == 'image') {
                $('#upload').trigger('click');
                $('#upload').on('change', function() {
                    var file = this.files[0];
                    if ($("input[name='image_file']").val() == '') {
                        return false
                    }
                    $('#loading').show();
                    var fd = new FormData($('#image_upload').get(0));
                    fd.append('file', file);
                    $.ajax({
                        type: 'POST',
                        url: '/image/add',
                        cache: false,
                        data: fd,
                        processData: false,
                        contentType: false
                    }).done(function(data) {
                        callback(data.image_url)
                    }).fail(function(data) {
                        $('.header_status_text').text('通信エラー');
                        $('.header_status').addClass('_show _error');

                    }).always(function(data) {
                        $('#loading').hide();
                        setTimeout(function() {
                            $('.header_status_text').text('');
                            $('.header_status').removeClass('_show _success _error');
                        },1000);

                    });
                });
            }
        }
    });
}
