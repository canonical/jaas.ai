/* plugins/handlebars.runtime-v2.0.0.js */
/*!

 handlebars v2.0.0

Copyright (C) 2011-2014 by Yehuda Katz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@license
*/
/* exported Handlebars */
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory();
  } else {
    root.Handlebars = root.Handlebars || factory();
  }
})(this, function() {
  // handlebars/safe-string.js
  var __module3__ = (function() {
    'use strict';
    var __exports__;
    // Build out our basic SafeString type
    function SafeString(string) {
      this.string = string;
    }

    SafeString.prototype.toString = function() {
      return '' + this.string;
    };

    __exports__ = SafeString;
    return __exports__;
  })();

  // handlebars/utils.js
  var __module2__ = (function(__dependency1__) {
    'use strict';
    var __exports__ = {};
    /*jshint -W004 */
    var SafeString = __dependency1__;

    var escape = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
      '`': '&#x60;'
    };

    var badChars = /[&<>"'`]/g;
    var possible = /[&<>"'`]/;

    function escapeChar(chr) {
      return escape[chr];
    }

    function extend(obj /* , ...source */) {
      for (var i = 1; i < arguments.length; i++) {
        for (var key in arguments[i]) {
          if (Object.prototype.hasOwnProperty.call(arguments[i], key)) {
            obj[key] = arguments[i][key];
          }
        }
      }

      return obj;
    }

    __exports__.extend = extend;
    var toString = Object.prototype.toString;
    __exports__.toString = toString;
    // Sourced from lodash
    // https://github.com/bestiejs/lodash/blob/master/LICENSE.txt
    var isFunction = function(value) {
      return typeof value === 'function';
    };
    // fallback for older versions of Chrome and Safari
    /* istanbul ignore next */
    if (isFunction(/x/)) {
      isFunction = function(value) {
        return typeof value === 'function' && toString.call(value) === '[object Function]';
      };
    }
    var isFunction;
    __exports__.isFunction = isFunction;
    /* istanbul ignore next */
    var isArray =
      Array.isArray ||
      function(value) {
        return value && typeof value === 'object'
          ? toString.call(value) === '[object Array]'
          : false;
      };
    __exports__.isArray = isArray;

    function escapeExpression(string) {
      // don't escape SafeStrings, since they're already safe
      if (string instanceof SafeString) {
        return string.toString();
      } else if (string == null) {
        return '';
      } else if (!string) {
        return string + '';
      }

      // Force a string conversion as this will be done by the append regardless and
      // the regex test will do this transparently behind the scenes, causing issues if
      // an object's to string has escaped characters in it.
      string = '' + string;

      if (!possible.test(string)) {
        return string;
      }
      return string.replace(badChars, escapeChar);
    }

    __exports__.escapeExpression = escapeExpression;
    function isEmpty(value) {
      if (!value && value !== 0) {
        return true;
      } else if (isArray(value) && value.length === 0) {
        return true;
      } else {
        return false;
      }
    }

    __exports__.isEmpty = isEmpty;
    function appendContextPath(contextPath, id) {
      return (contextPath ? contextPath + '.' : '') + id;
    }

    __exports__.appendContextPath = appendContextPath;
    return __exports__;
  })(__module3__);

  // handlebars/exception.js
  var __module4__ = (function() {
    'use strict';
    var __exports__;

    var errorProps = [
      'description',
      'fileName',
      'lineNumber',
      'message',
      'name',
      'number',
      'stack'
    ];

    function Exception(message, node) {
      var line;
      if (node && node.firstLine) {
        line = node.firstLine;

        message += ' - ' + line + ':' + node.firstColumn;
      }

      var tmp = Error.prototype.constructor.call(this, message);

      // Unfortunately errors are not enumerable in Chrome (at least), so `for prop in tmp` doesn't work.
      for (var idx = 0; idx < errorProps.length; idx++) {
        this[errorProps[idx]] = tmp[errorProps[idx]];
      }

      if (line) {
        this.lineNumber = line;
        this.column = node.firstColumn;
      }
    }

    Exception.prototype = new Error();

    __exports__ = Exception;
    return __exports__;
  })();

  // handlebars/base.js
  var __module1__ = (function(__dependency1__, __dependency2__) {
    'use strict';
    var __exports__ = {};
    var Utils = __dependency1__;
    var Exception = __dependency2__;

    var VERSION = '2.0.0';
    __exports__.VERSION = VERSION;
    var COMPILER_REVISION = 6;
    __exports__.COMPILER_REVISION = COMPILER_REVISION;
    var REVISION_CHANGES = {
      1: '<= 1.0.rc.2', // 1.0.rc.2 is actually rev2 but doesn't report it
      2: '== 1.0.0-rc.3',
      3: '== 1.0.0-rc.4',
      4: '== 1.x.x',
      5: '== 2.0.0-alpha.x',
      6: '>= 2.0.0-beta.1'
    };
    __exports__.REVISION_CHANGES = REVISION_CHANGES;
    var isArray = Utils.isArray,
      isFunction = Utils.isFunction,
      toString = Utils.toString,
      objectType = '[object Object]';

    function HandlebarsEnvironment(helpers, partials) {
      this.helpers = helpers || {};
      this.partials = partials || {};

      registerDefaultHelpers(this);
    }

    __exports__.HandlebarsEnvironment = HandlebarsEnvironment;
    HandlebarsEnvironment.prototype = {
      constructor: HandlebarsEnvironment,

      logger: logger,
      log: log,

      registerHelper: function(name, fn) {
        if (toString.call(name) === objectType) {
          if (fn) {
            throw new Exception('Arg not supported with multiple helpers');
          }
          Utils.extend(this.helpers, name);
        } else {
          this.helpers[name] = fn;
        }
      },
      unregisterHelper: function(name) {
        delete this.helpers[name];
      },

      registerPartial: function(name, partial) {
        if (toString.call(name) === objectType) {
          Utils.extend(this.partials, name);
        } else {
          this.partials[name] = partial;
        }
      },
      unregisterPartial: function(name) {
        delete this.partials[name];
      }
    };

    function registerDefaultHelpers(instance) {
      instance.registerHelper('helperMissing', function(/* [args, ]options */) {
        if (arguments.length === 1) {
          // A missing field in a {{foo}} constuct.
          return undefined;
        } else {
          // Someone is actually trying to call something, blow up.
          throw new Exception(
            "Missing helper: '" + arguments[arguments.length - 1].name + "'"
          );
        }
      });

      instance.registerHelper('blockHelperMissing', function(context, options) {
        var inverse = options.inverse,
          fn = options.fn;

        if (context === true) {
          return fn(this);
        } else if (context === false || context == null) {
          return inverse(this);
        } else if (isArray(context)) {
          if (context.length > 0) {
            if (options.ids) {
              options.ids = [options.name];
            }

            return instance.helpers.each(context, options);
          } else {
            return inverse(this);
          }
        } else {
          if (options.data && options.ids) {
            var data = createFrame(options.data);
            data.contextPath = Utils.appendContextPath(options.data.contextPath, options.name);
            options = {data: data};
          }

          return fn(context, options);
        }
      });

      instance.registerHelper('each', function(context, options) {
        if (!options) {
          throw new Exception('Must pass iterator to #each');
        }

        var fn = options.fn,
          inverse = options.inverse;
        var i = 0,
          ret = '',
          data;

        var contextPath;
        if (options.data && options.ids) {
          contextPath =
            Utils.appendContextPath(options.data.contextPath, options.ids[0]) + '.';
        }

        if (isFunction(context)) {
          context = context.call(this);
        }

        if (options.data) {
          data = createFrame(options.data);
        }

        if (context && typeof context === 'object') {
          if (isArray(context)) {
            for (var j = context.length; i < j; i++) {
              if (data) {
                data.index = i;
                data.first = i === 0;
                data.last = i === context.length - 1;

                if (contextPath) {
                  data.contextPath = contextPath + i;
                }
              }
              ret = ret + fn(context[i], {data: data});
            }
          } else {
            for (var key in context) {
              if (context.hasOwnProperty(key)) {
                if (data) {
                  data.key = key;
                  data.index = i;
                  data.first = i === 0;

                  if (contextPath) {
                    data.contextPath = contextPath + key;
                  }
                }
                ret = ret + fn(context[key], {data: data});
                i++;
              }
            }
          }
        }

        if (i === 0) {
          ret = inverse(this);
        }

        return ret;
      });

      instance.registerHelper('if', function(conditional, options) {
        if (isFunction(conditional)) {
          conditional = conditional.call(this);
        }

        // Default behavior is to render the positive path if the value is truthy and not empty.
        // The `includeZero` option may be set to treat the condtional as purely not empty based on the
        // behavior of isEmpty. Effectively this determines if 0 is handled by the positive path or negative.
        if ((!options.hash.includeZero && !conditional) || Utils.isEmpty(conditional)) {
          return options.inverse(this);
        } else {
          return options.fn(this);
        }
      });

      instance.registerHelper('unless', function(conditional, options) {
        return instance.helpers['if'].call(this, conditional, {
          fn: options.inverse,
          inverse: options.fn,
          hash: options.hash
        });
      });

      instance.registerHelper('with', function(context, options) {
        if (isFunction(context)) {
          context = context.call(this);
        }

        var fn = options.fn;

        if (!Utils.isEmpty(context)) {
          if (options.data && options.ids) {
            var data = createFrame(options.data);
            data.contextPath = Utils.appendContextPath(
              options.data.contextPath,
              options.ids[0]
            );
            options = {data: data};
          }

          return fn(context, options);
        } else {
          return options.inverse(this);
        }
      });

      instance.registerHelper('log', function(message, options) {
        var level =
          options.data && options.data.level != null ? parseInt(options.data.level, 10) : 1;
        instance.log(level, message);
      });

      instance.registerHelper('lookup', function(obj, field) {
        return obj && obj[field];
      });
    }

    var logger = {
      methodMap: {0: 'debug', 1: 'info', 2: 'warn', 3: 'error'},

      // State enum
      DEBUG: 0,
      INFO: 1,
      WARN: 2,
      ERROR: 3,
      level: 3,

      // can be overridden in the host environment
      log: function(level, message) {
        if (logger.level <= level) {
          var method = logger.methodMap[level];
          if (typeof console !== 'undefined' && console[method]) {
            console[method].call(console, message);
          }
        }
      }
    };
    __exports__.logger = logger;
    var log = logger.log;
    __exports__.log = log;
    var createFrame = function(object) {
      var frame = Utils.extend({}, object);
      frame._parent = object;
      return frame;
    };
    __exports__.createFrame = createFrame;
    return __exports__;
  })(__module2__, __module4__);

  // handlebars/runtime.js
  var __module5__ = (function(__dependency1__, __dependency2__, __dependency3__) {
    'use strict';
    var __exports__ = {};
    var Utils = __dependency1__;
    var Exception = __dependency2__;
    var COMPILER_REVISION = __dependency3__.COMPILER_REVISION;
    var REVISION_CHANGES = __dependency3__.REVISION_CHANGES;
    var createFrame = __dependency3__.createFrame;

    function checkRevision(compilerInfo) {
      var compilerRevision = (compilerInfo && compilerInfo[0]) || 1,
        currentRevision = COMPILER_REVISION;

      if (compilerRevision !== currentRevision) {
        if (compilerRevision < currentRevision) {
          var runtimeVersions = REVISION_CHANGES[currentRevision],
            compilerVersions = REVISION_CHANGES[compilerRevision];
          throw new Exception(
            'Template was precompiled with an older version of Handlebars than the current runtime. ' +
              'Please update your precompiler to a newer version (' +
              runtimeVersions +
              ') or downgrade your runtime to an older version (' +
              compilerVersions +
              ').'
          );
        } else {
          // Use the embedded version info since the runtime doesn't know about this revision yet
          throw new Exception(
            'Template was precompiled with a newer version of Handlebars than the current runtime. ' +
              'Please update your runtime to a newer version (' +
              compilerInfo[1] +
              ').'
          );
        }
      }
    }

    __exports__.checkRevision = checkRevision; // TODO: Remove this line and break up compilePartial

    function template(templateSpec, env) {
      /* istanbul ignore next */
      if (!env) {
        throw new Exception('No environment passed to template');
      }
      if (!templateSpec || !templateSpec.main) {
        throw new Exception('Unknown template object: ' + typeof templateSpec);
      }

      // Note: Using env.VM references rather than local var references throughout this section to allow
      // for external users to override these as psuedo-supported APIs.
      env.VM.checkRevision(templateSpec.compiler);

      var invokePartialWrapper = function(
        partial,
        indent,
        name,
        context,
        hash,
        helpers,
        partials,
        data,
        depths
      ) {
        if (hash) {
          context = Utils.extend({}, context, hash);
        }

        var result = env.VM.invokePartial.call(
          this,
          partial,
          name,
          context,
          helpers,
          partials,
          data,
          depths
        );

        if (result == null && env.compile) {
          var options = {
            helpers: helpers,
            partials: partials,
            data: data,
            depths: depths
          };
          partials[name] = env.compile(
            partial,
            {data: data !== undefined, compat: templateSpec.compat},
            env
          );
          result = partials[name](context, options);
        }
        if (result != null) {
          if (indent) {
            var lines = result.split('\n');
            for (var i = 0, l = lines.length; i < l; i++) {
              if (!lines[i] && i + 1 === l) {
                break;
              }

              lines[i] = indent + lines[i];
            }
            result = lines.join('\n');
          }
          return result;
        } else {
          throw new Exception(
            'The partial ' + name + ' could not be compiled when running in runtime-only mode'
          );
        }
      };

      // Just add water
      var container = {
        lookup: function(depths, name) {
          var len = depths.length;
          for (var i = 0; i < len; i++) {
            if (depths[i] && depths[i][name] != null) {
              return depths[i][name];
            }
          }
        },
        lambda: function(current, context) {
          return typeof current === 'function' ? current.call(context) : current;
        },

        escapeExpression: Utils.escapeExpression,
        invokePartial: invokePartialWrapper,

        fn: function(i) {
          return templateSpec[i];
        },

        programs: [],
        program: function(i, data, depths) {
          var programWrapper = this.programs[i],
            fn = this.fn(i);
          if (data || depths) {
            programWrapper = program(this, i, fn, data, depths);
          } else if (!programWrapper) {
            programWrapper = this.programs[i] = program(this, i, fn);
          }
          return programWrapper;
        },

        data: function(data, depth) {
          while (data && depth--) {
            data = data._parent;
          }
          return data;
        },
        merge: function(param, common) {
          var ret = param || common;

          if (param && common && param !== common) {
            ret = Utils.extend({}, common, param);
          }

          return ret;
        },

        noop: env.VM.noop,
        compilerInfo: templateSpec.compiler
      };

      var ret = function(context, options) {
        options = options || {};
        var data = options.data;

        ret._setup(options);
        if (!options.partial && templateSpec.useData) {
          data = initData(context, data);
        }
        var depths;
        if (templateSpec.useDepths) {
          depths = options.depths ? [context].concat(options.depths) : [context];
        }

        return templateSpec.main.call(
          container,
          context,
          container.helpers,
          container.partials,
          data,
          depths
        );
      };
      ret.isTop = true;

      ret._setup = function(options) {
        if (!options.partial) {
          container.helpers = container.merge(options.helpers, env.helpers);

          if (templateSpec.usePartial) {
            container.partials = container.merge(options.partials, env.partials);
          }
        } else {
          container.helpers = options.helpers;
          container.partials = options.partials;
        }
      };

      ret._child = function(i, data, depths) {
        if (templateSpec.useDepths && !depths) {
          throw new Exception('must pass parent depths');
        }

        return program(container, i, templateSpec[i], data, depths);
      };
      return ret;
    }

    __exports__.template = template;
    function program(container, i, fn, data, depths) {
      var prog = function(context, options) {
        options = options || {};

        return fn.call(
          container,
          context,
          container.helpers,
          container.partials,
          options.data || data,
          depths && [context].concat(depths)
        );
      };
      prog.program = i;
      prog.depth = depths ? depths.length : 0;
      return prog;
    }

    __exports__.program = program;
    function invokePartial(partial, name, context, helpers, partials, data, depths) {
      var options = {
        partial: true,
        helpers: helpers,
        partials: partials,
        data: data,
        depths: depths
      };

      if (partial === undefined) {
        throw new Exception('The partial ' + name + ' could not be found');
      } else if (partial instanceof Function) {
        return partial(context, options);
      }
    }

    __exports__.invokePartial = invokePartial;
    function noop() {
      return '';
    }

    __exports__.noop = noop;
    function initData(context, data) {
      if (!data || !('root' in data)) {
        data = data ? createFrame(data) : {};
        data.root = context;
      }
      return data;
    }
    return __exports__;
  })(__module2__, __module4__, __module1__);

  // handlebars.runtime.js
  var __module0__ = (function(
    __dependency1__,
    __dependency2__,
    __dependency3__,
    __dependency4__,
    __dependency5__
  ) {
    'use strict';
    var __exports__;
    /*globals Handlebars: true */
    var base = __dependency1__;

    // Each of these augment the Handlebars object. No need to setup here.
    // (This is done to easily share code between commonjs and browse envs)
    var SafeString = __dependency2__;
    var Exception = __dependency3__;
    var Utils = __dependency4__;
    var runtime = __dependency5__;

    // For compatibility and usage outside of module systems, make the Handlebars object a namespace
    var create = function() {
      var hb = new base.HandlebarsEnvironment();

      Utils.extend(hb, base);
      hb.SafeString = SafeString;
      hb.Exception = Exception;
      hb.Utils = Utils;
      hb.escapeExpression = Utils.escapeExpression;

      hb.VM = runtime;
      hb.template = function(spec) {
        return runtime.template(spec, hb);
      };

      return hb;
    };

    var Handlebars = create();
    Handlebars.create = create;

    Handlebars['default'] = Handlebars;

    __exports__ = Handlebars;
    return __exports__;
  })(__module1__, __module3__, __module4__, __module2__, __module5__);

  return __module0__;
});

/* plugins/prism.js */
/* http://prismjs.com/download.html?themes=prism-twilight&languages=markup+css+clike+javascript+bash+git+go+makefile+python+yaml */
var _self =
    'undefined' != typeof window
      ? window
      : 'undefined' != typeof WorkerGlobalScope && self instanceof WorkerGlobalScope
      ? self
      : {},
  Prism = (function() {
    var e = /\blang(?:uage)?-(?!\*)(\w+)\b/i,
      t = (_self.Prism = {
        util: {
          encode: function(e) {
            return e instanceof n
              ? new n(e.type, t.util.encode(e.content), e.alias)
              : 'Array' === t.util.type(e)
              ? e.map(t.util.encode)
              : e
                  .replace(/&/g, '&amp;')
                  .replace(/</g, '&lt;')
                  .replace(/\u00a0/g, ' ');
          },
          type: function(e) {
            return Object.prototype.toString.call(e).match(/\[object (\w+)\]/)[1];
          },
          clone: function(e) {
            var n = t.util.type(e);
            switch (n) {
              case 'Object':
                var a = {};
                for (var r in e) e.hasOwnProperty(r) && (a[r] = t.util.clone(e[r]));
                return a;
              case 'Array':
                return (
                  e.map &&
                  e.map(function(e) {
                    return t.util.clone(e);
                  })
                );
            }
            return e;
          }
        },
        languages: {
          extend: function(e, n) {
            var a = t.util.clone(t.languages[e]);
            for (var r in n) a[r] = n[r];
            return a;
          },
          insertBefore: function(e, n, a, r) {
            r = r || t.languages;
            var i = r[e];
            if (2 == arguments.length) {
              a = arguments[1];
              for (var l in a) a.hasOwnProperty(l) && (i[l] = a[l]);
              return i;
            }
            var s = {};
            for (var o in i)
              if (i.hasOwnProperty(o)) {
                if (o == n) for (var l in a) a.hasOwnProperty(l) && (s[l] = a[l]);
                s[o] = i[o];
              }
            return (
              t.languages.DFS(t.languages, function(t, n) {
                n === r[e] && t != e && (this[t] = s);
              }),
              (r[e] = s)
            );
          },
          DFS: function(e, n, a) {
            for (var r in e)
              e.hasOwnProperty(r) &&
                (n.call(e, r, e[r], a || r),
                'Object' === t.util.type(e[r])
                  ? t.languages.DFS(e[r], n)
                  : 'Array' === t.util.type(e[r]) && t.languages.DFS(e[r], n, r));
          }
        },
        highlightAll: function(e, n) {
          for (
            var a,
              r = document.querySelectorAll(
                'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'
              ),
              i = 0;
            (a = r[i++]);

          )
            t.highlightElement(a, e === !0, n);
        },
        highlightElement: function(a, r, i) {
          for (var l, s, o = a; o && !e.test(o.className); ) o = o.parentNode;
          if (
            (o && ((l = (o.className.match(e) || [, ''])[1]), (s = t.languages[l])),
            (a.className = a.className.replace(e, '').replace(/\s+/g, ' ') + ' language-' + l),
            (o = a.parentNode),
            /pre/i.test(o.nodeName) &&
              (o.className =
                o.className.replace(e, '').replace(/\s+/g, ' ') + ' language-' + l),
            s)
          ) {
            var u = a.textContent;
            if (u) {
              u = u.replace(/^(?:\r?\n|\r)/, '');
              var g = {element: a, language: l, grammar: s, code: u};
              if ((t.hooks.run('before-highlight', g), r && _self.Worker)) {
                var c = new Worker(t.filename);
                (c.onmessage = function(e) {
                  (g.highlightedCode = n.stringify(JSON.parse(e.data), l)),
                    t.hooks.run('before-insert', g),
                    (g.element.innerHTML = g.highlightedCode),
                    i && i.call(g.element),
                    t.hooks.run('after-highlight', g);
                }),
                  c.postMessage(JSON.stringify({language: g.language, code: g.code}));
              } else
                (g.highlightedCode = t.highlight(g.code, g.grammar, g.language)),
                  t.hooks.run('before-insert', g),
                  (g.element.innerHTML = g.highlightedCode),
                  i && i.call(a),
                  t.hooks.run('after-highlight', g);
            }
          }
        },
        highlight: function(e, a, r) {
          var i = t.tokenize(e, a);
          return n.stringify(t.util.encode(i), r);
        },
        tokenize: function(e, n) {
          var a = t.Token,
            r = [e],
            i = n.rest;
          if (i) {
            for (var l in i) n[l] = i[l];
            delete n.rest;
          }
          e: for (var l in n)
            if (n.hasOwnProperty(l) && n[l]) {
              var s = n[l];
              s = 'Array' === t.util.type(s) ? s : [s];
              for (var o = 0; o < s.length; ++o) {
                var u = s[o],
                  g = u.inside,
                  c = !!u.lookbehind,
                  f = 0,
                  h = u.alias;
                u = u.pattern || u;
                for (var p = 0; p < r.length; p++) {
                  var d = r[p];
                  if (r.length > e.length) break e;
                  if (!(d instanceof a)) {
                    u.lastIndex = 0;
                    var m = u.exec(d);
                    if (m) {
                      c && (f = m[1].length);
                      var y = m.index - 1 + f,
                        m = m[0].slice(f),
                        v = m.length,
                        k = y + v,
                        b = d.slice(0, y + 1),
                        w = d.slice(k + 1),
                        N = [p, 1];
                      b && N.push(b);
                      var O = new a(l, g ? t.tokenize(m, g) : m, h);
                      N.push(O), w && N.push(w), Array.prototype.splice.apply(r, N);
                    }
                  }
                }
              }
            }
          return r;
        },
        hooks: {
          all: {},
          add: function(e, n) {
            var a = t.hooks.all;
            (a[e] = a[e] || []), a[e].push(n);
          },
          run: function(e, n) {
            var a = t.hooks.all[e];
            if (a && a.length) for (var r, i = 0; (r = a[i++]); ) r(n);
          }
        }
      }),
      n = (t.Token = function(e, t, n) {
        (this.type = e), (this.content = t), (this.alias = n);
      });
    if (
      ((n.stringify = function(e, a, r) {
        if ('string' == typeof e) return e;
        if ('Array' === t.util.type(e))
          return e
            .map(function(t) {
              return n.stringify(t, a, e);
            })
            .join('');
        var i = {
          type: e.type,
          content: n.stringify(e.content, a, r),
          tag: 'span',
          classes: ['token', e.type],
          attributes: {},
          language: a,
          parent: r
        };
        if (('comment' == i.type && (i.attributes.spellcheck = 'true'), e.alias)) {
          var l = 'Array' === t.util.type(e.alias) ? e.alias : [e.alias];
          Array.prototype.push.apply(i.classes, l);
        }
        t.hooks.run('wrap', i);
        var s = '';
        for (var o in i.attributes) s += o + '="' + (i.attributes[o] || '') + '"';
        return (
          '<' +
          i.tag +
          ' class="' +
          i.classes.join(' ') +
          '" ' +
          s +
          '>' +
          i.content +
          '</' +
          i.tag +
          '>'
        );
      }),
      !_self.document)
    )
      return _self.addEventListener
        ? (_self.addEventListener(
            'message',
            function(e) {
              var n = JSON.parse(e.data),
                a = n.language,
                r = n.code;
              _self.postMessage(JSON.stringify(t.util.encode(t.tokenize(r, t.languages[a])))),
                _self.close();
            },
            !1
          ),
          _self.Prism)
        : _self.Prism;
    var a = document.getElementsByTagName('script');
    return (
      (a = a[a.length - 1]),
      a &&
        ((t.filename = a.src),
        document.addEventListener &&
          !a.hasAttribute('data-manual') &&
          document.addEventListener('DOMContentLoaded', t.highlightAll)),
      _self.Prism
    );
  })();
'undefined' != typeof module && module.exports && (module.exports = Prism);
(Prism.languages.markup = {
  comment: /<!--[\w\W]*?-->/,
  prolog: /<\?[\w\W]+?\?>/,
  doctype: /<!DOCTYPE[\w\W]+?>/,
  cdata: /<!\[CDATA\[[\w\W]*?]]>/i,
  tag: {
    pattern: /<\/?[^\s>\/]+(?:\s+[^\s>\/=]+(?:=(?:("|')(?:\\\1|\\?(?!\1)[\w\W])*\1|[^\s'">=]+))?)*\s*\/?>/i,
    inside: {
      tag: {
        pattern: /^<\/?[^\s>\/]+/i,
        inside: {punctuation: /^<\/?/, namespace: /^[^\s>\/:]+:/}
      },
      'attr-value': {
        pattern: /=(?:('|")[\w\W]*?(\1)|[^\s>]+)/i,
        inside: {punctuation: /[=>"']/}
      },
      punctuation: /\/?>/,
      'attr-name': {
        pattern: /[^\s>\/]+/,
        inside: {namespace: /^[^\s>\/:]+:/}
      }
    }
  },
  entity: /&#?[\da-z]{1,8};/i
}),
  Prism.hooks.add('wrap', function(t) {
    'entity' === t.type && (t.attributes.title = t.content.replace(/&amp;/, '&'));
  });
(Prism.languages.css = {
  comment: /\/\*[\w\W]*?\*\//,
  atrule: {pattern: /@[\w-]+?.*?(;|(?=\s*\{))/i, inside: {rule: /@[\w-]+/}},
  url: /url\((?:(["'])(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])*\1|.*?)\)/i,
  selector: /[^\{\}\s][^\{\};]*?(?=\s*\{)/,
  string: /("|')(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])*\1/,
  property: /(\b|\B)[\w-]+(?=\s*:)/i,
  important: /\B!important\b/i,
  function: /[-a-z0-9]+(?=\()/i,
  punctuation: /[(){};:]/
}),
  (Prism.languages.css.atrule.inside.rest = Prism.util.clone(Prism.languages.css)),
  Prism.languages.markup &&
    (Prism.languages.insertBefore('markup', 'tag', {
      style: {
        pattern: /<style[\w\W]*?>[\w\W]*?<\/style>/i,
        inside: {
          tag: {
            pattern: /<style[\w\W]*?>|<\/style>/i,
            inside: Prism.languages.markup.tag.inside
          },
          rest: Prism.languages.css
        },
        alias: 'language-css'
      }
    }),
    Prism.languages.insertBefore(
      'inside',
      'attr-value',
      {
        'style-attr': {
          pattern: /\s*style=("|').*?\1/i,
          inside: {
            'attr-name': {
              pattern: /^\s*style/i,
              inside: Prism.languages.markup.tag.inside
            },
            punctuation: /^\s*=\s*['"]|['"]\s*$/,
            'attr-value': {pattern: /.+/i, inside: Prism.languages.css}
          },
          alias: 'language-css'
        }
      },
      Prism.languages.markup.tag
    ));
Prism.languages.clike = {
  comment: [
    {pattern: /(^|[^\\])\/\*[\w\W]*?\*\//, lookbehind: !0},
    {pattern: /(^|[^\\:])\/\/.*/, lookbehind: !0}
  ],
  string: /("|')(\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,
  'class-name': {
    pattern: /((?:(?:class|interface|extends|implements|trait|instanceof|new)\s+)|(?:catch\s+\())[a-z0-9_\.\\]+/i,
    lookbehind: !0,
    inside: {punctuation: /(\.|\\)/}
  },
  keyword: /\b(if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b/,
  boolean: /\b(true|false)\b/,
  function: /[a-z0-9_]+(?=\()/i,
  number: /\b-?(0x[\dA-Fa-f]+|\d*\.?\d+([Ee]-?\d+)?)\b/,
  operator: /[-+]{1,2}|!|<=?|>=?|={1,3}|&{1,2}|\|?\||\?|\*|\/|~|\^|%/,
  punctuation: /[{}[\];(),.:]/
};
(Prism.languages.javascript = Prism.languages.extend('clike', {
  keyword: /\b(as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|false|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|true|try|typeof|var|void|while|with|yield)\b/,
  number: /\b-?(0x[\dA-Fa-f]+|0b[01]+|0o[0-7]+|\d*\.?\d+([Ee][+-]?\d+)?|NaN|Infinity)\b/,
  function: /(?!\d)[a-z0-9_$]+(?=\()/i
})),
  Prism.languages.insertBefore('javascript', 'keyword', {
    regex: {
      pattern: /(^|[^/])\/(?!\/)(\[.+?]|\\.|[^/\\\r\n])+\/[gimyu]{0,5}(?=\s*($|[\r\n,.;})]))/,
      lookbehind: !0
    }
  }),
  Prism.languages.insertBefore('javascript', 'class-name', {
    'template-string': {
      pattern: /`(?:\\`|\\?[^`])*`/,
      inside: {
        interpolation: {
          pattern: /\$\{[^}]+\}/,
          inside: {
            'interpolation-punctuation': {
              pattern: /^\$\{|\}$/,
              alias: 'punctuation'
            },
            rest: Prism.languages.javascript
          }
        },
        string: /[\s\S]+/
      }
    }
  }),
  Prism.languages.markup &&
    Prism.languages.insertBefore('markup', 'tag', {
      script: {
        pattern: /<script[\w\W]*?>[\w\W]*?<\/script>/i,
        inside: {
          tag: {
            pattern: /<script[\w\W]*?>|<\/script>/i,
            inside: Prism.languages.markup.tag.inside
          },
          rest: Prism.languages.javascript
        },
        alias: 'language-javascript'
      }
    });
(Prism.languages.bash = Prism.languages.extend('clike', {
  comment: {pattern: /(^|[^"{\\])#.*/, lookbehind: !0},
  string: {
    pattern: /("|')(\\?[\s\S])*?\1/,
    inside: {property: /\$([a-zA-Z0-9_#\?\-\*!@]+|\{[^\}]+\})/}
  },
  number: {
    pattern: /([^\w\.])-?(0x[\dA-Fa-f]+|\d*\.?\d+([Ee]-?\d+)?)\b/,
    lookbehind: !0
  },
  function: /\b(?:alias|apropos|apt-get|aptitude|aspell|awk|basename|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|chkconfig|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|cut|date|dc|dd|ddrescue|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|du|egrep|eject|enable|env|ethtool|eval|exec|expand|expect|export|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|fuser|gawk|getopts|git|grep|groupadd|groupdel|groupmod|groups|gzip|hash|head|help|hg|history|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|jobs|join|kill|killall|less|link|ln|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|most|mount|mtools|mtr|mv|mmv|nano|netstat|nice|nl|nohup|notify-send|nslookup|open|op|passwd|paste|pathchk|ping|pkill|popd|pr|printcap|printenv|printf|ps|pushd|pv|pwd|quota|quotacheck|quotactl|ram|rar|rcp|read|readarray|readonly|reboot|rename|renice|remsync|rev|rm|rmdir|rsync|screen|scp|sdiff|sed|seq|service|sftp|shift|shopt|shutdown|sleep|slocate|sort|source|split|ssh|stat|strace|su|sudo|sum|suspend|sync|tail|tar|tee|test|time|timeout|times|touch|top|traceroute|trap|tr|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unrar|unshar|uptime|useradd|userdel|usermod|users|uuencode|uudecode|v|vdir|vi|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yes|zip)\b/,
  keyword: /\b(if|then|else|elif|fi|for|break|continue|while|in|case|function|select|do|done|until|echo|exit|return|set|declare)\b/
})),
  Prism.languages.insertBefore('bash', 'keyword', {
    property: /\$([a-zA-Z0-9_#\?\-\*!@]+|\{[^}]+\})/
  }),
  Prism.languages.insertBefore('bash', 'comment', {
    important: /^#!\s*\/bin\/bash|^#!\s*\/bin\/sh/
  });
Prism.languages.git = {
  comment: /^#.*$/m,
  string: /("|')(\\?.)*?\1/m,
  command: {pattern: /^.*\$ git .*$/m, inside: {parameter: /\s(--|-)\w+/m}},
  coord: /^@@.*@@$/m,
  deleted: /^-(?!-).+$/m,
  inserted: /^\+(?!\+).+$/m,
  commit_sha1: /^commit \w{40}$/m
};
(Prism.languages.go = Prism.languages.extend('clike', {
  keyword: /\b(break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go(to)?|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b/,
  builtin: /\b(bool|byte|complex(64|128)|error|float(32|64)|rune|string|u?int(8|16|32|64|)|uintptr|append|cap|close|complex|copy|delete|imag|len|make|new|panic|print(ln)?|real|recover)\b/,
  boolean: /\b(_|iota|nil|true|false)\b/,
  operator: /([(){}\[\]]|[*\/%^!]=?|\+[=+]?|-[>=-]?|\|[=|]?|>[=>]?|<(<|[=-])?|==?|&(&|=|^=?)?|\.(\.\.)?|[,;]|:=?)/,
  number: /\b(-?(0x[a-f\d]+|(\d+\.?\d*|\.\d+)(e[-+]?\d+)?)i?)\b/i,
  string: /("|'|`)(\\?.|\r|\n)*?\1/
})),
  delete Prism.languages.go['class-name'];
Prism.languages.makefile = {
  comment: {pattern: /(^|[^\\])#(?:\\[\s\S]|.)*/, lookbehind: !0},
  string: /(["'])(?:\\[\s\S]|(?!\1)[^\\\r\n])*\1/,
  builtin: /\.[A-Z][^:#=\s]+(?=\s*:(?!=))/,
  symbol: {
    pattern: /^[^:=\r\n]+(?=\s*:(?!=))/m,
    inside: {variable: /\$+(?:[^(){}:#=\s]+|(?=[({]))/}
  },
  variable: /\$+(?:[^(){}:#=\s]+|\([@*%<^+?][DF]\)|(?=[({]))/,
  keyword: [
    /\b(?:define|else|endef|endif|export|ifn?def|ifn?eq|-?include|override|private|sinclude|undefine|unexport|vpath)\b/,
    {
      pattern: /(\()(?:addsuffix|abspath|and|basename|call|dir|error|eval|file|filter(?:-out)?|findstring|firstword|flavor|foreach|guile|if|info|join|lastword|load|notdir|or|origin|patsubst|realpath|shell|sort|strip|subst|suffix|value|warning|wildcard|word(?:s|list)?)(?=[ \t])/,
      lookbehind: !0
    }
  ],
  operator: /(?:::|[?:+!])?=|[|@]/,
  punctuation: /[:;(){}]/
};
Prism.languages.python = {
  comment: {pattern: /(^|[^\\])#.*?(\r?\n|$)/, lookbehind: !0},
  string: /"""[\s\S]+?"""|'''[\s\S]+?'''|("|')(\\?.)*?\1/,
  function: {
    pattern: /((^|\s)def[ \t]+)([a-zA-Z_][a-zA-Z0-9_]*(?=\())/g,
    lookbehind: !0
  },
  keyword: /\b(as|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|pass|print|raise|return|try|while|with|yield)\b/,
  boolean: /\b(True|False)\b/,
  number: /\b-?(0[bo])?(?:(\d|0x[a-f])[\da-f]*\.?\d*|\.\d+)(?:e[+-]?\d+)?j?\b/i,
  operator: /[-+]|<=?|>=?|!|={1,2}|&{1,2}|\|?\||\?|\*|\/|~|\^|%|\b(or|and|not)\b/,
  punctuation: /[{}[\];(),.:]/
};
Prism.languages.yaml = {
  scalar: {
    pattern: /([\-:]\s*(![^\s]+)?[ \t]*[|>])[ \t]*(?:(\n[ \t]+)[^\r\n]+(?:\3[^\r\n]+)*)/,
    lookbehind: !0,
    alias: 'string'
  },
  comment: /#[^\n]+/,
  key: {
    pattern: /(\s*[:\-,[{\n?][ \t]*(![^\s]+)?[ \t]*)[^\n{[\]},#]+?(?=\s*:\s)/,
    lookbehind: !0,
    alias: 'atrule'
  },
  directive: {
    pattern: /((^|\n)[ \t]*)%[^\n]+/,
    lookbehind: !0,
    alias: 'important'
  },
  datetime: {
    pattern: /([:\-,[{]\s*(![^\s]+)?[ \t]*)(\d{4}-\d\d?-\d\d?([tT]|[ \t]+)\d\d?:\d{2}:\d{2}(\.\d*)?[ \t]*(Z|[-+]\d\d?(:\d{2})?)?|\d{4}-\d{2}-\d{2}|\d\d?:\d{2}(:\d{2}(\.\d*)?)?)(?=[ \t]*(\n|$|,|]|}))/,
    lookbehind: !0,
    alias: 'number'
  },
  boolean: {
    pattern: /([:\-,[{]\s*(![^\s]+)?[ \t]*)(true|false)[ \t]*(?=\n|$|,|]|})/i,
    lookbehind: !0,
    alias: 'important'
  },
  null: {
    pattern: /([:\-,[{]\s*(![^\s]+)?[ \t]*)(null|~)[ \t]*(?=\n|$|,|]|})/i,
    lookbehind: !0,
    alias: 'important'
  },
  string: {
    pattern: /([:\-,[{]\s*(![^\s]+)?[ \t]*)("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')(?=[ \t]*(\n|$|,|]|}))/,
    lookbehind: !0
  },
  number: {
    pattern: /([:\-,[{]\s*(![^\s]+)?[ \t]*)[+\-]?(0x[\dA-Fa-f]+|0o[0-7]+|(\d+\.?\d*|\.?\d+)(e[\+\-]?\d+)?|\.inf|\.nan)[ \t]*(?=\n|$|,|]|})/i,
    lookbehind: !0
  },
  tag: /![^\s]+/,
  important: /[&*][\w]+/,
  punctuation: /([:[\]{}\-,|>?]|---|\.\.\.)/
};

/* templates/templates.js */
(function() {
  var template = Handlebars.template,
    templates = (Handlebars.templates = Handlebars.templates || {});
  templates['blog-feed-v1'] = template({
    '1': function(depth0, helpers, partials, data) {
      var stack1,
        helper,
        lambda = this.lambda,
        escapeExpression = this.escapeExpression,
        helperMissing = helpers.helperMissing,
        functionType = 'function';
      return (
        '  <li class="p-list__item">\n    <h4 class="u-no-margin--bottom"><a href="' +
        escapeExpression(
          lambda(
            (stack1 =
              (stack1 = depth0 != null ? depth0.links : depth0) != null
                ? stack1['0']
                : stack1) != null
              ? stack1.href
              : stack1,
            depth0
          )
        ) +
        '">' +
        escapeExpression(
          lambda(
            (stack1 = depth0 != null ? depth0.title_detail : depth0) != null
              ? stack1.value
              : stack1,
            depth0
          )
        ) +
        '</a></h4>\n    <h6>' +
        escapeExpression(
          (helpers.formatDate || (depth0 && depth0.formatDate) || helperMissing).call(
            depth0,
            depth0 != null ? depth0.published : depth0,
            '%Y-%m-%d',
            {name: 'formatDate', hash: {}, data: data}
          )
        ) +
        ' by ' +
        escapeExpression(
          ((helper =
            (helper = helpers.author || (depth0 != null ? depth0.author : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'author', hash: {}, data: data})
            : helper)
        ) +
        '</h6>\n    <p>\n      ' +
        escapeExpression(
          lambda(
            (stack1 = depth0 != null ? depth0.summary_detail : depth0) != null
              ? stack1.value
              : stack1,
            depth0
          )
        ) +
        '\n    </p>\n  </li>\n'
      );
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        buffer = '<ul class="p-list">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.entries : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['blog-feed'] = template({
    '1': function(depth0, helpers, partials, data) {
      var stack1,
        helper,
        lambda = this.lambda,
        escapeExpression = this.escapeExpression,
        helperMissing = helpers.helperMissing,
        functionType = 'function',
        buffer =
          '  <li>\n    <h3><a href="' +
          escapeExpression(
            lambda(
              (stack1 =
                (stack1 = depth0 != null ? depth0.links : depth0) != null
                  ? stack1['0']
                  : stack1) != null
                ? stack1.href
                : stack1,
              depth0
            )
          ) +
          '">' +
          escapeExpression(
            lambda(
              (stack1 = depth0 != null ? depth0.title_detail : depth0) != null
                ? stack1.value
                : stack1,
              depth0
            )
          ) +
          '</a></h3>\n    <p class="note">' +
          escapeExpression(
            (helpers.formatDate || (depth0 && depth0.formatDate) || helperMissing).call(
              depth0,
              depth0 != null ? depth0.published : depth0,
              '%Y-%m-%d',
              {name: 'formatDate', hash: {}, data: data}
            )
          ) +
          ' by  ' +
          escapeExpression(
            ((helper =
              (helper = helpers.author || (depth0 != null ? depth0.author : depth0)) != null
                ? helper
                : helperMissing),
            typeof helper === functionType
              ? helper.call(depth0, {name: 'author', hash: {}, data: data})
              : helper)
          ) +
          '</p>\n    ';
      stack1 = lambda(
        (stack1 = depth0 != null ? depth0.summary_detail : depth0) != null
          ? stack1.value
          : stack1,
        depth0
      );
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '\n  </li>\n';
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        buffer = '<ul class="blog-list no-bullets">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.entries : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['connects'] = template({
    '1': function(depth0, helpers, partials, data) {
      var helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression;
      return (
        '    <li>\n        <a href="' +
        escapeExpression(
          ((helper =
            (helper = helpers.charm_url || (depth0 != null ? depth0.charm_url : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'charm_url', hash: {}, data: data})
            : helper)
        ) +
        '">\n            <span>\n                <p class="tooltip">\n                    <img height="75" width="75" src="' +
        escapeExpression(
          ((helper =
            (helper = helpers.icon_url || (depth0 != null ? depth0.icon_url : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'icon_url', hash: {}, data: data})
            : helper)
        ) +
        '">\n                    <span data-tooltip="' +
        escapeExpression(
          ((helper =
            (helper = helpers.charm_name || (depth0 != null ? depth0.charm_name : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'charm_name', hash: {}, data: data})
            : helper)
        ) +
        '" class="tooltip__content"></span>\n                </p>\n            </span>\n        </a>\n    </li>\n'
      );
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        buffer = '<ul class="list__icons clearfix">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.charms : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['event-feed-v1'] = template({
    '1': function(depth0, helpers, partials, data) {
      var helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression;
      return (
        '    <li class="p-list__item">\n      <div class="p-media-object">\n        <img class="p-media-object__image" alt="Location map"\n          src="//maps.googleapis.com/maps/api/staticmap?center=' +
        escapeExpression(
          ((helper =
            (helper = helpers.location || (depth0 != null ? depth0.location : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'location', hash: {}, data: data})
            : helper)
        ) +
        '&amp;zoom=12&amp;size=156x156&amp;sensor=false">\n        <div class="p-media-object__details">\n          <h3 class="p-media-object__title">\n            <a href="' +
        escapeExpression(
          ((helper =
            (helper = helpers.link || (depth0 != null ? depth0.link : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'link', hash: {}, data: data})
            : helper)
        ) +
        '">' +
        escapeExpression(
          ((helper =
            (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'title', hash: {}, data: data})
            : helper)
        ) +
        '</a>\n          </h3>\n          <ul class="p-media-object__meta-list">\n            <li class="p-media-object__meta-list-item--date">\n              <span class="u-off-screen">Date: </span>' +
        escapeExpression(
          ((helper =
            (helper = helpers.dates || (depth0 != null ? depth0.dates : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'dates', hash: {}, data: data})
            : helper)
        ) +
        '\n              <span class="u-off-screen">\n                  <time datetime="' +
        escapeExpression(
          ((helper =
            (helper = helpers.start_date || (depth0 != null ? depth0.start_date : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'start_date', hash: {}, data: data})
            : helper)
        ) +
        '"\n                      itemprop="startDate"></time>\n                  <time datetime="' +
        escapeExpression(
          ((helper =
            (helper = helpers.end_date || (depth0 != null ? depth0.end_date : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'end_date', hash: {}, data: data})
            : helper)
        ) +
        '"\n                      itemprop="endDate"></time>\n              </span>\n            </li>\n            <li class="p-media-object__meta-list-item--location" itemtype="http://schema.org/PostalAddress"\n                itemscope="" itemprop="location">\n              <span class="u-off-screen">Location: </span>' +
        escapeExpression(
          ((helper =
            (helper = helpers.location || (depth0 != null ? depth0.location : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'location', hash: {}, data: data})
            : helper)
        ) +
        '\n            </li>\n          </ul>\n        </div>\n      </div>\n    </li>\n'
      );
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        buffer = '<ul class="p-list">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.entries : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['event-feed'] = template({
    '1': function(depth0, helpers, partials, data) {
      var helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression;
      return (
        '        <li>\n            <div class="event-details-wrapper clearfix">\n                <h3>\n                    <a href="' +
        escapeExpression(
          ((helper =
            (helper = helpers.link || (depth0 != null ? depth0.link : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'link', hash: {}, data: data})
            : helper)
        ) +
        '" class="external">\n                        ' +
        escapeExpression(
          ((helper =
            (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'title', hash: {}, data: data})
            : helper)
        ) +
        '\n                    </a>\n                </h3>\n                <div class="event-map">\n                    <a href="' +
        escapeExpression(
          ((helper =
            (helper = helpers.link || (depth0 != null ? depth0.link : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'link', hash: {}, data: data})
            : helper)
        ) +
        '">\n                        <img class="avatar" alt="Location map"\n                            src="//maps.googleapis.com/maps/api/staticmap?center=' +
        escapeExpression(
          ((helper =
            (helper = helpers.location || (depth0 != null ? depth0.location : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'location', hash: {}, data: data})
            : helper)
        ) +
        '&amp;zoom=12&amp;size=156x156&amp;sensor=false">\n                    </a>\n                </div>\n                <dl class="event-details">\n                    <dt class="accessibility-aid">Date:</dt>\n                    <dd class="event-date">\n                        ' +
        escapeExpression(
          ((helper =
            (helper = helpers.dates || (depth0 != null ? depth0.dates : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'dates', hash: {}, data: data})
            : helper)
        ) +
        '\n                        <span class="accessibility-aid">\n                            <time datetime="' +
        escapeExpression(
          ((helper =
            (helper = helpers.start_date || (depth0 != null ? depth0.start_date : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'start_date', hash: {}, data: data})
            : helper)
        ) +
        '"\n                                itemprop="startDate"></time>\n                            <time datetime="' +
        escapeExpression(
          ((helper =
            (helper = helpers.end_date || (depth0 != null ? depth0.end_date : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'end_date', hash: {}, data: data})
            : helper)
        ) +
        '"\n                                itemprop="endDate"></time>\n                        </span>\n                    </dd>\n                    <dt class="accessibility-aid">Location:</dt>\n                    <dd class="location" itemtype="http://schema.org/PostalAddress"\n                        itemscope="" itemprop="location">\n                        ' +
        escapeExpression(
          ((helper =
            (helper = helpers.location || (depth0 != null ? depth0.location : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'location', hash: {}, data: data})
            : helper)
        ) +
        '\n                    </dd>\n                </dl>\n            </div>\n        </li>\n'
      );
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        buffer = '\n<ul class="events-list no-bullets">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.entries : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['related-solution'] = template({
    '1': function(depth0, helpers, partials, data) {
      var helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression;
      return (
        '    <li>\n        <a href="' +
        escapeExpression(
          ((helper =
            (helper = helpers.charm_url || (depth0 != null ? depth0.charm_url : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'charm_url', hash: {}, data: data})
            : helper)
        ) +
        '">\n            <span>\n                <p class="tooltip">\n                    <img height="75" width="75" src="' +
        escapeExpression(
          ((helper =
            (helper = helpers.icon_url || (depth0 != null ? depth0.icon_url : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'icon_url', hash: {}, data: data})
            : helper)
        ) +
        '">\n                    <span data-tooltip="' +
        escapeExpression(
          ((helper =
            (helper = helpers.charm_name || (depth0 != null ? depth0.charm_name : depth0)) !=
            null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'charm_name', hash: {}, data: data})
            : helper)
        ) +
        '" class="tooltip__content"></span>\n                </p>\n            </span>\n        </a>\n\n    </li>\n'
      );
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression,
        buffer =
          '<div class="details">\n    <div class="title">\n        ' +
          escapeExpression(
            ((helper =
              (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null
                ? helper
                : helperMissing),
            typeof helper === functionType
              ? helper.call(depth0, {name: 'name', hash: {}, data: data})
              : helper)
          ) +
          '\n    </div>\n    <div class="deploys note">\n        ' +
          escapeExpression(
            ((helper =
              (helper = helpers.deploys || (depth0 != null ? depth0.deploys : depth0)) != null
                ? helper
                : helperMissing),
            typeof helper === functionType
              ? helper.call(depth0, {name: 'deploys', hash: {}, data: data})
              : helper)
          ) +
          ' deploys\n    </div>\n</div>\n<ul class="list__icons clearfix">\n';
      stack1 = helpers.each.call(depth0, depth0 != null ? depth0.charms : depth0, {
        name: 'each',
        hash: {},
        fn: this.program(1, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer + '</ul>\n';
    },
    useData: true
  });
  templates['video-feed'] = template({
    '1': function(depth0, helpers, partials, data) {
      var stack1,
        helper,
        functionType = 'function',
        helperMissing = helpers.helperMissing,
        escapeExpression = this.escapeExpression,
        buffer = '    <div class="four-col ';
      stack1 = helpers['if'].call(depth0, depth0 != null ? depth0.isModLast : depth0, {
        name: 'if',
        hash: {},
        fn: this.program(2, data),
        inverse: this.noop,
        data: data
      });
      if (stack1 != null) {
        buffer += stack1;
      }
      return (
        buffer +
        '">\n        <div class="video-container">\n            <iframe width="329" height="185" src="' +
        escapeExpression(
          ((helper =
            (helper = helpers.video || (depth0 != null ? depth0.video : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'video', hash: {}, data: data})
            : helper)
        ) +
        '" allowfullscreen></iframe>\n        </div>\n        <h3>' +
        escapeExpression(
          ((helper =
            (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null
              ? helper
              : helperMissing),
          typeof helper === functionType
            ? helper.call(depth0, {name: 'title', hash: {}, data: data})
            : helper)
        ) +
        '</h3>\n    </div>\n'
      );
    },
    '2': function(depth0, helpers, partials, data) {
      return 'last-col';
    },
    compiler: [6, '>= 2.0.0-beta.1'],
    main: function(depth0, helpers, partials, data) {
      var stack1,
        helperMissing = helpers.helperMissing,
        buffer = '';
      stack1 = (helpers.everyNth || (depth0 && depth0.everyNth) || helperMissing).call(
        depth0,
        depth0 != null ? depth0.entries : depth0,
        3,
        {
          name: 'everyNth',
          hash: {},
          fn: this.program(1, data),
          inverse: this.noop,
          data: data
        }
      );
      if (stack1 != null) {
        buffer += stack1;
      }
      return buffer;
    },
    useData: true
  });
})();
