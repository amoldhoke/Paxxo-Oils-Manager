/* -------------------------------
# MESSAGE (PULSE)
------------------------------- */

// 1) Character remaining character
$(document).ready(function() {
    var start = 0;
    var limit = 1000;

    $("#message").keyup(function() {
        start = this.value.length
        if(start > limit) {
            return false;
        }
        else if (start == 1000) {
            $("#remaining").html("Character remaining: " + (limit - start)).css('color', 'red');
            swal("Opsss !", "Characters limit exceeded !", "info");
        }
        else if (start > 984) {
            $("#remaining").html("Character remaining: " + (limit - start)).css('color', 'red');          
        }
        else if (start < 1000) {
            $("#remaining").html("Character remaining: " + (limit - start)).css('color', 'black'); 
        }
        else {
            $("#remaining").html("Character remaining: " + (limit)).css('color', 'black');
        }
    })
})

// 2) Inputmask (PHONE)
$(document).ready(function() {
    $(".phone").inputmask("99999-99999", {"onincomplete": function() {
        swal("Opsss !", "Incomplete phone. Please review !", "info");
        $(".phone").val("");
        return false;
    }})
})

// 3) Script to get the TIME running at realtime
setInterval(function() {
    var date = new Date();
    $('#clock, #mini-clock').html(
        (date.getHours() < 10 ? '0' : '') + date.getHours() + ":" +
        (date.getMinutes() < 10 ? '0' : '') + date.getMinutes() + ":" +
        (date.getSeconds() < 10 ? '0' : '') + date.getSeconds()
    );
}, 500)

// 4) Script to update the page always at (0:00)
function autoRefresh(hours, minutes, seconds) {
    var now = new Date(), then = new Date();
    then.setHours(hours, minutes, seconds, 0);
    if(then.getTime() < now.getTime()) {
        then.setDate(now.getDate() + 1);
    }
    var timeout = (then.getTime() - now.getTime());
    setTimeout(function() {
        window.location.reload(true);
    }, timeout);
}
autoRefresh(0, 0, 0)

// 5) Script to advice the users about logout at 5 min (after 25min)
setTimeout(function() {
    var notice = document.querySelector('#warning');
    if(notice) {
        notice.click();
    }
}, 25 * 60000);  // 25 min

// 6) Script to auto logout (after 5 min passed)
setTimeout(function() {
    var action = document.querySelector('#info');
    if(action) {
        action.click();
    }
}, 30 * 60000);  // 30 min

// 7)  Function to pulse the text (login page)
(function pulse() {
    $('.text-pulse').fadeOut(1000).fadeIn(1000, pulse);
})();

// 8) Function to hide/show password
function myFunction() {
    var p = document.getElementById("password");
    if (p.type == "password") {
        p.type = "text";
    }
    else {
        p.type = "password"
    }
}

// 9) Script to close offcanvas when the button is clicked
jQuery("#offcanvasRight, .offcanvas-body a").click(function() {
    console.log($(this).attr("href"));
    jQuery('.offcanvas').offcanvas('hide');
});

// 10) Script to accept 2mb (upload files)
var upload = document.getElementById('file');
    upload.onchange = function() {
        if (this.files[0].size > 2 * 1048576) {
            swal("Attention !", "Maximum allowed size is 2mb.", "info");
            this.value = "";
        };
    };

// 11) If no message, hide all content
$(document).ready(function() {
    var verify = $('#chk_td').length;
        if (verify == 0) {
            $(".hide").css('display', 'none');
            $("#msg").text("No message found");
            $("#refresh").html('<i class="fas fa-sync-alt fa-3x">')
        }
})

// 12) Ajax Back Spinner
jQuery(function($) {
    $(document).ajaxSend(function() {
        $("#bg-spinner").fadeIn(500);
    });
    
    $(".send-email").click(function() {
        $.ajax({
        type: 'GET',
        success:function (data) {
            var d = $.parseJSON(data);
            alert(d.Test);
        }
        }).done(function() {
        setTimeout(function() {
            $("#bg-spinner").fadeOut(500);
        }, 700);
        });
    });
});
// Close modal (after 'send button is clicked')
$(".send-email").click(function() {
    var msg = $("#email-msg").val();
    var subject = $("#email-subject").val();

    if ((msg != "") && (subject != "")) {
        $(".close-modal").modal("hide");
    }
})






