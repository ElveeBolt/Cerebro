$("#btn-sidebar").click(function(){
  $("body").toggleClass("show-sidebar");
});

$("#btn-close-sidebar, #overlay").click(function(){
  $("body").removeClass("show-sidebar");
});