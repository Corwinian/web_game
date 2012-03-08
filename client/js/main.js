var sections; // descriptions of toplevel sections (which behave like pages)
window.onhashchange = innerShowSection;

function sendNonAuthorizedRequest(data, handler, error_handler)
{
  $.getJSON('/ajax',  { data: JSON.stringify(data) }, function (json)  
  //$.post('/', { data: JSON.stringify(data) }, function (json)  
  {
    json.result== 'ok' ? handler(json) : (error_handler || alert)(json.result);
//    json.result== 'ok' ? handler(json) : (error_handler || alert)(json.message, json.result);
  });
}

function sendRequest(data, handler, error_handler)
{
  sendNonAuthorizedRequest($.extend(data, { sid: sessionStorage.sid }),
    handler, error_handler);
}

function showCurrentUser(prefix)
{
  $("#current-user").html(prefix + sessionStorage.username);
}

function showSection(name)
{
  if (getCurrentSectionName() == name)
  {
    innerShowSection();
    return;
  }
  window.location.hash = name;
}

function getCurrentSectionName()
{
  return window.location.hash.substr(1); // remove # symbol
}

function innerShowSection()
{
  var section = getCurrentSectionName();
  if (!section || !(section in sections))
  {
    window.location.hash = "registration";
    return;
  }
  sections[section].show();
}

Section = $.inherit(
  {
    __constructor: function(name)
    {
      this.name = name
    },
    show: function()
    {
      $('#content > *, #menu, #menu > li').hide();
      $('#' + this.name).show();
    }
  }
);

SectionWithNavigation = $.inherit(
  Section,
  {
    show: function ()
    {
      this.__base();
      $('nav > p').removeClass('nav-current');
      $('#nav-' + this.name).addClass('nav-current');

      showCurrentUser('<i>Welcome</i>, ');

      $('#menu, #menu li[id!="leave-game"], nav, #nav-vertical-line').show();
    }
  }
);


function describeSections()
{
  sections = {
    'registration': new Section('registration'),
  }
}

function submitForm(form, handler, grabber, command)
{
  function formError(form, text)
  {
    $('.error', form).remove();
    form.prepend(
      $('<p/>', {class: 'error ui-corner-all'})
      .append($('<img/>', { src: '/images/error.png' }))
      .append(text)
    );
  }

  function grabForm(form)
  {
    var obj = {};
    $("input[type!='submit'], textarea", form).each(function(i, v)
    {
      obj[$(v).attr('name')] = $(v).hasClass('int-value') ? parseInt($(v).val()) : $(v).val();
    });
    $("select", form).each(function(i, v)
    {
      obj[$(v).attr('name')] = $(':selected', v).text();
    });
    return obj;
  }

  var data = grabber ? grabber(form): grabForm(form);
  var commands = {
    'registration': function() { return { action: 'register' }; },
    //'registration': function() { return { action: 'login' }; },
  }
  command = command || commands[form.attr('name')]();
  if (command.action == 'register' || command.action == 'login')
    requestFunc = sendNonAuthorizedRequest;
  else
    requestFunc = sendRequest;

  requestFunc(
    $.extend(data, command),
    function (json) { handler(json, data); clearForm(form); },
    function (message) { formError(form, message); }
  );

  return false; // ban POST requests
}

function initBinds()
{
  // Registration
  $('form[name="registration"]').submit(function()
  {
    return submitForm($(this), function(json, data)
      {
        if(sessionStorage.length && sessionStorage.username == data.username &&
          inGame())
        {
          showSection('lobby');
          return;
        }
        sessionStorage.clear();
        sessionStorage.sid = json.sid;
        sessionStorage.username = data.username;
        showSection('active-games');
      }
    );
  });
}

function clearForm(form)
{
  $('.error', form).remove();
  $('input[type!="submit"]', form).val('');
}

$(document).ready(function()
{
  //initNavigation();
  //initHorzMenu();
  initBinds();

  $('input:submit, a.button').button();
  //$('#auto-turn').button();
  $('input:text').addClass('ui-widget');

  describeSections();
  showSection(getCurrentSectionName() || "registration");
});