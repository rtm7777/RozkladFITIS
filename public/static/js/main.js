

$(function() {
  $("#tag1, #tag4").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/ac",
        dataType: "jsonp",
        data: {predmet: request.term},
        success: function(data) {
          response($.map(data.sources, function(item) {
            return {
              label: item.name+' - '+item.type,
              value: item.name+' - '+item.type
            }
          }));
        }
      });
    },
    minLength: 1,
  });
});

$(function() {
  $("#tag2, #tag5").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/tch",
        dataType: "jsonp",
        data: {teacher: request.term},
        success: function(data) {
          response($.map(data.sources, function(item) {
            return {
              label: item.lastname+' '+item.firstname+' '+item.middlename,
              value: item.lastname+' '+item.firstname+' '+item.middlename
            }
          }));
        }
      });
    },
    minLength: 1,
  });
});

$(function() {
  $("#tag3").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#sel1").val()},
        success: function(data) {
          response($.map(data.sources, function(item) {
            return {
              label: item.number,
              value: item.number
            }
          }));
        }
      });
    },
    minLength: 1,
  });
});

$(function() {
  $("#tag6").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#sel2").val()},
        success: function(data) {
          response($.map(data.sources, function(item) {
            return {
              label: item.number,
              value: item.number
            }
          }));
        }
      });
    },
    minLength: 1,
  });
});

$(function() {
  $("#sendsubject").click(function() {
    $.ajax({
      url: "/sendsubj",
      dataType: "jsonp",
      data: {
        para: $("#day").val(),
        group: $("#group").val(),
        evenodd: $("#daycheck").prop("checked"),
        subject1: $("#tag1").val(),
        teacher1: $("#tag2").val(),
        audience1: $("#tag3").val(),
        house1: $("#sel11").val(),
        period1: $('#btn-group1 button.active').val(),
        subject2: $("#tag4").val(),
        teacher2: $("#tag5").val(),
        audience2: $("#tag6").val(),
        house2: $("#sel12").val(),
        period2: $('#btn-group2 button.active').val(),
      },
      beforeSend: function() {
        $("#load_animation").show("fast");
      },
      success: function(data) {
        ShowMessage("success", "Предмет додано");
        $("#load_animation").hide("fast");
        $.ajax({
          url: "/getsubjsingle",
          dataType: "jsonp",
          data: {
            para: $("#day").val(),
            group: $("#group").val(),
          },
          beforeSend: function() {
            $("#load_animation").show("fast");
          },
          success: function(data) {
            var id_day = $("#day").val().charAt(0);
            var id_pair = $("#day").val().split(' ');
            $("#"+id_day+"_"+id_pair[1]+" td:last-child").removeClass("single_admin").html('<p class="null"></p><hr><p class="null"></p>');
            $.map(data.sources, function(item) {
              if (item.tupe == "кожен") {
                $('#'+item.daypair+' .subject_content').addClass("single_admin").text(item.subject);
              } else if (item.tupe == "непарна") {
                $('#'+item.daypair+' td p:first-child').removeClass("null").text(item.subject);
              } else if (item.tupe == "парна") {
                $('#'+item.daypair+' td p:last-child').removeClass("null").text(item.subject);
              };
            });
            $("#load_animation").hide("fast");
          },
          error: function() {
            ShowMessage("error", "Виникла помилка при відображенні")
            $("#load_animation").hide("fast");
          }
        });
      },
      error: function() {
        ShowMessage("error", "Виникла помилка при додаванні занять");
        $("#load_animation").hide("fast");
      }
    });
    $('#subject_add_modal').modal('hide');
  });
});

$(function() {
  $("#send_login").click(function() {
    $.post('/login_ajax', {username: $("#login").val(), password: $("#password").val()})
      .done(function(data) {
        if (data.logined == "true") {
          window.location.reload()
        } else {
          ShowMessage('error', 'Введено некоректні дані')
        };
      })
      .fail(function() {ShowMessage('error', 'Виникла помолка в процесі авторизації')})

  });
});

$(function() {
  $("#send_logout").click(function() {
    $.post('/logout_ajax')
      .done(function(data) {
        if (data.logout == "true") {
          window.location.reload()
        } else {
          ShowMessage('error', 'Введено некоректні дані')
        };
      })
      .fail(function() {ShowMessage('error', 'Виникла помолка в процесі авторизації')})

  });
});

$(function() { //Очистка полів введення у вікні додавання заняття
  $(".modal_container div div button").click(function() {
    var button = $(this).val();
    $(button).val('');
  });
});

function ShowMessage(type, message) { // Показ повідомлень
  $("#alert_"+type+" h4").text(message);
  $("#alert_"+type).slideDown().delay(1500);
  $("#alert_"+type).slideUp();
};

function ClearSubModal() {
  $("#subject_add_modal .modal_container div div input").val('');
  $("#subject_add_modal .modal_container div .btn-group button").removeClass("active");
  $("#subject_add_modal .modal_container div .btn-group button:first-child").addClass("active");
}

