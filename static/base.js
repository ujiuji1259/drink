var base_url = ''
if (window.location.href.indexOf('aoi') >= 0) {
    base_url = '/drinks'
}

$(function () {
    $('.jump_top').on('click', function () {
        location.href = base_url + "/";
    });

    $('.jump_logout').on('click', function () {
        location.href = base_url + "/logout";
    });

    $('.jump_admin').on('click', function () {
        location.href = base_url + "/admin";
    })
})