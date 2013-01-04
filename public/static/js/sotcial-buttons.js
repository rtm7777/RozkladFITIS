$(document).ready(function() {
  window.___gcfg = {
    lang: 'uk'
      };
      (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/ru_RU/all.js#xfbml=1&appId=288131697957171";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
  !function(d,s,id){
    var js,fjs=d.getElementsByTagName(s)[0];
    if(!d.getElementById(id)){
      js=d.createElement(s);
      js.id=id;js.src="//platform.twitter.com/widgets.js";
      fjs.parentNode.insertBefore(js,fjs);
    }
  }(document,"script","twitter-wjs");
  $("#daycheck").change(function() { //Вибір між загальним заняттям і по парним чи непарним тижням
    if ($('#daycheck').is(':checked')) {
        $("#tag4, #tag5, #tag6, #sel2").prop({disabled: true});
        $("#btn-group2 button").prop({disabled: true});
        $(".modal_cont2 div label").addClass("label_disabled");
    } else {
        $("#tag4, #tag5, #tag6, #sel2").prop({disabled: false});
        $("#btn-group2 button").prop({disabled: false});
        $(".modal_cont2 div label").removeClass("label_disabled");
    }   
  }).change();
});