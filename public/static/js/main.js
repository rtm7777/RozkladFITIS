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


////////// AJAX SECTION //////////
$(function() {  // Ajax для автозаповнення предмету
  $("#msub1, #msub2, #ssub1, #ssub2").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/ac",
        dataType: "jsonp",
        data: {query: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.name+' - '+item.type;
          }));
        }
      });
    },
  });
});

$(function() {  // Ajax для автозаповнення викладача
  $("#mteach1, #mteach2, #steach1, #steach2").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/tch",
        dataType: "jsonp",
        data: {query: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.lastname+' '+item.firstname+' '+item.middlename;
          }));
        }
      });
    },
  });
});

$(function() {  // Ajax для автозаповнення аудиторії
  $("#maud1, #saud1, #maud2, #saud2").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {query: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.number;
          }));
        }
      });
    },
  });
});

function SendSubjectData(lining) {  // Відправка Ajax на сервер для додавання заняття
  $.ajax({
    url: "/sendsubj",
    dataType: "jsonp",
    data: {
      lining: lining,
      para: $("#day").val(),
      group: $("#group").val(),
      evenodd: $("#daycheck").prop("checked"),
      subject1: $("#msub1").val(),
      teacher1: $("#mteach1").val(),
      audience1: $("#maud1").val(),
      period1: $('#btn-group1 button.active').val(),
      subject2: $("#msub2").val(),
      teacher2: $("#mteach2").val(),
      audience2: $("#maud2").val(),
      period2: $('#btn-group2 button.active').val(),
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      if (data.errors !== "true") {
        $.ajax({  // Ajax для відображення доданого предмету в таблиці
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
            var dnd_html = $(".dnd_live").html();
            var id_day = $("#day").val().charAt(0);
            var id_pair = $("#day").val().split(' ');
            $("#"+id_day+"_"+id_pair[1]+" td:last-child").removeClass("single_admin").html('<p class="null"></p><hr><p class="null"></p>'+dnd_html);
            $.map(data.sources, function(item) {
              if (item.tupe == "кожен") {
                $('#'+item.daypair+' .subject_content').html('<p class="single_sub">'+item.subject+'</p>'+dnd_html);
              } else if (item.tupe == "непарна") {
                $('#'+item.daypair+' td p:first').removeClass("null").text(item.subject);
              } else if (item.tupe == "парна") {
                $('#'+item.daypair+' td p:last').removeClass("null").text(item.subject);
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
        if (data.lining == "true") {
          $("#load_animation").hide("fast");
          ShowModalMessageAdv("#subject_add_modal", "Можлива накладка");
        } else {
          $("#load_animation").hide("fast");
          ShowModalMessage("#subject_add_modal", data.errors_message);
        };
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
      period1: $('#stream-btn-group1 button.active').val(),
      subject2: $("#ssub2").val(),
      teacher2: $("#steach2").val(),
      audience2: $("#saud2").val(),
      period2: $('#stream-btn-group2 button.active').val(),
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      if (data.errors !== "true") {
        if ($("#group").val() !== "") {
          GetSubjects($("#group").val(), false)
        };
        $("#add_stream_modal").modal('hide');
        $("#load_animation").hide("fast");
        ShowMessage("success", "dodano");
      } else {
        $("#load_animation").hide("fast");
        ShowModalMessage("#add_stream_modal", data.errors_message);
      };
    },
    error: function() {
      ShowMessage("error", "Виникла помилка при додаванні занять");
      $("#load_animation").hide("fast");
    }
  });
};

function GetSubjects(group_val, message) {  // Отримання JSON занять для певної групи і їх відображення
  $.ajax({
    url: "/getsubjs",
    dataType: "jsonp",
    data: {
      group: group_val,
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      var dnd_html = $(".dnd_live").html();
      $("tr td:last-child").removeClass("single_admin").html('<p class="null"></p><hr><p class="null"></p>'+dnd_html);
      $.map(data.sources, function(item) {
        if (item.tupe == "кожен") {
          $('#'+item.daypair+' .subject_content').html('<p class="single_sub">'+item.subject+'</p>'+dnd_html);
        } else if (item.tupe == "непарна") {
          $('#'+item.daypair+' .subject_content p:first').removeClass("null").text(item.subject);
        } else if (item.tupe == "парна") {
          $('#'+item.daypair+' .subject_content p:last').removeClass("null").text(item.subject);
        };
      });
      if (message == true) {
        ShowMessage("info", "Вибрано групу " + group_val);
      };
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function SingleModalWindow(elem) {  // Отримання JSON занять для конкретної групи, дня, пари і їх відображення
  if ($("#group").val() !== "") {
    $("#load_animation").show("fast");
    $("#day").prop({value: elem.attr("customdata")});
    $("#subject_add_modal div h3").text("Заняття - "+elem.attr("customdata").substring(1)+" пара");
    $("#daycheck").prop({checked: false});
    ClearSubModal();
    DisableModalOdd(false);
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
              SetPeriodActive(1, item.period);
              DisableModalOdd(true);
            } else if (item.pair_type == "парна") {
              $("#daycheck").prop({checked: false});
              $("#msub2").val(item.subject);
              $("#mteach2").val(item.teacher);
              $("#maud2").val(item.audience);
              SetPeriodActive(2, item.period);
              DisableModalOdd(false);
            } else if (item.pair_type == "непарна") {
              $("#daycheck").prop({checked: false});
              $("#msub1").val(item.subject);
              $("#mteach1").val(item.teacher);
              $("#maud1").val(item.audience);
              SetPeriodActive(1, item.period);
              DisableModalOdd(false);
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
    ShowMessage("error", "Спочатку виберіть групу");
  }; 
}

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


///////////  FUNCTIONS SECTION //////////////
$(function() {
  $("#sendsubject").click(function() { // Провірка вікна дод. заняття на заповненість
    errors = false;
    if ($("#daycheck").prop("checked")) {
      if ($("#msub1").val() !== "") {
        if ($("#mteach1").val() == "" || $("#maud1").val() == "") {
          errors = true;
        };
      }; 
    } else {
      if ($("#msub1").val() !== "") {
        if ($("#mteach1").val() == "" || $("#maud1").val() == "") {
          errors = true;
        };
      };
      if ($("#msub2").val() !== "") {
        if ($("#mteach2").val() == "" || $("#maud2").val() == "") {
          errors = true;
        };
      };
    };
    if (errors !== true) {
      SendSubjectData("true");
    } else {
      ShowModalMessage("#subject_add_modal", "Заповніть всі поля");
    };
  });
});

$(function() {
  $("#adv_send_sub").click(function() {
    SendSubjectData("false");
  });
});

$(function() {
  $("#send_stream_subject").click(function() { // Провірка вікна дод. поток. заняття на заповненість
    errors = false;
    if ($("#stream_groups").val() == "" || $("#stream_pair").val() == "" || $("#stream_day").val() == "") {
      errors = true;
    };
    if ($("#streamdaycheck").prop("checked")) {
      if ($("#ssub1").val() !== "") {
        if ($("#steach1").val() == "" || $("#saud1").val() == "") {
          errors = true;
        };
      }; 
    } else {
      if ($("#ssub1").val() !== "") {
        if ($("#steach1").val() == "" || $("#saud1").val() == "") {
          errors = true;
        };
      };
      if ($("#ssub2").val() !== "") {
        if ($("#steach2").val() == "" || $("#saud2").val() == "") {
          errors = true;
        };
      };
    };
    if (errors !== true) {
      SendStreamSubjectData();
    } else {
      ShowModalMessage("#add_stream_modal", "Заповніть всі поля");
    };
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

function ShowModalMessage(modal, message) {  //Повідомлення в модальному вікні
  $(modal+" .modal-footer .modal_message p:first-child b").text(message);
  $(modal+" .modal-footer .modal_message").show("fast").delay(1700);
  $(modal+" .modal-footer .modal_message").hide("fast");
};

function ShowModalMessageAdv(modal, message) { //Відкриття діалогу в модальному вікні
  DisableModalOdd(true);
  DisableModalEven(true);
  $(modal+" .modal-footer .modal_message_adv p:first-child b").text(message);
  $(modal+" .modal-footer .modal_message_adv").slideDown("fast");
  $(modal+" .modal-footer .modal_buttons").slideUp("fast");
};

function HideModalMessageAdv(modal) {
  if ($("#daycheck").is(':checked')) {
      DisableModalEven(false);
    } else {
      DisableModalOdd(false);
      DisableModalEven(false);
    };
  $(modal+" .modal_container").prop({disabled: false});
  $(modal+" .modal-footer .modal_message_adv").slideUp("fast");
  $(modal+" .modal-footer .modal_buttons").slideDown("fast");
};

function ClearSubModal() {  //Очистка модального вікна
  HideModalMessageAdv("#subject_add_modal");
  $("#subject_add_modal .modal_container div div input").val('');
  $("#subject_add_modal .modal_container div .btn-group button").removeClass("active");
  $("#subject_add_modal .modal_container div .btn-group button:first-child").addClass("active");
};

function SetPeriodActive(evenodd, period) { //Установка кнопки періоду
  if (evenodd == 1) {
    $(".modal_cont1 .btn-group button").removeClass("active");
    $(".modal_cont1 .btn-group button:nth-child("+period+")").addClass("active");
  } else if (evenodd == 2) {
    $(".modal_cont2 .btn-group button").removeClass("active");
    $(".modal_cont2 .btn-group button:nth-child("+period+")").addClass("active");
  };
};

function DisableModalEven(property) {
  $("#msub1, #ssub1").prop({disabled: property});
  $("#mteach1, #steach1").prop({disabled: property});
  $("#maud1, #saud1").prop({disabled: property});
  $(".modal_container .modal_cont1 div button").prop({disabled: property});
  if (property) {
    $(".modal_container .modal_cont1 div label").addClass("label_disabled");
  } else{
    $(".modal_container .modal_cont1 div label").removeClass("label_disabled");
  };
};

function DisableModalOdd(property) {  //Блокування правої частини діалогового вікна
  $("#msub2, #ssub2").prop({disabled: property});
  $("#mteach2, #steach2").prop({disabled: property});
  $("#maud2, #saud2").prop({disabled: property});
  $(".modal_container .modal_cont2 div button").prop({disabled: property});
  if (property) {
    $(".modal_container .modal_cont2 div label").addClass("label_disabled");
  } else{
    $(".modal_container .modal_cont2 div label").removeClass("label_disabled");
  };
};


//////// DOCUMENT READY ///////////
$(document).ready(function() {

  $("#tab1 table tbody tr").dblclick(function() { //Виклик вікна додавання заняття
    SingleModalWindow($(this));
  });

  $(document).on('click', ".mov_elem div button:first-child", function() {
    SingleModalWindow($(this).parents("tr"));
  });

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
    GetSubjects(group.attr("value"), true)
  });

  $("#daycheck").click(function() {  // Зміна стану діалогового вікна заняття
    if ($("#daycheck").is(':checked')) {
      DisableModalOdd(true);
    } else {
      DisableModalOdd(false);
    };
  });

  $("#streamdaycheck").click(function() {  // Зміна стану діалогового вікна потокового заняття
    if ($("#streamdaycheck").is(':checked')) {
      DisableModalOdd(true);
    } else {
      DisableModalOdd(false);
    };
  });

  $("#hide_adv_dialog").click(function() {
    HideModalMessageAdv("#subject_add_modal");
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


  ////////// HTML5 DRAG AND DROP ///////////
  $(".subject_content").on("dragstart", function(e) {
    e.originalEvent.dataTransfer.setData("Text", $(this).parent().attr("id"));
    $(this).addClass("drag_start");
    $("td:last-child .pop_elem").not($(this).children()).show();
  });

  $(document).on('dragover', ".subject_content > div > div > div", function(e) {
    e.preventDefault();
    return false;
  });

  $(document).on('dragenter', ".subject_content > div > div > div", function(e) {
    $(this).addClass("drag_enter");
    return false;
  });
 
  $(document).on('dragleave', ".subject_content > div > div > div", function(e) {
    var related = e.relatedTarget,
    inside = false;
    if (related !== this) {
      if (related) {
        inside = jQuery.contains(this, related);
      }
      if (!inside) {
        $(this).removeClass("drag_enter");
      }
    }
    return false;
  });

  $(document).on('drop', ".subject_content > div > div > div", function(e) {
    e.preventDefault();
    if (e.stopPropagation) {
      e.stopPropagation();
    };
    $.ajax({
      url: "/dnd",
      dataType: "jsonp",
      data: {
        group: $("#group").val(),
        from: e.originalEvent.dataTransfer.getData("Text"),
        to: $(this).parents("tr").attr("id"),
        action: $(this).attr("value")
      },
      beforeSend: function() {
        $("#load_animation").show("fast");
      },
      success: function(data) {
        if ($("#group").val() !== "") {
          GetSubjects($("#group").val(), false)
        };
      },
      error: function() {
        ShowMessage("error", "Виникла помилка")
        $("#load_animation").hide("fast");
      }
    });
    $(this).removeClass("drag_enter");
    return false;
  });

  $("tr td:last-child").on('dragend', function (e) {
    $("td:last-child .pop_elem").hide();
    $("td:last-child").removeClass("drag_enter");
    $(this).removeClass("drag_start");
  });


  /////// Additional control elements  //////
  $(".subject_content").on("mouseout", function(e) {
    $(this).children(".mov_elem").hide();
  });

  $(".subject_content").on("mouseover", function(e) {
    $(this).children(".mov_elem").show();
  });

});


