$(function() {
  $('ul#members a.remove').live('click', function(e) {
    var $this = $(this);
    var href = $this.attr('href');
    $.ajax({
      url: href,
      type: 'POST'
    })
    .success(function() {
      console.log('yay!');
      $this.closest('li').remove();
    })
    .error(function() {
      console.log('show error dialog');
    });
    e.preventDefault();
  });
  
  // Dropdown example for topbar nav
  // ===============================

  $("body").bind("click", function (e) {
    $('.dropdown-toggle, .menu').parent("li").removeClass("open");
  });
  $(".dropdown-toggle, .menu").click(function (e) {
    var $li = $(this).parent("li").toggleClass('open');
    return false;
  });
})
