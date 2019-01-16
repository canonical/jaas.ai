/**
  Format a date to human readable form.
 */
window.Jujucharms._HBSformatDate = function(date, format) {
  return new Date(date).toISOString().slice(0, 10);
};

/**
  Format a date to human readable form.
 */
window.Jujucharms._HBSeveryNth = function(context, every, options) {
  var fn = options.fn,
    inverse = options.inverse;
  var ret = '';
  if (context && context.length > 0) {
    for (var i = 0, j = context.length; i < j; i += 1) {
      var modZero = i % every === 0;
      var modLast = ((i + 1) / every) % 1 === 0;
      ret =
        ret +
        fn(
          Object.assign({}, context[i], {
            isModZero: modZero,
            isModLast: modLast,
            isModZeroNotFirst: modZero && i > 0,
            isLast: i === context.length - 1
          })
        );
    }
  } else {
    ret = inverse(this);
  }
  return ret;
};

/**
  Register handlebars helpers.
  */
window.Jujucharms.registerHelpers = function() {
  Handlebars.registerHelper('formatDate', window.Jujucharms._HBSformatDate);
  Handlebars.registerHelper('everyNth', window.Jujucharms._HBSeveryNth);
};
