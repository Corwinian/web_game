var sections; // descriptions of toplevel sections (which behave like pages)
window.onhashchange = innerShowSection;

function sendNonAuthorizedRequest(data, handler, error_handler)
{
	$.getJSON('/ajax',	{ data: JSON.stringify(data) }, function (json)	
	{
		//пока так потом сделать нормально, что в хэндлер можно было передать сообщение
		json.result== 'ok' ? handler(json, data.action == "register" ? "regitation ok" : '' )
			: (error_handler || alert)(false, json.result);
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
		window.location.hash = "autorisation";
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
			$('#content > *, #menu > li').hide();
			$('#' + this.name).show();

			non_auth = (this.name == "registration" || this.name == "autorisation");

			if (this.name == "registration" || this.name == "autorisation")
			{
				$('#menu li[id="reg_window"]').show();
			}
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

			$('#menu, #menu li[id!="reg_window"], #nav-vertical-line, nav').show();
		}
	}
);

LobbySection = $.inherit(
 SectionWithNavigation,
  {
    __constructor: function()
    {
      this.__base('lobby');
    },
    show: function() {
      this.__base();
      initLobby();
    }
  }
);

function initLobby()
{
  if(!sessionStorage.length)
  {
    showSection('autorisation');
  }

  getLobbyState();
}

function getLobbyState()
{
  if(getCurrentSectionName() != 'lobby')
  {
    return;
  }

  var command = { action: 'getMessages', since:0 };
  if (sections.lobby.last_id)
  {
    $.extend(command, { since: sections.lobby.last_id });
  }

  sendNonAuthorizedRequest(command, function (json)
  {
    if (json.messages.length)
    {
      sections.lobby.last_id = json.messages[json.messages.length-1].id;
      $.each(json.messages, function(i, entry)
      {
        $('#chat-window').append($('<div/>')
          .append($('<p/>', { class: 'chat-header' })
            .append(entry.time)
            .append($('<br/>'))
            .append($('<p/>', { class: 'chat-username', text: entry.username })))
          .append($('<p/>', { class: 'chat-message', text: entry.text}))
        );
      });
    }
	setTimeout(getLobbyState, 3000);
  });
}

function updateSelect($select, command, array, attr)
{
	sendNonAuthorizedRequest({ action: command }, function(json) {
    $select.empty();
    $.each(json[array], function(i, option) {
      $select.append(new Option(option[attr], i));
    });
  });
}

function initCreateGame(){
	updateSelect($('#creation-map'), "getMapList", 'maps', 'mapName');
}

CreateGameSection = $.inherit(
  SectionWithNavigation,
  {
    __constructor: function()
    {
      this.__base('create-game');
    },
    show: function()
    {
      this.__base();
      initCreateGame();
    }
  }
);

function describeSections()
{
	sections = {
		'registration': new Section('registration'),
		'autorisation': new Section('autorisation'),
		'lobby': new LobbySection(),
		'create-game': new CreateGameSection(),
	}
}

function initHorzMenu()
{
	$("#sign-out").click(function()
	{
		sendRequest({ action :'logout' }, function (json)
		{
			sessionStorage.clear();
			showSection('autorisation');
		});
	});

	$("#reg_window").click(function() {	showSection('registration');});
}

function submitForm(form, handler, grabber, command)
{
	function formError(form, text)
	{
		$('.error', form).remove();
		$('.good', form).remove();
		form.prepend(
			$('<p/>', {class: 'error ui-corner-all'})
			.append($('<img/>', { src: '/images/error.png' }))
			.append(text)
		);
	}

	function formGood(form, text)
	{
		$('.error', form).remove();
		$('.good', form).remove();
		form.prepend(
			$('<p/>', {class: 'good ui-corner-all'})
			.append($('<img/>', { src: '/images/good.png' }))
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
		'autorisation': function() { return { action: 'login' }; },
		'send-message': function() { return { action: 'sendMessage' }; },
	//	'send-message': function() { return { action: 'sendMessage' }; },
	}
	command = command || commands[form.attr('name')]();
	if (command.action == 'register' || command.action == 'login')
		requestFunc = sendNonAuthorizedRequest;
	else
		requestFunc = sendRequest;

	requestFunc(
		$.extend(data, command),
		function (json, message) 
		{
			handler(json, data); clearForm(form); 
			if (message != ''){	formGood($('form[name="autorisation"]'),message);}
		},
		function (message) { formError(form, message); }
	);

	return false; // ban POST requests
}
function initNavigation()
{
  var items = $("nav > p");

  $(".main-section").hide();
  items.click(function()
  {
    var item = $(this);

    if (item.hasClass("nav-current")) return;
    $.each(items, function() { $(this).removeClass("nav-current"); });
    item.addClass("nav-current");

    showSection(item.attr('id').substring(4)); // strip 'nav-' prefix
  });

  // add animation
  var pad_out = 25;
  var pad_in = 15;
  items.each(function()
  {
    $(this).hover(function()
    {
      $(this).animate({ paddingLeft: pad_out }, 150);
    },
    function()
    {
      $(this).animate({ paddingLeft: pad_in }, 150);
    });
  });
}


function initBinds()
{
	// Registration
	$('form[name="registration"]').submit(function()
	{
		return submitForm($(this), function(json, data)
			{
				showSection('autorisation');
			}
		);
	});
	$('form[name="autorisation"]').submit(function()
	{
		return submitForm($(this), function(json, data)
			{
				sessionStorage.clear();
				sessionStorage.sid = json.sid;
				sessionStorage.username = data.username;
				showSection('lobby');
				return;
			}
		);
	});
	//Lobby
	$('form[name="send-message"]').submit(function()
	{
		var form = $(this);
		var message = $('#send-message-text', form);
		if (message.length != 0)
		{
			submitForm(form, function() {message.val('');});
			getLobbyState();
			showSection('lobby');
			return;
		}
	});
	//CreateGame
	$('form[name="create-game"]').submit(function()
	{
		var form = $(this);
		var name= $('#creation-title', form);
		if (name.length != 0){

		}
	//	else{
	//		alert("Game Name must be not empty");
	//		return;
	//	}





	});
}

function clearForm(form)
{
	$('.error', form).remove();
	$('input[type!="submit"]', form).val('');
}

$(document).ready(function()
{
	initNavigation();
	initHorzMenu();
	initBinds();

	$('input:submit, a.button').button();
	//$('#auto-turn').button();
	$('input:text').addClass('ui-widget');

	describeSections();
	showSection(getCurrentSectionName() || "autorisation");
});
