/* script.js
 * global javascript code for site
 *
 * Michael Zhu, 2015
 */

// ----------------------------------------------------------------------------
// init function
// ----------------------------------------------------------------------------
$(function () {
  init_flash_messages();
});

// ----------------------------------------------------------------------------
// flash message functions
// ----------------------------------------------------------------------------

// fade out messages one by one after a certain amount of time
function fade_flash_messages() {
  var messages = $('ul.messages li');
  $(messages[0])
    .delay(2000)
    .fadeTo(1000, 0)
    .slideUp(400)
    .queue(function () { $(this).remove(); fade_flash_messages(); });
}

// setup mouseover pause on flash messages
function pause_flash_message_fade() {
  $('ul.messages').hover(
    function () {
      var first_li = $(this).children('li')[0];

      if ($(first_li).css('opacity', 0)) {
        $(first_li).stop(true, false).slideDown(400);
      }

      if (!$(first_li).css('opacity', 1)) {
        $(first_li).fadeTo(400, 1);
      }
    },
    fade_flash_messages
  );
}

function init_flash_messages() {
  pause_flash_message_fade();
  fade_flash_messages();
}

// add a flash message to the flash message area
// msg - contents of message
// msg_type - can be either "success", "error", or "warning"
function add_flash_message(msg, msg_type, enable_fade) {
  enable_fade = typeof enable_fade !== 'undefined' ? enable_fade : false;

  if (msg_type != "success" && msg_type != "error" && msg_type != "warning") {
    msg_type = "warning";
  }

  $('ul.messages').append('<li class="' + msg_type + '">' + msg + '</li>');

  if (enable_fade) {
    init_flash_messages();
  }
}

// modify String prototype with sprintf like equivelant
// (stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format)
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

// ----------------------------------------------------------------------------
// print resume javascript function
// ----------------------------------------------------------------------------
function createPrintFrame() {
  if ($('iframe[name="print_frame"]').length == 0) {
    var print_frame = document.createElement('iframe');
    print_frame.name = "print_frame";
    print_frame.width = "0";
    print_frame.height = "0";
    print_frame.frameBorder = "0";
    print_frame.src = "about:blank";
    document.body.appendChild(print_frame);

    window.frames["print_frame"].document.body.innerHTML = new String($('#resume-css-include')[0].outerHTML);
    window.frames["print_frame"].document.body.innerHTML += new String($('#google-font-include')[0].outerHTML);

    window.frames["print_frame"].document.body.innerHTML += document.getElementById('resume-container').parentNode.innerHTML;
  }
}

// create an iframe if needed and pull out resume contents to be printed
function printResume(event) {
  createPrintFrame();

  window.frames["print_frame"].window.focus();
  window.frames["print_frame"].window.print();

  window.focus(); // bring focus back to main window
  return false;
};

// ----------------------------------------------------------------------------
// toggle dashboard section
// ----------------------------------------------------------------------------
function init_slide_section(header_id, id, start_open) {
  if (!start_open) {
    $('#' + id).hide();
  }

  $('#' + header_id).css({'cursor': 'pointer'});
  $('#' + header_id).addClass('dropdown');

  // on hover, set header to slide to the right a little
  $('#' + header_id).hover(function() {
    $(this).attr('padding-left: 20px;');
  }, function () {
    $(this).attr('padding-left: 0;');
  });

  $('#' + header_id).click(function () {
    $('#' + id).slideToggle();
  });
}