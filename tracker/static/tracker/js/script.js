if ('Notification' in window) {
    if (Notification.permission !== "granted" && Notification.permission !== "denied") {
        Notification.requestPermission();
    }
}

$(document).on('show.bs.modal', '#editRecord', function (event) {
    const button = $(event.relatedTarget);
    const modal = $(this);
    const record_id = button.data('record_id');
    modal.find("input[name='record_id']").val(record_id);

    const start_time = button.data('start_time');
    modal.find("input[name='start_time']").val(start_time);

    const end_time = button.data('end_time');
    if(!end_time) return;
    modal.find("input[name='end_time']").val(end_time);
});

$(document).on('show.bs.modal', '#deleteRecord', function (event) {
    const button = $(event.relatedTarget);
    const modal = $(this);
    const record_id = button.data('record_id');
    modal.find("input[name='record_id']").val(record_id);
});

$(function() { });