function DisableModalOdd() {
  $("#tag4").prop({disabled: true});
  $("#tag5").prop({disabled: true});
  $("#tag6").prop({disabled: true});
  $("#sel12").prop({disabled: true});
  $(".modal_container .modal_cont2 div button").prop({disabled: true});
  $(".modal_container .modal_cont2 div label").addClass("label_disabled");
}

function EnableModalOdd() {
  $("#tag4").prop({disabled: false});
  $("#tag5").prop({disabled: false});
  $("#tag6").prop({disabled: false});
  $("#sel12").prop({disabled: false});
  $(".modal_container .modal_cont2 div button").prop({disabled: false});
  $(".modal_container .modal_cont2 div label").removeClass("label_disabled");
}

$(document).ready(function() {

  $("#tab1 table tbody tr").dblclick(function() { //Виклик вікна додавання заняття
    if ($("#group").val() !== "") {
      var elem = $(this);
      $("#load_animation").show("fast");
      $("#day").prop({value: elem.attr("customdata")});
      $("#subject_add_modal div h3").text("Заняття - "+elem.attr("customdata").substring(1)+" пара");
      if (elem.find("td:last-child").html() !== '<p class="null"></p><hr><p class="null"></p>') {
        $.ajax({
          url: "/getsubjsmodal",
          dataType: "jsonp",
          data: {
            para: $("#day").val(),
            group: $("#group").val(),
          },
          beforeSend: function() {
            $("#load_animation").show("fast");
          },
          success: function(data) {
            $.map(data.sources, function(item) {
              if (item.amount == "true") {
                if (item.pair_type == "кожен") {
                  $("#daycheck").prop({checked: true});
                  DisableModalOdd();
                } else {
                  $("#daycheck").prop({checked: false});
                  EnableModalOdd();
                };
                $("#tag1").val(item.subject);
                $("#tag2").val(item.teacher);
                $("#tag3").val(item.audience);
              } else if (item.tupe == "непарна") {
                $('#'+item.daypair+' .subject_content p:first-child').removeClass("null").text(item.subject);
              }
            });
            $('#subject_add_modal').modal('show');
            $("#load_animation").hide("fast");
          },
          error: function() {
            $('#subject_add_modal').modal('show');
            ShowMessage("error", "Виникла помилка при завантаженні");
            $("#load_animation").hide("fast");
          }
        });
      } else {
        ClearSubModal();
        $('#subject_add_modal').modal('show');
        $("#load_animation").hide("fast");
      };
    } else {
      ShowMessage("error", "Спочатку виберіть групу");
    };
  });

  $("#toTop").hide();
 
  $(function () {  //функція для прокрутки сторінки вгору
      $(window).scroll(function () {
          if ($(this).scrollTop() > 110)
                      {
              $('#toTop').fadeIn();
          } else {
              $('#toTop').fadeOut();
          }
      });
      $('#toTop').click(function () {
          $('body,html').animate({
              scrollTop: 0
          }, 400);
          return false;
      });
  });

  $("#group_id li a").click(function() { // Завантаження розкладу для сторінки адміністрування
    var group = $(this);
    $("#group").prop({value: group.attr("value")});
    $("#group_name").text("Група - " + group.attr("value"));
    $.ajax({
      url: "/getsubjs",
      dataType: "jsonp",
      data: {
        group: group.attr("value"),
      },
      beforeSend: function() {
        $("#load_animation").show("fast");
      },
      success: function(data) {
        $("tr td:last-child").removeClass("single_admin").html('<p class="null"></p><hr><p class="null"></p>');
        $.map(data.sources, function(item) {
          if (item.tupe == "кожен") {
            $('#'+item.daypair+' .subject_content').addClass("single_admin").text(item.subject);
          } else if (item.tupe == "непарна") {
            $('#'+item.daypair+' .subject_content p:first-child').removeClass("null").text(item.subject);
          } else if (item.tupe == "парна") {
            $('#'+item.daypair+' .subject_content p:last-child').removeClass("null").text(item.subject);
          };
        });
        ShowMessage("info", "Вибрано групу " + group.attr("value"));
        $("#load_animation").hide("fast");
      },
      error: function() {
        ShowMessage("error", "Виникла помилка");
        $("#load_animation").hide("fast");
      }
    });
  });

  $("#daycheck").click(function() {
    if ($("#daycheck").is(':checked')) {
      DisableModalOdd();
    } else {
      EnableModalOdd()
    };
  });

  $("#clearcheck").change(function() { //Провірка згоди на очистку розкладу
    if ($('#clearcheck').is(':checked')) {
        $("#clear_schedule").prop({disabled: false});
    } else {
        $("#clear_schedule").prop({disabled: true});
    }   
  }).change();

  $("a[href='#clear_schedule_modal']").click(function() { //Скидання стану вікна очистки розкладу
    $("#clearcheck").prop({checked: false})
    $("#clear_schedule").prop({disabled: true});
  });

  $("#myTab li a").click(function() {
    var tab = $(this);
    $("#rozklad_span3 div").slideUp("slow");
    $("#"+tab.attr("value")).slideDown("slow");
  });

});