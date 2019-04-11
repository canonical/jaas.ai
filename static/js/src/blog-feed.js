function renderFeed() {
  const container = document.querySelector('#blog-feed');
  if (container) {
    const feed = JSON.parse(this.responseText);
    let posts = feed.map(post => {
      const posted = new Date(post.published);
      const month = `0${posted.getMonth() + 1}`.slice(-2);
      const day = `0${posted.getDate()}`.slice(-2);
      return `
        <li class="p-list__item">
          <h4 class="u-no-margin--bottom">
            <a href="${post.links[0].href}">${post.title_detail.value}</a>
          </h4>
          <h6>${posted.getFullYear()}-${month}-${day} by ${post.author}</h6>
          <p>
            ${post.summary_detail.value}
          </p>
        </li>
      `;
    });
    container.innerHTML = `<ul class="p-list">${posts.join('')}</ul>`;
  }
};
const request = new XMLHttpRequest();
request.addEventListener("load", renderFeed);
request.open("GET", "/blog/feed");
request.send();
