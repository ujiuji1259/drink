var toDoubleDigits = function (num) {
    if (num.length === 1) {
        num = "0" + num;
    }
    return num;
}

function init_chart(drink_data, year, month, day) {
    let chart_data = [];
    let labels = [];
    let CurrentDate = new Date(year, month, day);
    let weekdate = CurrentDate.getDay();

    for (let i = 0; i < 7; i++) {
        var tableDate = new Date(year, month, day);
        tableDate.setDate(tableDate.getDate() - weekdate + 2 + i);
        let tmp = tableDate.getFullYear().toString() + '-' + toDoubleDigits(tableDate.getMonth().toString()) + '-' + toDoubleDigits(tableDate.getDate().toString());
        labels.push(tmp);
        if (tmp in drink_data) {
            chart_data.push(drink_data[tmp]);
        }
    }

    var ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            lineTension: 0,
            labels: labels,
            datasets: [
                {
                    label: '純粋アルコール量',
                    data: chart_data,
                    borderColor: 'rgb(255, 0, 0, 1)',
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'アルコール',
                fontSize: 25
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMax: 10,
                        suggestedMin: 0,
                        stepSize: 10,
                        fontSize: 18
                    }
                }],
                xAxes: [{
                    ticks: {
                        fonSize: 18
                    }
                }]
            }
        }
    });
}

function init_table(data, year, month, day) {
    let CurrentDate = new Date(year, month, day);
    let weekdate = CurrentDate.getDay();
    var columns = [];
    columns.push({'field': 'title', 'title': '日付', 'width': 150, align: 'center', valign: 'middle',});
    var table_data = [];
    var rows = {'text': '日記', 'nes': 'メンタル情報', 'tags': 'ハッシュタグ'};
    var column_complete_flag = false;

    for (var single_row in rows) {
        var row = {};
        row['title'] = rows[single_row];
        for (let i = 0; i < 7; i++) {
            var tableDate = new Date(year, month, day);
            tableDate.setDate(tableDate.getDate() + i - weekdate + 2);
            let tmp = tableDate.getFullYear().toString() + '-' + toDoubleDigits(tableDate.getMonth().toString()) + "-" + toDoubleDigits(tableDate.getDate().toString());
            // for (var single in data) {
            //     row[single] = data[single][single_row];
            //     if (!column_complete_flag) {
            //         columns.push({'field': single, 'title': single});
            //     }
            // }
            if (tmp in data) {
                row[tmp] = data[tmp][single_row];
            }
            if (!column_complete_flag) {
                columns.push({'field': tmp, 'title': tmp});
            }
        }
        table_data.push(row);
        column_complete_flag = true;
    }

    $('#table').bootstrapTable('destroy');
    $('#table').bootstrapTable({
        classes: 'table table-no-bordered',
        data: table_data,
        columns: columns,
    });
}

function get_date() {
    let date = new Date(2020, 6, 25);
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    return [year, month, day, date]
}

function get_admin_data() {
    var formData = new FormData();
    var selected_name = $('.selectpicker').val();
    formData.append('username', selected_name);
    $.ajax({
            url: base_url + '/get_admin_data',
            data: formData,
            type: "POST",
            contentType: false,
            processData: false,
            success: function (result) {
                $('#patient_name').text(selected_name);
                if (!$('.card-body').is(':visible')) {
                    $('.card-body').slideDown();
                }
                var selected_date = get_date();
                post_result = result;
                init_chart(result['drink_data'], selected_date[0], selected_date[1], selected_date[2])
                init_table(result['data'], selected_date[0], selected_date[1], selected_date[2])
            }
        });
}

var post_result = {};
var chat = null;
$(function () {
    get_admin_data();

    var selected_date = get_date();
    var date = selected_date[3];
    $('.move-arrow').on('click', function (event) {
        var action = $(this).attr('data-action');
        if (action === 'move-prev') {
            date.setDate(date.getDate() - 7);
        } else if (action === 'move-next') {
            date.setDate(date.getDate() + 7);
        }
        init_chart(post_result['drink_data'], date.getFullYear(), date.getMonth()+1, date.getDate());
        init_table(post_result['data'], date.getFullYear(), date.getMonth()+1, date.getDate());
    });

    $('.selectpicker').on('change', function () {
        get_admin_data();
    })
})