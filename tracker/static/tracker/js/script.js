if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

$(document).on('show.bs.modal', '#editRecord', function (event) {
    const button = $(event.relatedTarget);
    const modal = $(this);
    const record_id = button.data('record_id');
    modal.find("input[name='record_id']").val(record_id);

    console.info(button.data('record_id'));
    console.info(button.data('start_time'));
    console.info(button.data('end_time'));

    const start_timestamp = button.data('start_time').split('T');
    modal.find("input[name='start_date']").val(start_timestamp[0]);
    modal.find("input[name='start_time']").val(start_timestamp[1]);

    if(!button.data('end_time')) return;
    const end_timestamp = button.data('end_time').split('T');
    modal.find("input[name='end_date']").val(end_timestamp[0]);
    modal.find("input[name='end_time']").val(end_timestamp[1]);
});

$(document).on('show.bs.modal', '#deleteRecord', function (event) {
    const button = $(event.relatedTarget);
    const modal = $(this);
    const record_id = button.data('record_id');
    modal.find("input[name='record_id']").val(record_id);
});

$(function() { });
