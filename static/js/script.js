jQuery(document).ready(function ($) {
    /*------Registration popup------*/
    $('#regShowForm').on('click', function (e) {
        $('.mtMedia-wrap').css('display', 'none');
        $('.regNew-form-wrap').css('display', 'flex');;
    });
    $('.fgPass').on('click', function (e) {
        event.preventDefault();

        $('.overlay').fadeIn();
    });
    $('.close-modal').on('click', function (e) {
        $('.overlay').fadeOut();

    });
    /*------End Registration popup------*/

    /*------Header-menu------*/
    $('.account__link-shop').on('click', function (e) {
        e.preventDefault();
        $(this).addClass('account__link--active');
        $('.shop-popup').show();

    });
    $(document).mouseup(function (e) {
        var block = $(".shop-popup");
        if (!block.is(e.target) &&
            block.has(e.target).length === 0) {
            $('.account__link-shop').removeClass('account__link--active');
            block.hide();
        }
    });

    /*------End Header-menu------*/
    /*------Form styler list------*/
    $('#list-filter').styler();

    /*------End Form styler list------*/
    /*------Form styler details------*/
    $('#form-details').find('input').styler();
    $('#form-details').find('select').styler();
    $('.item-quantity').find('input').styler();
    // $('input, select').styler();

    /*------End Form styler details------*/
    /*----- POUPUP-----*/
    $('.profile-info__change-pass').on('click', function (e) {
        $('.overlay').fadeIn();
        $('.popup').fadeIn();
    });

    $('.popup-close').on('click', function (e) {
        $('.overlay').fadeOut();
        $('.popup').fadeOut();
    });
    $('.overlay').on('click', function (e) {
        $('.overlay').fadeOut();
        $('.popup').fadeOut();
    });
    /*-----POPUP END-----*/
});