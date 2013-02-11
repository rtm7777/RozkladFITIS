function getCookie(name) { // Отримання значення csrftoken-ена 
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({    // Установка X-CSRFToken заголовку в Ajax запит
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(function() {
  $("#msub1, #msub2, #ssub1, #ssub2").autocomplete({
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
  $("#mteach1, #mteach2, #steach1, #steach2").autocomplete({
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
  $("#maud1").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#msel1").val()},
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
  $("#saud1").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#ssel1").val()},
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
  $("#maud2").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#msel2").val()},
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
  $("#saud2").autocomplete({
    source: function(request,response) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {auditory: request.term,
              korpus: $("#ssel2").val()},
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

function SendSubjectData() {  // Відправка Ajax на сервер для додавання заняття
  $.ajax({
    url: "/sendsubj",
    dataType: "jsonp",
    data: {
      para: $("#day").val(),
      group: $("#group").val(),
      evenodd: $("#daycheck").prop("checked"),
      subject1: $("#msub1").val(),
      teacher1: $("#mteach1").val(),
      audience1: $("#maud1").val(),
      house1: $("#msel1").val(),
      period1: $('#btn-group1 button.active').val(),
      subject2: $("#msub2").val(),
      teacher2: $("#mteach2").val(),
      audience2: $("#maud2").val(),
      house2: $("#msel2").val(),
      period2: $('#btn-group2 button.active').val(),
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      if (data.errors !== "true") {
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
        $("#subject_add_modal").modal('hide');
        $("#load_animation").hide("fast");
        ShowMessage("success", "dodano");
      } else {
        $("#load_animation").hide("fast");
        ShowModalMessage("#subject_add_modal", data.errors_message);
      };
    },
    error: function() {
      ShowMessage("error", "Виникла помилка при додаванні занять");
      $("#load_animation").hide("fast");
    }
  });
};

function SendStreamSubjectData() { // Відправка Ajax на сервер для додавання потокового заняття
  $.ajax({
    url: "/sendstreamsubj",
    dataType: "jsonp",
    data: {
      day: $("#stream_day").val(),
      pair: $("#stream_pair").val(),
      groups: $("#stream_groups").val(),
      evenodd: $("#streamdaycheck").prop("checked"),
      subject1: $("#ssub1").val(),
      teacher1: $("#steach1").val(),
      audience1: $("#saud1").val(),
      house1: $("#ssel1").val(),
      period1: $('#stream-btn-group1 button.active').val(),
      subject2: $("#ssub2").val(),
      teacher2: $("#steach2").val(),
      audience2: $("#saud2").val(),
      house2: $("#ssel2").val(),
      period2: $('#stream-btn-group2 button.active').val(),
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function() {
      $("#add_stream_modal").modal('hide');
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка при додаванні занять");
      $("#load_animation").hide("fast");
    }
  });
};

$(function() {
  $("#sendsubject").click(function() { // Провірка вікна дод. заняття на заповненість
    errors = false;
    if ($("#daycheck").prop("checked")) {
      if ($("#msub1").val() !== "") {
        if ($("#mteach1").val() == "" || $("#maud1").val() == "") {
          ShowModalMessage("#subject_add_modal", "Заповніть всі поля");
          errors = true;
        };
      }; 
    } else {
      if ($("#msub1").val() !== "") {
        if ($("#mteach1").val() == "" || $("#maud1").val() == "") {
          ShowModalMessage("#subject_add_modal", "Заповніть всі поля");e
          errors = true;
        };
      };
      if ($("#msub2").val() !== "") {
        if ($("#mteach2").val() == "" || $("#maud2").val() == "") {
          ShowModalMessage("#subject_add_modal", "Заповніть всі поля");;
          errors = true;
        };
      };
    };
    if (errors !== true) {
      SendSubjectData();
    };
  });
});

$(function() {
  $("#send_stream_subject").click(function() { // Провірка вікна дод. поток. заняття на заповненість
    errors1 = false;
    errors2 = false;
    if ($("#stream_groups").val() == "" || $("#stream_pair").val() == "" || $("#stream_day").val() == "") {
      errors1 = true;
    };
    if ($("#streamdaycheck").prop("checked")) {
      if ($("#ssub1").val() == "" || $("#steach1").val() == "" || $("#saud1").val() == "") {
        errors1 = true;
      };
    } else {
      if ($("#ssub1").val() == "" || $("#steach1").val() == "" || $("#saud1").val() == "") {
        errors1 = true;
      };
      if ($("#ssub2").val() == "" || $("#steach2").val() == "" || $("#saud2").val() == "") {
        errors2 = true;
      };
    };
    if (errors1 !== true && errors2 !== true) {
      SendStreamSubjectData();
    } else {
      ShowModalMessage("#add_stream_modal", "Заповніть всі поля");
    };
    
  });
});

$(function() { // Функція для входу користувача (Ajax)
  $("#send_login").click(function() {
    $.ajax({
      type:"POST",
      url:"/login",
      data: {'login': $("#login").val(),
             'password': $("#password").val()},
      success: function(data){
        alert("sdgsd");
      }
    });
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

//Повыдомлення в модальному вікні
function ShowModalMessage(modal, message) {
  $(modal+" .modal-footer .modal_message p b").text(message);
  $(modal+" .modal-footer .modal_message").show("fast").delay(1700);
  $(modal+" .modal-footer .modal_message").hide("fast");
};

//Очистка модального вікна
function ClearSubModal() { 
  $("#subject_add_modal .modal_container div div input").val('');
  $("#subject_add_modal .modal_container div .btn-group button").removeClass("active");
  $("#subject_add_modal .modal_container div .btn-group button:first-child").addClass("active");
  $("#msel1, #ssel1, #msel2, #ssel2").val("1");
};

//Установка кнопки періоду
//Потрібно переписать для підтримки IE8
function SetPeriodActive(evenodd, period) {
  if (evenodd == 1) {
    $(".modal_cont1 .btn-group button").removeClass("active");
    $(".modal_cont1 .btn-group button:nth-child("+period+")").addClass("active");
  } else if (evenodd == 2) {
    $(".modal_cont2 .btn-group button").removeClass("active");
    $(".modal_cont2 .btn-group button:nth-child("+period+")").addClass("active");
  };
  
}

function DisableModalOdd() {
  $("#msub2, #ssub2").prop({disabled: true});
  $("#mteach2, #steach2").prop({disabled: true});
  $("#maud2, #saud2").prop({disabled: true});
  $("#msel2, #ssel2").prop({disabled: true});
  $(".modal_container .modal_cont2 div button").prop({disabled: true});
  $(".modal_container .modal_cont2 div label").addClass("label_disabled");
}

function EnableModalOdd() {
  $("#msub2, #ssub2").prop({disabled: false});
  $("#mteach2, #steach2").prop({disabled: false});
  $("#maud2, #saud2").prop({disabled: false});
  $("#msel2, #ssel2").prop({disabled: false});
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
            ClearSubModal();
            $.map(data.sources, function(item) {
                if (item.pair_type == "кожен") {
                  $("#daycheck").prop({checked: true});
                  $("#msub1").val(item.subject);
                  $("#mteach1").val(item.teacher);
                  $("#maud1").val(item.audience);
                  $("#msel1").val(item.house);
                  SetPeriodActive(1, item.period);
                  DisableModalOdd();
                } else if (item.pair_type == "парна") {
                  $("#daycheck").prop({checked: false});
                  $("#msub2").val(item.subject);
                  $("#mteach2").val(item.teacher);
                  $("#maud2").val(item.audience);
                  $("#msel2").val(item.house);
                  SetPeriodActive(2, item.period);
                  EnableModalOdd();
                } else if (item.pair_type == "непарна") {
                  $("#daycheck").prop({checked: false});
                  $("#msub1").val(item.subject);
                  $("#mteach1").val(item.teacher);
                  $("#maud1").val(item.audience);
                  $("#msel1").val(item.house);
                  SetPeriodActive(1, item.period);
                  EnableModalOdd();
                };
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
        $("#daycheck").prop({checked: false});
        ClearSubModal();
        EnableModalOdd();
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

  $("#streamdaycheck").click(function() {
    if ($("#streamdaycheck").is(':checked')) {
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

  $("#stream_day_div ul li a").click(function() {
    $("#stream_day_div>a").html($(this).text()+" <span class='caret'></span>");
    $("#stream_day").val($(this).attr("value"));
  });

  $("#stream_pair_div ul li a").click(function() {
    $("#stream_pair_div>a").html($(this).text()+" Пара <span class='caret'></span>");
    $("#stream_pair").val($(this).attr("value"));
  });

  $('#groups-popover').popover({
    trigger: 'manual',
    html: true,
    placement: 'bottom',
    title: $('#groups-header-popover').html(),
    content: $('#groups-footer-popover').html()
  }).click(function (e) {
    e.preventDefault();
    $(this).popover('show');
  });

  $(document).on("click", "#btn-close-gr", function() {
    $('#groups-popover').popover('hide');
  });

  $(document).on("click", "#stream_groups_ok", function() {
    var data = "";
    $('#group_popover_buttons .btn.active').each(function() {
      data += $(this).attr("value")+",";
    });
    $("#stream_groups").val(data);
    $('#groups-popover').popover('hide');
  });
});

