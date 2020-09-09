var toDoubleDigits = function (num) {
    if (num.length === 1) {
        num = "0" + num;
    }
    return num;
}

function drawTable(data, year, month, day) {
    let CurrentDate = new Date(year, month, day);
    let weekdate = CurrentDate.getDay();
    
    let weekday = '<thead class="thead-dark">';
    weekday += "<tr>";
    weekday += "<th>日付</th>";
    for (let i=0; i < 7; i++) {
        weekday += "<th>";
        var tableDate = new Date(year, month, day);
        tableDate.setDate(tableDate.getDate() -weekdate + 2 + i);
        weekday += tableDate.getMonth().toString() + "-" + tableDate.getDate().toString();
        weekday += "</th>";
    }

    weekday += "</tr>";
    weekday += "</thead>";

    weekday += "<tbody>";
    weekday += "<tr>";
    weekday += "<td>メンタル情報</td>";
    for (let i=0; i < 7; i++) {
        weekday += "<td>";
        var tableDate = new Date(year, month, day);
        tableDate.setDate(tableDate.getDate() + i - weekdate + 2);
        let tmp = tableDate.getFullYear().toString() + '-' + toDoubleDigits(tableDate.getMonth().toString()) + "-" + toDoubleDigits(tableDate.getDate().toString());

        if (data[tmp]) {
            for (let i=0; i < data[tmp]['nes'].length; i++) {
                weekday += data[tmp]['nes'][i] + "<br>";
            }
        }
        weekday += "</td>";
    }

    weekday += "</tr>";

    weekday += "<tr>";
    weekday += "<td>ハッシュタグ</td>";
    for (let i=0; i < 7; i++) {
        weekday += "<td>";
        var tableDate = new Date(year, month, day);
        tableDate.setDate(tableDate.getDate() + i - weekdate + 2);
        let tmp = tableDate.getFullYear().toString() + '-' + toDoubleDigits(tableDate.getMonth().toString()) + "-" + toDoubleDigits(tableDate.getDate().toString());

        if (data[tmp]) {
            for (let i=0; i < data[tmp]['tags'].length; i++) {
                weekday += data[tmp]['tags'][i][1] + "<br>";
            }
        }
        weekday += "</td>";
    }

    weekday += "</tr>";

    weekday += "</tbody>";
    document.getElementById("mytable").innerHTML = '<table class="table">' + weekday + "</table>";
}


