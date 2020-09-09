function csv2Array(str) {
    var csvData = [];
    var lines = str.split("\n");
    for (var i = 0; i < lines.length; ++i) {
        var cells = lines[i].split(",");
        csvData.push(cells);
    }
    return csvData;
}

function getData(filePath) {
    var req = new XMLHttpRequest();
    req.open("GET", filePath, true);
    req.onload = function() {
        data = csv2Array(req.responseText);
    }
    return data;
}

function drawChart() {
    var data = getData('/home/ujiie/narrative/current.csv')
    var tmpLabels = [], tmpData = [];
    for (var row in data) {
        tmpLabels.push(data[row][0])
        tmpData.push(data[row][1])
    };

    var ctx = document.getElementById("myChart");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: tmpLabels,
            data: tmpData
        }
    });
}

