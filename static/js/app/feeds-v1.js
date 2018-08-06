/**
  Fetch (asynchronously) the blog feed and display the specified number of
  items in a nicely-formatted manner.

  @param {String} selector the ID of the blog container
  @param {Integer} numberOfItems the number of blog entries to display;
      defaults to 5
*/
window.Jujucharms.fetchBlogFeed = function(selector, numberOfItems) {
  numberOfItems = numberOfItems || 5;
  var request = new XMLHttpRequest(),
    feedURL = '/community/blog/feed',
    container = document.querySelector(selector);

  if (container) {
    request.open('GET', feedURL, true);
    request.onreadystatechange = function() {
      if (request.readyState === 4 && request.status === 200) {
        var feed = JSON.parse(request.responseText);
        var data = { entries: feed.entries.slice(0, numberOfItems) };
        container.innerHTML = Handlebars.templates['blog-feed-v1'](data);
      }
    };
    request.send();
  }
};

/**
  Fetch (asynchronously) the video feed and display the specified number of
  items in a nicely-formatted manner.

  @param {String} selector the id or class of the video container.
  @param {Integer} numberOfItems the number of video entries to display;
      defaults to 5.
*/
window.Jujucharms.fetchVideosFeed = function(selector, numberOfItems) {
  numberOfItems = numberOfItems || 5;
  var request = new XMLHttpRequest(),
    feedURL = '/videos/feed/' + numberOfItems,
    container = document.querySelector(selector);

  if (container) {
    request.open('GET', feedURL, true);
    request.onreadystatechange = function() {
      if (request.readyState === 4 && request.status === 200) {
        var feed = JSON.parse(request.responseText);
        container.innerHTML = Handlebars.templates['video-feed'](feed);
      }
    };
    request.send();
  }
};

/**
  Fetch (asynchronously) the event feed and display the specified number of
  items in a nicely-formatted manner.
  @param {String} selector the id or class of the event container.
  @param {Integer} numberOfItems the number of event entries to display;
      defaults to 5.
*/
window.Jujucharms.fetchEventsFeed = function(selector, numberOfItems) {
  numberOfItems = numberOfItems || 3;
  var request = new XMLHttpRequest(),
    feedURL = '/events/feed/' + numberOfItems,
    container = document.querySelector(selector);

  if (container) {
    request.open('GET', feedURL, true);
    request.onreadystatechange = function() {
      if (request.readyState === 4 && request.status === 200) {
        var feed = JSON.parse(request.responseText);
        container.innerHTML = Handlebars.templates['event-feed-v1'](feed);
      }
    };
    request.send();
  }
};
