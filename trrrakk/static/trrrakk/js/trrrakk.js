var locale = window.navigator.userLanguage || window.navigator.language;

$(function() {
    $('time.locale').each(function() {
        const datetime = $(this).attr('datetime');
        const format = $(this).attr('format');
        $(this).text(moment(datetime).locale(locale).format(format));
    });
});