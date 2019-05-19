let buyTime = '20190411,12:00:00';

$(document).ready(function() {
    moment.locale('zh-cn');

    var interval = setInterval(function() {
        var momentBuy = moment(buyTime, 'YYYYMMDD,h:mm:ss');
        if (momentBuy.isAfter(moment())) {
            $('#buy_status').html(moment().format('LLLL') + ' 距离抢购还有' + momentBuy.fromNow(true));
        } else {
            $('#buy_status').html(moment().format('LLLL') + ' 抢购已结束！');
        }

    }, 100);
});

$('#buy').click(function(){
    $('#buy').prop('disabled', 'true');
    $('#buying_process').show();

    let process = $("#buying_processbar");

    var value = 0;
    const buying = setInterval(function(e){
        if (value !== 100) {
            value = parseInt(value) + 1;
            process.css("width", value + "%").text(value + "%");
            if (value>=0 && value<=30) {
                process.addClass("bg-danger");
            } else if (value>=30 && value <=60) {
                process.removeClass("bg-danger");
                process.addClass("bg-warning");
            } else if (value>=60 && value <=90) {
                process.removeClass("bg-warning");
                process.addClass("bg-info");
            } else if(value >= 90 && value<100) {
                process.removeClass("bg-info");
                process.addClass("bg-success");
            }
        } else {
            $.ajax({
                url: "/buy",
                data: $('#buying_form').serialize(),
                type: "POST",
                success: function(data) {
                    $('#buy').prop('disabled', false);
                    $('#buying_process').hide();
                    $('#buying_info .toast-body').html(data);
                    $('#buying_info').toast('show');
                },
                error: function(xhr, status, error) {
                    $('#buy').prop('disabled', false);
                    $('#buying_process').hide();
                    $('#buying_info .toast-body').html(xhr.responseText + xhr.status + xhr.readyState + xhr.statusText + status + error);
                    $('#buying_info').toast('show');
                }
            });
            clearInterval(buying);
        }
    }, 5);



});