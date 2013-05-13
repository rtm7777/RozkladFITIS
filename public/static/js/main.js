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
  $("#msub1, #msub2, #ssub1, #ssub2, #sub_task").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/ac",
        dataType: "jsonp",
        data: {str: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.name+' - '+item.type;
          }));
        }
      });
    }
  });
});

$(function() {  // Ajax для автозаповнення викладача
  $("#mteach1, #mteach2, #steach1, #steach2, #teach_task").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/tch",
        dataType: "jsonp",
        data: {str: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.lastname+' '+item.firstname+' '+item.middlename;
          }));
        }
      });
    }
  });
});

$(function() {  // Ajax для автозаповнення аудиторії
  $("#maud1, #saud1, #maud2, #saud2, #aud_task").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/au",
        dataType: "jsonp",
        data: {str: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.number;
          }));
        }
      });
    }
  });
});

$(function() {  // Ajax для автозаповнення групи
  $("#group_task").typeahead({
    source: function(query, process) {
      $.ajax({
        url: "/gr",
        dataType: "jsonp",
        data: {str: query},
        success: function(data) {
          process($.map(data.sources, function(item) {
            return item.name;
          }));
        }
      });
    }
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
        GetConformity($("#group").val());
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
        GetConformity($("#group").val());
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
      $("#tab1 tr td:last-child").removeClass("single_admin").html('<p class="null"></p><hr><p class="null"></p>'+dnd_html);
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
};

function GetAudEmployment(house, day) {
  $.ajax({
    url: "/getaudemp",
    dataType: "jsonp",
    data: {
      house: house,
      day: day
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $("#tab2 table tbody").html(" ");
      $.map(data.audiences, function(item) {
        $("#tab2 table tbody").append("<tr class=" + item.number + "><th>" + item.number + "</th><th class='I1'><p></p></th><th class='I2'><p></p></th><th class='II1'><p></p></th><th class='II2'><p></p></th><th class='III1'><p></p></th><th class='III2'><p></p></th><th class='IV1'><p></p></th><th class='IV2'><p></p></th><th class='V1'><p></p></th><th class='V2'><p></p></th><th class='VI1'><p></p></th><th class='VI2'><p></p></th></tr>");
        $.map(item.pairs,  function(i) {
          var period_bool = false;
          var type = 0;
          var periods = "";
          var periods_true = false;
          if (i.type == "непарна") {
            type = 1
          } else if (i.type == "парна") {
            type = 2
          } else if (i.type == "кожен") {
            period_bool = true;
          };
          if (i.period == "1") {
            var periods_true = true;
          } else {
            if (periods_true == false) {
              periods += i.period + ","
            };
          };
          if (periods_true) {
            if (period_bool) {
              $("#tab2 table tbody ." + item.number + " ." + i.num + "1").addClass("bysy_cell");
              $("#tab2 table tbody ." + item.number + " ." + i.num + "2").addClass("bysy_cell");
            } else {
              $("#tab2 table tbody ." + item.number + " ." + i.num + type).addClass("bysy_cell");
            };
          } else {
            if (period_bool) {
              $("#tab2 table tbody ." + item.number + " ." + i.num + "1").addClass("bysy_cell");
              $("#tab2 table tbody ." + item.number + " ." + i.num + "1 p").text(periods.slice(0,-1));
              $("#tab2 table tbody ." + item.number + " ." + i.num + "2").addClass("bysy_cell");
              $("#tab2 table tbody ." + item.number + " ." + i.num + "2 p").text(periods.slice(0,-1));
            } else {
              $("#tab2 table tbody ." + item.number + " ." + i.num + type).addClass("bysy_cell");
              $("#tab2 table tbody ." + item.number + " ." + i.num + type + " p").text(periods.slice(0,-1));
            };
          };
          
        });
      });
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function GetTeachEmployment(day) {
  $.ajax({
    url: "/getteachemp",
    dataType: "jsonp",
    data: {
      day: day
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $("#tab3 table tbody").html(" ");
      $.map(data.teachers, function(item) {
        $("#tab3 table tbody").append("<tr class=" + item.name + "><th>" + item.name + "</th><th class='I1'><p></p></th><th class='I2'><p></p></th><th class='II1'><p></p></th><th class='II3'><p></p></th><th class='III1'><p></p></th><th class='III2'><p></p></th><th class='IV1'><p></p></th><th class='IV2'><p></p></th><th class='V1'><p></p></th><th class='V2'><p></p></th><th class='VI1'><p></p></th><th class='VI2'><p></p></th></tr>");
        $.map(item.pairs,  function(i) {
          var period_bool = false;
          var periods = "";
          var type = 0;
          if (i.type == "непарна") {
            type = 1
          } else if (i.type == "парна") {
            type = 2
          }else if (i.type == "кожен") {
            period_bool = true;
          };
          if (period_bool) {
            $("#tab3 table tbody ." + item.name + " ." + i.num + "1").addClass("bysy_cell");
            $("#tab3 table tbody ." + item.name + " ." + i.num + "2").addClass("bysy_cell");
          } else {
            $("#tab3 table tbody ." + item.name + " ." + i.num + type).addClass("bysy_cell");
          };
        });
      });
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function GetDepTasks(dep) {
  $.ajax({
    url: "/getdeptasks",
    dataType: "jsonp",
    data: {
      dep: dep
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $("#tab4 table tbody").html(" ");
      $.map(data.tasks, function(item) {
        $("#tab4 table tbody").append("<tr><td><p>"+item.subject+"</p></td><td><p>"+item.group+"</p></td><td><p>"+item.time+"</p></td><td><p>"+item.teacher+"</p></td><td><p>"+item.audience+"</p></td></tr>");
      });
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function GetConformity(group) {
  $.ajax({
    url: "/getconformity",
    dataType: "jsonp",
    data: {
      group: group
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $("#opt_rozklad div").html("<p><b>Відповідність завданню:</b></p>");
      $.map(data.sources, function(item) {
        $("#opt_rozklad>div").append('<p>'+item.subject+'</p><div class="progress '+item.type+'"><div class="bar" style="width: '+item.value+'%"></div></div>')
        });
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function AddDepTask() {
  $.ajax({
    url: "/adddeptask",
    dataType: "jsonp",
    data: {
      department: $("#tab4_dep").val(),
      subject: $("#sub_task").val(),
      group: $("#group_task").val(),
      teacher: $("#teach_task").val(),
      audience: $("#aud_task").val(),
      duration: $("#task-btn-group1 button.active").val()
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      if (data.errors) {
        ShowModalMessage("#add_task_modal", "деякі поля введено некоректно");
        $("#load_animation").hide("fast");
      } else {
        GetDepTasks($("#tab4_dep").val());
        if ($("#group").val() !== "") {
          GetConformity($("#group").val());
        };
        $("#add_task_modal").modal('hide');
        $("#load_animation").hide("fast");
      };
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function DeleteSubject(pair, group) {
  $.ajax({
    url: "/delsub",
    dataType: "jsonp",
    data: {
      group: group,
      pair: pair
    },
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function() {
      GetSubjects($("#group").val(), false);
      GetConformity($("#group").val());
      $("#dialog_modal").modal("hide");
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function Simulate() {
  $.ajax({
    url: "/simulate",
    dataType: "jsonp",
    data: {},
    beforeSend: function() {
      $("#tab5 pre").html("Консоль\nРозпочалось симулювання розкладу\n");
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $("#tab5 pre").append(data.status);
      $("#tab5 pre").append(data.dat);
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function GetGroupsofYear(year) {
  $.ajax({
    url: "/getgroups",
    dataType: "jsonp",
    data: {year: year},
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      $(".rgraph_buttons .nav").html(" ");
      $.map(data.data, function(item) {
        $(".rgraph_buttons .nav").append('<li><a href="#" value="'+item+'">'+item+'</a></li>');
      });
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
};

function GetGroupLoading(group) {
  grloaddata = [];
  $.ajax({
    url: "/getgrouploading",
    dataType: "jsonp",
    data: {group: group},
    async: false,
    beforeSend: function() {
      $("#load_animation").show("fast");
    },
    success: function(data) {
      grloaddata = data.data;
      $("#load_animation").hide("fast");
    },
    error: function() {
      ShowMessage("error", "Виникла помилка");
      $("#load_animation").hide("fast");
    }
  });
  return grloaddata;
};

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

$(function() {
  $("#add_dep_task").click(function(){
  if ($("#sub_task").val() == "" || $("#group_task").val() == "" || $("#teach_task").val() == "") {
    ShowModalMessage("#add_task_modal", "Заповніть всі поля");
  } else {
    AddDepTask();
  };
  });
});

$(function() {
  $("#dialog_yes").click(function(){
    DeleteSubject($("#dm_param").val(), $("#group").val());
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
  $(".modal_container .modal_cont1 div button[value='2']").prop({disabled: true});
  $(".modal_container .modal_cont1 div button[value='4']").prop({disabled: true});
  $(".modal_container .modal_cont2 div button[value='3']").prop({disabled: true});
  $(".modal_container .modal_cont2 div button[value='5']").prop({disabled: true});
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

function DisableModalEven(property) {  //Блокування лівої частини діалогового вікна
  $("#msub1, #ssub1").prop({disabled: property});
  $("#mteach1, #steach1").prop({disabled: property});
  $("#maud1, #saud1").prop({disabled: property});
  $(".modal_container .modal_cont1 div button[value^='#']").prop({disabled: property});
  $(".modal_container .modal_cont1 div button[value='1']").prop({disabled: property});
  $(".modal_container .modal_cont1 div button[value='3']").prop({disabled: property});
  $(".modal_container .modal_cont1 div button[value='5']").prop({disabled: property});
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
  $(".modal_container .modal_cont2 div button[value^='#']").prop({disabled: property});
  $(".modal_container .modal_cont2 div button[value='1']").prop({disabled: property});
  $(".modal_container .modal_cont2 div button[value='2']").prop({disabled: property});
  $(".modal_container .modal_cont2 div button[value='4']").prop({disabled: property});
  if (property) {
    $(".modal_container .modal_cont2 div label").addClass("label_disabled");
  } else{
    $(".modal_container .modal_cont2 div label").removeClass("label_disabled");
  };
};


function ShowGraph(data) {
  var myLine = new RGraph.Line('cvs',data);
  RGraph.ObjectRegistry.Clear("cvs");
  myLine.Set('chart.labels', ['Понеділок','Вівторок','Середа','Четвер',"П'ятниця"]);
  myLine.Set('chart.gutter.left', 40);
  myLine.Set('chart.gutter.right', 15);
  myLine.Set('chart.gutter.bottom', 20);
  myLine.Set('chart.colors', ['#08c']);
  myLine.Set('chart.units.post', ' год.');
  myLine.Set('chart.linewidth', 5);
  myLine.Set('chart.hmargin', 35);
  myLine.Set('numyticks', 3);
  myLine.Set('chart.ylabels', true);
  myLine.Set('chart.ylabels.count', 6);
  myLine.Set('chart.ymax', 6);
  myLine.Set('chart.ymin', 0);
  myLine.Set('chart.text.color', '#333');
  myLine.Set('chart.text.font', 'Arial');
  myLine.Set('chart.background.grid.autofit', true);
  myLine.Set('chart.background.grid.autofit.numvlines', 5);
  myLine.Set('chart.background.grid.autofit.numhlines', 12);
  myLine.Set('chart.shadow', true);
  myLine.Set('chart.shadow.color', 'rgba(20,20,20,0.3)');
  myLine.Set('chart.shadow.blur',  10);
  myLine.Set('chart.shadow.offsetx', 0);
  myLine.Set('chart.shadow.offsety', 0);
  myLine.Set('chart.background.grid.vlines', true);
  myLine.Set('chart.background.grid.border', true);
  myLine.Set('chart.noxaxis', true);
  myLine.Set('chart.title', 'Навантаження групи - ....');
  myLine.Set('chart.axis.color', '#666');
  myLine.Set('chart.text.color', '#666');
  myLine.Draw();
};


//////// DOCUMENT READY ///////////
$(document).ready(function() {

  $("#tab1 table tbody tr").dblclick(function() { //Виклик вікна додавання заняття
    SingleModalWindow($(this));
  });

  $(document).on('click', ".mov_elem div button:first-child", function() {
    SingleModalWindow($(this).parents("tr"));
  });

  $(document).on('click', ".mov_elem div button:last-child", function() {
    pair = $(this).parents("tr").attr("id");
    $("#dm_param").val(pair);
    $("#dialog_modal").modal('show');
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
    GetSubjects(group.attr("value"), true);
    GetConformity(group.attr("value"));
  });

  $("#house_id li a").click(function() {  // Відображення зайнятості аудиторій - корпус
    var house = $(this);
    $("#tab2_house").prop({value: house.attr("value")});
    $("#house_num").text(house.attr("value") + " - корпус");
    GetAudEmployment($("#tab2_house").val(), $("#tab2 div button.active").val());
  });

  $("#tab2 div button").click(function() {  // Відображення зайнятості аудиторій - день
    var day = $(this);
    if ($("#tab2_house").val() !== "") {
      GetAudEmployment($("#tab2_house").val(), day.attr("value"));
    } else{
      ShowMessage("error", "Виберіть корпус");
    };
  });

  $("#dep_id li a").click(function() {  // Відображення завдань кафедри
    var dep = $(this);
    $("#tab4_dep").prop({value: dep.attr("value")});
    $("#dep_num").text("кафедра - " + dep.attr("value"));
    GetDepTasks($("#tab4_dep").val())
  });

  $("a[href='#tab2']").click(function() { // Оновлення при виборі вкладки
    if ($("#tab2_house").val() !== "") {
      GetAudEmployment($("#tab2_house").val(), $("#tab2 div button.active").val());
    };
  });

  $("#tab3 div button").click(function() {  // Відображення зайнятості викладачів - день
    var day = $(this);
    GetTeachEmployment(day.attr("value"));
  });

  $("a[href='#tab3']").click(function() {  // Оновлення при виборі вкладки
    GetTeachEmployment($("#tab3 div button.active").val());
  });

  $("a[href='#simulate']").click(function() {  // симуляція навчання
    Simulate();
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
    $("#rozklad_span3>div").slideUp("slow");
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

  $(".rgraph_buttons .dropdown-menu li a").click(function() {
    $(".rgraph_buttons .btn-group>a").html($(this).text()+" <span class='caret'></span>");
    GetGroupsofYear($(this).attr("value"));
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

  /////////// Canvas + Rgraph //////////////
  $("a[href='#rgraphgr']").click(function() {  // графік
    $("#graph_modal").modal('show');
  });

  $(document).on('click', "#graph_modal .nav>li>a", function() {
    ShowGraph(GetGroupLoading($(this).attr("value")));
  });

});


