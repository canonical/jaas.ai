/**
  Initialize the typer
  @param {HTMLElement} container The main container to type in
  @param {HTMLElement} commentContainer the container to add comments
*/
window.app.cliTyper = function (container, commentContainer) {
  const cli = [
    'juju clouds',
    'juju add-credential aws-personal',
    'juju add-credential aws-work',
    'juju bootstrap aws',
    'juju status',
    'juju deploy mariadb',
    'juju deploy mariadb --constraints cores=8 mem=16G',
    'juju config mariadb dataset-size=80%',
    'juju add-model prod-california us-west-1',
    'juju add-model prod-tokyo ap-northeast-1',
    'juju list-models',
    'juju deploy jenkins',
    'juju deploy',
    'juju deploy jenkins-slave',
    'juju relate jenkins jenkins-slave',
    'juju add-unit jenkins-slave -n 3',
    'juju add-user sarah',
    'juju grant sarah read prod-california',
    'juju add-cloud mystack mystack-config.yaml',
  ];

  // For future decorations of the CLI
  const comments = [
    'Choose a cloud to work with',
    'Juju manages multiple cloud credentials',
    false,
    "Let's set up a controller on a public cloud",
    "What's happening?",
    'Juju deploys applications with a single command',
    'Need more power?',
    'Tune the application',
    'Build and manage many models',
    false,
    false,
    'Want continuous integration?',
    false,
    false,
    'Configure your applications to work together. Juju charms handle connections',
    'Increased demand? Bring up 3 more nodes...',
    'Juju is multi-user',
    false,
    'Use your own private cloud - including OpenStack',
  ];

  const RESET_SPEED = 1000;
  const BASE_SPEED = 50;
  const SPEED_MODIFIER = 100;
  const DELETE_PAUSE = 250;
  const NEXT_PAUSE = 2000;

  const cliEle = container;
  const commentEle = commentContainer;
  let current = '';

  /**
    Get the difference between two strings

    @param {String} orig The source string
    @param {String} next The target string
  */
  function getDiff(orig, next) {
    let changes = [];
    let matchTo = 0;
    const toAdd = [];
    let i = 0;

    for (i = orig.length; i > -1; i -= 1) {
      if (next[i] !== orig[i]) {
        matchTo = i;
      }
    }

    if (matchTo > 0) {
      for (i = 0; i < orig.length - matchTo; i += 1) {
        changes.push(-1);
      }
      changes.push(DELETE_PAUSE);
    }

    i = matchTo;
    for (let ii = next.length; i < ii; i += 1) {
      toAdd.push(next[i]);
    }

    changes = changes.concat(toAdd);

    changes.push(NEXT_PAUSE);

    return changes;
  }

  /**
    Add a comment based on the decorator

    @param {Boolean} hide whether the element should be hidden
    @param {HTMLElement} _comment the string to display
    @param {Function} cb Callback if waiting for transition
  */
  function comment(hide, _comment, cb) {
    if (!hide) {
      commentEle.innerHTML = _comment;
      commentEle.classList.add('fade-in');
    } else {
      commentEle.classList.remove('fade-in');
    }

    setTimeout(cb, 500);
  }

  /**
    Type out all the changes in order with delays and randomness
    to simulate someone typing.

    @param {Array} changes The change list (get's modified)
    @param {Array} original The original change list
  */
  function typeIt(changes, original) {
    const change = changes.shift();
    let speed = BASE_SPEED + Math.ceil(Math.random() * SPEED_MODIFIER);
    let currentText = current;
    if (typeof change === 'string' && change.indexOf('#') === 0) {
      comment(true, false, function () {
        comment(false, change.substr(1));
      });
    } else if (change === -1) {
      currentText = currentText.substr(0, current.length - 1);
      speed = BASE_SPEED;
    } else if (typeof change === 'number' && change >= 0) {
      speed = change;
    } else {
      currentText += change;
    }

    const html = `<span>${  currentText.split(' ').join('</span> <span>')  }</span>`;

    current = currentText;

    cliEle.innerHTML = html;

    const next = (function () {
      const _changes = changes;

      return function () {
        typeIt(_changes, original);
      };
    })();

    if (changes.length > 0) {
      setTimeout(next, speed);
    } else {
      typeIt(original.slice(0), original);
    }
  }

  /**
    Get the changes in an array.

    @param {Array} arr the array
    @param {Boolean} resetAtEnd Start again?
  */
  function changesInArray(arr, resetAtEnd) {
    const changes = [];
    let i;
    let current;
    let previous;

    for (i = 0, ii = arr.length; i < ii; i += 1) {
      current = arr[i];
      previous = arr[i - 1] || '';

      changes.push(getDiff(previous, current));
    }

    if (resetAtEnd) {
      const reset = [];
      for (i = 0, ii = current.length; i < ii; i += 1) {
        reset.push(-1);
      }
      reset.push(RESET_SPEED);
      changes.push(reset);
    }

    return changes;
  }

  /**
    Flatten a multidimensional array

    @param {Array} arr the original array
  */
  function flattenArray(arr) {
    let newArr = [];

    for (let i = 0, ii = arr.length; i < ii; i += 1) {
      newArr = newArr.concat(arr[i]);
    }

    return newArr;
  }

  const changeList = changesInArray(cli, true);

  // Decorate with comments
  for (var i = 0, ii = changeList.length; i < ii; i += 1) {
    if (comments[i]) {
      changeList[i].unshift(`#${  comments[i]}`);
    }
  }

  const changes = flattenArray(changeList);
  typeIt(changes.slice(0), changes);
};
