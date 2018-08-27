if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

$(function() {
    $('#editRecord').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        var record_id = button.data('record_id');
        modal.find("input[name='record_id']").val(record_id);

        var start_time = button.data('start_time');
        modal.find("input[name='start_time']").val(start_time);

        var end_time = button.data('end_time');
        modal.find("input[name='end_time']").val(end_time);
    });

    $('#deleteRecord').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modal = $(this);
        var record_id = button.data('record_id');
        modal.find("input[name='record_id']").val(record_id);
    });
});
