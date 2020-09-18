var result = {};

function init_calendar() {
    return new tui.Calendar('#calendar', {
        defaultView: 'month',
        useCreationPopup: false,
        useDetailPopup: false,
        month: {
            daynames: ['日', '月', '火', '水', '木', '金', '土'],
            startDayOfWeek: 0,
            narrowWeekend: false
        }
    });
}

var current_height = document.documentElement.clientHeight;
$('#calendar').css({'height': current_height * 0.8});
var cal = init_calendar();

function getDataAction(target) {
    return target.dataset ? target.dataset.action : target.getAttribute('data-action');
}

function onClickNavi(e) {
    var action = getDataAction(e.target);
    switch (action) {
        case 'move-prev':
            cal.prev();
            break;
        case 'move-next':
            cal.next();
            break;
        case 'move-today':
            cal.today();
            break;
        default:
            return;
    }
    setRenderRangeText();
}

function setRenderRangeText() {
    var renderRange = document.getElementById('renderRange');
    var options = cal.getOptions();
    var viewName = cal.getViewName();
    var html = [];
    if (viewName === 'day') {
        html.push(moment(cal.getDate().getTime()).format('YYYY年MM月DD日'));
    } else if (viewName === 'month' &&
        (!options.month.visibleWeeksCount || options.month.visibleWeeksCount > 4)) {
        html.push(moment(cal.getDate().getTime()).format('YYYY年MM月'));
    } else {
        html.push(moment(cal.getDateRangeStart().getTime()).format('YYYY年MM月DD日'));
        html.push(' ~ ');
        html.push(moment(cal.getDateRangeEnd().getTime()).format(' MM月DD日'));
    }
    renderRange.innerHTML = html.join('');
}

function init_modal() {
    $('#first-panel').show();
    $('#second-panel').hide();
    $('#third-panel').hide();
    $('#next-button').show();
    $('#next-button').attr('disabled', true);
    $('#submit-button').hide();
    $('#progressbar').css('width', '2%');
    $('input[name="isdrink"]').prop('checked', false);
    $('#drink_text').val("");
    $('.drink-slider').slider('refresh', {useCurrentValue: false});
}

