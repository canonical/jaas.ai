function renderFeed(selector) {
  const container = document.querySelector(selector);
  if (container) {
    const feed = JSON.parse(this.responseText);
    const posts = feed.map(
      (post) => `
      <li class="p-list__item">
        <h4 class="u-no-margin--bottom">
          <a href="${post.links[0].href}">${post.title_detail.value}</a>
        </h4>
        <h6>${new Date(post.published).toISOString().slice(0, 10)} by ${post.author}</h6>
        <p>
          ${post.summary_detail.value}
        </p>
      </li>
    `
    );
    container.innerHTML = `<ul class="p-list">${posts.join('')}</ul>`;
  }
}

function loadFeed(url, selector) {
  const request = new XMLHttpRequest();
  request.addEventListener('load', renderFeed.bind(request, selector));
  request.open('GET', url);
  request.send();
}

loadFeed('/blog/feed', '#blog-feed');
