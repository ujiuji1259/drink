var base_url = ''
if (window.location.href.indexOf('.jp') >= 0 || window.location.href.indexOf('.com') >= 0) {
    base_url = '/drink'
}

$(function () {
    $('.jump_top').on('click', function () {
        location.href = base_url + "/";
    });

    $('.jump_logout').on('click', function () {
        location.href = base_url + "/logout";
    });

    $('.jump_admin').on('click', function () {
        location.href = base_url + "/admin2";
    })
})

function get_day(index) {
    return '日月火水木金土'.charAt(index);
}