$(function () {
    var today = new Date();
    setRenderRangeText();

    $('.move-button').on('click', function (event) {
        onClickNavi(event);
    });

    $('.drink-slider').slider({
        formatter: function (value) {
            return value;
        }
    });

    $('.drink-slider').on('change', function () {
        var val = $(this).val();
        if (val.length > 0 && parseInt(val) > 0) {
            $('#progressbar').css('width', '66%');
            $('#next-button').attr('disabled', false);
        }
        var beer = parseInt($('input[name="beer"]').val());
        var syo = parseInt($('input[name="syo"]').val());
        var wine = parseInt($('input[name="wine"]').val());
        var highball = parseInt($('input[name="highball"]').val());
        var jap = parseInt($('input[name="jap"]').val());
        var other = parseInt($('input[name="other"]').val());
        if (beer + syo + wine + highball + jap + other === 0) {
            $('#progressbar').css('width', '33%');
            $('#next-button').attr('disabled', true);
        }
    });

    $('input[name="other"]').on('change', function () {
        var val = $(this).val();
        if (val.length > 0 && parseInt(val) > 0) {
            $('#other_re_text').slideDown();
            $('#progressbar').css('width', '66%');
        }
        if (val.length > 0 && parseInt(val) === 0) {
            $('#other_re_text').slideUp();
            $('#progressbar').css('width', '33%');
        }
    });

    $('#drink_text').on('input', function () {
        var val = $(this).val();
        if (val.length >= 5) {
            $('#progressbar').css('width', '100%');
        }
        if (val.length === 0) {
            if ('drink' in result) {
                $('#progressbar').css('width', '66%');
            } else if ('notdrink' in result) {
                $('#progressbar').css('width', '50%');
            }
        }
    });

    $('.isdrink').on('click', function () {
        $('#next-button').attr('disabled', false);
        var selected = $(this).val();
        if (selected === 'yes') {
            $('#progressbar').css('width', '33%');
            if ('nodrink' in result) {
                delete result.nodrink
            }
            result['drink'] = "";
        } else if (selected === 'no') {
            $('#progressbar').css('width', '50%');
            if ('drink' in result) {
                delete result.drink
            }
            result['nodrink'] = "";
        }
    });

    $('#createModal').on('hidden.bs.modal', function (e) {
        init_modal();
    });

    $('#next-button').on('click', function () {
        var dairy_value = {};
        if ('drink' in result) {
            if ($('#first-panel').is(':visible') && !$('#second-panel').is(':visible') && !$('#third-panel').is(':visible')) {
                $.get(base_url + "/get_dairy_value/" + $('#clicked-date').val(), function (data, status) {
                    dairy_value = data;
                    for (var key in dairy_value) {
                        $('input[name="' + key + '"').attr('value', dairy_value[key]);
                        if ('text' in data) {
                            $('#drink_text').text(dairy_value['text']);
                        }
                    }
                });
                $('#first-panel').fadeOut();
                $('#second-panel').fadeIn();
                $('#next-button').attr('disabled', true);
            } else if (!$('#first-panel').is(':visible') && $('#second-panel').is(':visible') && !$('#third-panel').is(':visible')) {
                result['beer'] = $('input[name="beer"]').val();
                result['syo'] = $('input[name="syo"]').val();
                result['wine'] = $('input[name="wine"]').val();
                result['highball'] = $('input[name="highball"]').val();
                result['jap'] = $('input[name="jap"]').val();
                result['other'] = $('input[name="other"]').val();
                result['other_re'] = $('input[name="other_re"]').val();
                $('#second-panel').fadeOut();
                $('#third-panel').fadeIn();
                $('#next-button').hide();
                $('#submit-button').show();
            }
        } else if ('nodrink' in result) {
            if ($('#first-panel').is(':visible') && !$('#third-panel').is(':visible')) {
                $('#first-panel').fadeOut();
                $('#third-panel').fadeIn();
                $('#next-button').hide();
                $('#submit-button').show();
            }
        }
    });

    $('#submit-button').on('click', function () {
        if ($('#drink_text').val().length <= 0 ) {
            bootbox.alert({
                    title: "確認",
                    message: "一行日記を書いてください",
                    // centerVertical: true,
                    size: 'small',
                    buttons: {
                        ok: {
                            label: '閉じる',
                            className: 'btn-secondary'
                        }
                    }
                });
            return
        }
        if ('drink' in result) {
            result['drink'] = $('#drink_text').val();
            post_url = base_url + '/drink';
        } else if ('nodrink' in result) {
            result['nodrink'] = $('#drink_text').val();
            post_url = base_url + '/nodrink';
        }
        $('#progressbar').css('width', '100%');
        // $.ajax({
        //     type: "post",
        //     url: post_url,
        //     data: JSON.stringify(result),
        //     contentType: "application/json; charset=utf-8",
        //     dataType: "json",
        //     success: function () {
        //         console.log(111);
        //     }
        // });
        $('#createModal').modal('hide');
        alert(JSON.stringify(result));
    });

    cal.on({
        'clickSchedule': function (e) {
            console.log('clickSchedule', e);
        },
        'beforeCreateSchedule': function (e) {
            var clicked_date = e.start.toDate();
            var guideEl$ = e.guide.guideElement ? e.guide.guideElement : e.guide.guideElements[Object.keys(e.guide.guideElements)[0]];
            if ($('.tui-full-calendar-month-guide-block').length > 1) {
                $('.tui-full-calendar-month-guide-block').each(function () {
                    if (!$(this).is($(guideEl$))) {
                        $(this).remove();
                    }
                });
            }
            if (clicked_date > today) {
                bootbox.alert({
                    title: "確認",
                    message: "未来の日記を書くことはできません",
                    // centerVertical: true,
                    size: 'small',
                    buttons: {
                        ok: {
                            label: '閉じる',
                            className: 'btn-secondary'
                        }
                    }
                });
                return
            }
            var clicked_date = e.start.getTime();
            var day = e.start.toDate().getDay();
            $('#clicked-date').val(moment(clicked_date).format('YYYY-MM-DD'));
            $('#createModalLabel').text(moment(clicked_date).format('YYYY年MM月DD日') + "（" + get_day(day) + "）");
            $('#createModal').modal('show');
        },
        'beforeUpdateSchedule': function (e) {
            console.log('beforeUpdateSchedule', e);
            e.schedule.start = e.start;
            e.schedule.end = e.end;
            cal.updateSchedule(e.schedule.id, e.schedule.calendarId, e.schedule);
        },
        'beforeDeleteSchedule': function (e) {
            console.log('beforeDeleteSchedule', e);
            cal.deleteSchedule(e.schedule.id, e.schedule.calendarId);
        }
    });

});
