function enable(selector)
{
  $(selector).removeAttr('disabled');
}

function disable(selector)
{
  $(selector).attr('disabled', 'disabled');
}
