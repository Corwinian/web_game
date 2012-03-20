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
			$('#content > *, #menu, #menu > li').hide();
			$('#' + this.name).show();

			if (this.name == "registration" || this.name == "autorisation")
			{ $('#menu, #menu li[id="reg_window"]').show();}
		}
	}
);

LobbySection = $.inherit(
  Section,
  {
    __constructor: function()
    {
      this.__base('lobby');
    },
    show: function() {
      this.__base();
      $('#menu, #leave-game, #current-user').show();
      showCurrentUser('');
//      initLobby();
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

function initLobby()
{
  if(!sessionStorage.length)
  {
    showSection('registration');
  }
  else if(!inGame())
  {
    showSection('active-games');
  }

  sendRequest({ action: 'getGamesList' }, function (json)
  {
    var currentGame;
    $.each(json.games, function (i, game) {
      if (game.gameName == sessionStorage.gameName)
      {
        currentGame = game;
        return;
      }
    });
    sessionStorage.factionName = currentGame.factionName;

    sessionStorage.max_players = currentGame.playersCount;

  });
  getLobbyState();
}

function getLobbyState()
{
  if(getCurrentSectionName() != 'lobby')
  {
    return;
  }

  var calls = 2;
  function delayedSetTimeout()
  {
    if(!--calls)
    {
      setTimeout(getLobbyState, 3000);
    }
  }

  var command = addGame({ cmd: 'getChatHistory' });
  if (sections.lobby.last_id)
  {
    $.extend(command, { since: sections.lobby.last_id });
  }
  sendRequest(command, function (json)
  {
    if (json.chat.length)
    {
      sections.lobby.last_id = json.chat[json.chat.length-1].id;
      $.each(json.chat, function(i, entry)
      {
        // example: 2010-11-18 13:06:08.071000
        var match = entry.time.match(/^[\d-]+\s(\d\d):(\d\d).*$/);
        var hours = (parseInt(match[1]) - (new Date()).getTimezoneOffset() / 60) % 24;
        var minutes = match[2];
        var time = '[' + hours + ':' + minutes + ']';
        $('#chat-window').append($('<div/>')
          .append($('<p/>', { class: 'chat-header' })
            .append(time)
            .append($('<br/>'))
            .append($('<p/>', { class: 'chat-username', text: entry.username })))
          .append($('<p/>', { class: 'chat-message', text: entry.message }))
        );
      });
    }
    delayedSetTimeout();
  });

  sendRequest(addGame({ action: 'getPlayersListForGame' }), function (json)
  {
    var all_ready = json.players.length == sessionStorage.max_players;

    var players_counter = $('#players h3').empty();
    players_counter.text(json.players.length + ' / ' + sessionStorage.max_players);

    var players_list = $('#players-list').empty();
    $.each(json.players, function(i, player)
    {
      var status = player.status.replace('_', '-');
      var ready = status == 'ready' || status == 'in-game';
      all_ready = all_ready && ready;
      players_list
        .append($('<tr/>')
          .append($('<td/>', { class: 'username' }).text(player.username))
          .append($('<td/>').addClass(status).addClass('status')))
    });
    if (all_ready)
    {
      sessionStorage.armyName = $('#choose-army :selected').text();
      showSection('game');
    }
    delayedSetTimeout();
  });
}


function describeSections()
{
	sections = {
		'registration': new Section('registration'),
		'autorisation': new Section('autorisation'),
		'lobby': new LobbySection(),
	}
}

function initHorzMenu()
{
	$("#sign-out").click(function()
	{
		sendRequest({ action :'unregister' }, function (json)
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
		var message = $('#send-messge-text', form);
		if (message.val()!="")
		{
			return submitForm(form, function() {message.val('');});
		}
		return false;
	}
			
	);
}

function clearForm(form)
{
	$('.error', form).remove();
	$('input[type!="submit"]', form).val('');
}

$(document).ready(function()
{
	//initNavigation();
	initHorzMenu();
	initBinds();

	$('input:submit, a.button').button();
	//$('#auto-turn').button();
	$('input:text').addClass('ui-widget');

	describeSections();
	showSection(getCurrentSectionName() || "autorisation");
});
