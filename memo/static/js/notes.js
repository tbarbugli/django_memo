function save_note(){
    var form = $(this).parent().parent().parent().find("form");
    if (form.length != 1) {
        var form = $(this).parent().parent().parent().parent().find("form");
    } 
    form.find(".text").val(form.find(".editable").text());
    $.ajax({
        type: 'POST',
        url: form.attr("action"),
        data: form.serialize()
      });
}

function init_notes()
{ 
  $(".note").draggable({
    cancel: ".bottom, section",    
    stack: "#notes div", 
    containment: "#notes",
    create: function() {if($(this).hasClass("shake")){$(this).effect("bounce", "fast");}},
    stop : function (event, ui) { 
      var form = $(this).children().children("form");
      form.find(".text").val($(this).find(".editable").text()); 
      form.find(".top").val(ui.position.top);
      form.find(".left").val(ui.position.left);  
      $.ajax({
        type: 'POST',
        url: form.attr("action"),
        data: form.serialize()
      });    
    }
  });
  $("input, select").change(save_note); 
  $("section").blur(save_note); 
  $("a.remove").unbind('click');                     
  $("a.remove").click(function(){       
    $.ajax({
      type: 'POST',
      url: $(this).attr("href"),
      data: {}
    });
    $(this).parent().parent().parent().hide("puff");
    return false;
  }); 
}    

function init_follow_btn(){   
    $("a.follow").unbind('click');
    $("a.follow").click(function(){       
      $.ajax({
        type: 'POST',
        url: $(this).attr("href"),
        data: {}
      });
      $(this).hide("puff");
      return false;
    });
}
function append_note(data){  
  var note = $(data);
  note.css("top", "100");
  note.css("z-index", "999");
  note.css("left", "50");  
  note.addClass("shake");
  $("#notes").append(note);    
  init_notes();       
}
