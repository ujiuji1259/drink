var toDoubleDigits = function (num) {
    if (num.length === 1) {
        num = "0" + num;
    }
    return num;
}

function drawChart(drink_data, year, month, day) {
    let data = [];
    let labels = [];
    let CurrentDate = new Date(year, month, day);
    let weekdate = CurrentDate.getDay();

    for (let i=0; i < 7; i++) {
        var tableDate = new Date(year, month, day);
        tableDate.setDate(tableDate.getDate() -weekdate + 2 + i);
        let tmp = tableDate.getFullYear().toString() + '-' + toDoubleDigits(tableDate.getMonth().toString()) + '-' + toDoubleDigits(tableDate.getDate().toString());
        labels.push(tmp);
        data.push(drink_data[tmp])
    }

    var ctx = document.getElementById("myChart").getContext("2d");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            lineTension: 0,
            labels: labels,
            datasets: [
                {
                    label: '純粋アルコール量',
                    data: data,
                    borderColor: "rgba(255,0,0,1)"
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
                xAxes: {
                    ticks: {
                        fonSize: 18
                    }
                }
            }
        }
    });
}

