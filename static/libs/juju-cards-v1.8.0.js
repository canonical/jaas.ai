// Allow the user of the cards to customize the install URL to their own
// controller using the data-demoDomain attribute on the script tag
// embedding the juju-cards.js script.
const customDemoDomain = document.currentScript.getAttribute("data-demodomain");
let demoDomain = "https://jujucharms.com/new";
if (customDemoDomain) {
  demoDomain = customDemoDomain + "/new";
}

let jujuCards = demoDomain => {
  let targetClass = "juju-card";
  let siteDomain = "https://jaas.ai";
  let apiAddress = "https://api.jujucharms.com/charmstore/v5/";
  let apiIncludes = "?include=id-name" + "&include=id" + "&include=owner" + "&include=stats" + "&include=id-series" + "&include=promulgated";
  let copyIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">' + '<path d="M4.85 11.15l6.3-6.3" overflow="visible" fill="none" stroke="gray" stroke-width="1.463"/>' + '<path d="M12.152 0a1.984 1.984 0 0 0-.33.04c-.867.173-1.42.78-1.898 1.26L8.487 2.738c-.48.48-1.087 1.03-1.26 1.898-.075.37-.044.76.096 1.167l1.77-1.77c.102-.113.215-.23.337-.352l1.437-1.435c.48-.48.886-.83 1.217-.896a.877.877 0 0 1 .277-.01c.313.034.738.245 1.398.905.88.88.96 1.342.895 1.673-.066.33-.417.736-.896 1.216L12.32 6.57c-.124.123-.242.237-.356.34l-1.767 1.77c.407.14.797.17 1.168.096.867-.173 1.42-.78 1.898-1.26l1.437-1.44c.48-.48 1.087-1.03 1.26-1.898.174-.867-.223-1.84-1.26-2.878C13.923.522 13.18.105 12.492.017a2.125 2.125 0 0 0-.34-.016zM4.965 7.19a1.984 1.984 0 0 0-.33.038c-.867.174-1.42.782-1.898 1.26L1.3 9.925c-.48.48-1.087 1.03-1.26 1.898-.174.868.223 1.842 1.26 2.88 1.037 1.035 2.01 1.432 2.878 1.26.867-.175 1.42-.783 1.898-1.262l1.437-1.436c.48-.48 1.087-1.03 1.26-1.898.075-.37.044-.76-.096-1.168l-1.765 1.765c-.104.114-.218.233-.342.357l-1.437 1.437c-.48.48-.886.83-1.217.895-.33.066-.793-.016-1.673-.895-.88-.88-.96-1.343-.895-1.673.066-.33.417-.737.896-1.216L3.68 9.43c.124-.122.24-.236.355-.34l1.767-1.767a2.498 2.498 0 0 0-.497-.12 2.125 2.125 0 0 0-.34-.015z" fill="gray"/>' + "</svg>";

  let cards = document.querySelectorAll("." + targetClass);

  // getLink
  // Get the button link
  const getLink = (domain, id, dd) => {
    let addLink = `${domain}/?deploy-target=${id}`;

    if (dd !== undefined) {
      addLink = `${domain}/?dd=${id}`;
    }

    return addLink;
  };

  // getButtonText
  // Get the button text
  const getButtonText = (domain, id, dd) => {
    let deployTitle = "Deploy with Juju";

    if (dd !== undefined) {
      deployTitle = "Deploy with JAAS";
    }

    return deployTitle;
  };

  // getData
  // Concatenates the api url and fetches it
  let getData = (card, id) => {
    let apiUrl = `${apiAddress}${id}/meta/any${apiIncludes}`;
    get(apiUrl, function (response) {
      if (!response.Message) {
        detectType(card, response);
      } else {
        reportError(card, response.Message);
      }
    }, card, id);
  };

  // detectType
  // Checks if the element is a bundle or charm and renders the correct function
  let detectType = (card, data) => {
    if (data.Meta["id-series"].Series === "bundle") {
      renderBundle(card, data);
    } else {
      renderCharm(card, data);
    }
  };

  // renderBundle
  // Split out required data and insert card markup
  let renderBundle = (card, data) => {
    let name = data.Meta["id-name"].Name;
    let id = data.Id;
    let series = data.Meta["id-series"].Series;
    let revision = data.Meta.id.Revision;
    let owner = data.Meta.owner.User;
    let ownerLink = `${siteDomain}/u/${owner}`;
    let promulgated = data.Meta.promulgated.Promulgated;
    let detailsLink = "";
    let image = `${apiAddress}bundle/${name}-${revision}/diagram.svg`;
    if (promulgated) {
      detailsLink = `${siteDomain}/${name}`;
    } else {
      detailsLink = `${ownerLink}/${name}`;
      image = `${apiAddress}~${owner}/bundle/${name}-${revision}/diagram.svg`;
    }

    const addLink = getLink(demoDomain, getImageID(id), card.dataset.dd);
    const deployTitle = getButtonText(demoDomain, getImageID(id), card.dataset.dd);

    let dom = `<div class="juju-card__container bundle-card">` + `<a href="${detailsLink}" class="bundle-card__link">View details</a>` + `<header class="bundle-card__header">` + `<div class="bundle-card__image-container">` + `<object wmode="transparent" width="100%" class="bundle-card__bundle-image" type="image/svg+xml" data="${image}"></object>` + `</div>` + `</header>` + `<main class="bundle-card__main">` + `<div class="bundle-card__meta">` + `<h1 class="bundle-card__title">${name}</h1>` + `<p class="bundle-card__by">by ${owner}</h1>` + `</div>` + `<ul class="bundle-card__actions">` + `<li class="bundle-card__actions-item--details">` + `<label class="bundle-card__actions-label" for="cli-deploy">Deploy with the CLI:</label>` + `<div class="bundle-card__actions-command">` + `<input class="bundle-card__actions-field js-clipboard-input" readonly="readonly" value="juju deploy ${id}" onclick="this.select();" id="cli-deploy">` + `<button class="bundle-card__actions-copy-to-clipboard js-copy-to-clipboard" onclick="jujuCards.copyToClipboard(this.parentElement);" title="Copy to clipboard">${copyIcon}</button>` + `</div>` + `</li>` + `</ul>` + `</main>` + `<footer class="bundle-card__footer">` + `<a href="http://jujucharms.com"><img src="https://assets.ubuntu.com/v1/7e21b535-logo-juju.svg" alt="" class="bundle-card__footer-logo" /></a>` + `<p class="bundle-card__footer-note">&copy; <a href="http://www.canonical.com">Canonical Ltd</a>.</p>` + `</footer>` + `</div>`;

    card.innerHTML = dom;
    card.classList.add("juju-card--rendered");
    card.classList.add(getWidthClass(card));
  };

  // renderCharm
  // Split out required data and insert card markup
  let renderCharm = (card, data) => {
    let name = data.Meta["id-name"].Name;
    let id = data.Id;
    let image = `${apiAddress}${getImageID(id)}/icon.svg`;
    let deploys = prettyPrintNumber(data.Meta.stats.ArchiveDownloadCount);
    let series = data.Meta["id-series"].Series;
    let revision = data.Meta.id.Revision;
    let owner = data.Meta.owner.User;
    let promulgated = data.Meta.promulgated.Promulgated;
    let ownerLink = `${siteDomain}/u/${owner}`;
    let detailsLink = "";
    if (promulgated) {
      detailsLink = `${siteDomain}/${name}`;
    } else {
      detailsLink = `${ownerLink}/${name}`;
    }
    const addLink = getLink(demoDomain, getImageID(id), card.dataset.dd);
    const deployTitle = getButtonText(demoDomain, getImageID(id), card.dataset.dd);

    let seriesEle = ``;
    if (series) {
      seriesEle = `<li class="charm-card__meta-item--series">${series}</li>`;
    }

    let dom = `<div class="juju-card__container charm-card">` + `<a href="${detailsLink}" class="charm-card__link">View details</a>` + `<header class="charm-card__header">` + `<img src="${image}" alt="${name}" class="charm-card__image" />` + `<h1 class="charm-card__title">${name}</h1>` + `<ul class="charm-card__meta">` + `<li class="charm-card__meta-item--by">by ${owner}</li>` + `${seriesEle}` + `</ul>` + `</header>` + `<main class="charm-card__main">` + `<ul class="charm-card__actions">` + `<li class="charm-card__actions-item--details">` + `<label class="charm-card__actions-label" for="cli-deploy">Deploy with the CLI:</label>` + `<div class="charm-card__actions-command">` + `<input class="charm-card__actions-field js-clipboard-input" readonly="readonly" value="juju deploy ${id}" onclick="this.select();" id="cli-deploy">` + `<button class="charm-card__actions-copy-to-clipboard js-copy-to-clipboard" onclick="jujuCards.copyToClipboard(this);" title="Copy to clipboard">${copyIcon}</button>` + `</div>` + `</li>` + `</ul>` + `</main>` + `<footer class="charm-card__footer">` + `<a href="http://jujucharms.com"><img src="https://assets.ubuntu.com/v1/7e21b535-logo-juju.svg" alt="" class="charm-card__footer-logo" /></a>` + `<p class="charm-card__footer-note">&copy; <a href="http://www.canonical.com">Canonical Ltd</a>.</p>` + `</footer>` + `</div>`;

    card.innerHTML = dom;
    card.classList.add("juju-card--rendered");
    card.classList.add(getWidthClass(card));
  };

  // getWidthClass
  // Checks the width of the card container and returns the correct class to
  // attach element queries
  let getWidthClass = el => {
    let width = el.offsetWidth;
    let queryClass = "juju-card--small";
    if (width > 301) {
      queryClass = "juju-card--medium";
    }
    if (width > 626) {
      queryClass = "juju-card--large";
    }
    return queryClass;
  };

  let reportError = (card, message) => {
    let dom = `<div class="juju-card__error">` + `<p class="juju-card__error-message">${message}</p>` + `</div>`;

    card.innerHTML = dom;
    card.classList.add("juju-card--rendered");
  };

  // prettyPrintNumber
  // Takes a number and returns string with commas in the correct places.
  // For example: 3000 => 3,000
  let prettyPrintNumber = x => x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  // getImageID
  // Take a charm ID and removes ''cs:' then returns the remainer to create the
  // image URL.
  let getImageID = id => id.toString().replace("cs:", "");

  // get
  // Wraps a XMLHttpRequest in a promise.
  let get = (url, callback, card, id) => {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function () {
      if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
          var data = JSON.parse(httpRequest.responseText);
          if (callback) callback(data);
        } else {
          reportError(card, "No charm or bundle found for " + id);
        }
      } else {
        reportError(card, "No charm or bundle found for " + id);
      }
    };
    httpRequest.open("GET", url);
    httpRequest.send();
  };

  Array.prototype.slice.call(cards).forEach(function (card) {
    let id = card.dataset.id;
    if (id == undefined || id == "") {
      console.warn("Card found with no ID");
    } else {
      getData(card, id);
    }
  });
};

// updateHead
// Add the required stylesheet and font to the page head
jujuCards.updateHead = () => {
  let filePath = "";
  // TODO: make this a full regex pattern for js/juju-embed.js$
  //       then use it with the .replace
  let pattern = /juju-cards-v[0-9]+.[0-9]+.[0-9]+\.js$/i;

  Array.prototype.slice.call(document.getElementsByTagName("script")).forEach(function (script) {
    if (pattern.test(script.getAttribute("src"))) {
      filePath = script.getAttribute("src").replace(".js", "").replace("js/", "");
    }
  });

  // Load the card stylesheet
  let css = document.createElement("link");
  css.rel = "stylesheet";
  css.type = "text/css";
  css.href = `${filePath}.css`;
  css.media = "all";
  document.getElementsByTagName("head")[0].appendChild(css);
};

jujuCards.copyToClipboard = function (item) {
  let commandInput = item.parentElement.getElementsByTagName("input")[0];
  if (commandInput) {
    commandInput.select();
    try {
      document.execCommand("copy");
    } catch (err) {
      console.log("Unable to copy");
    }
  }
};

if (window.onload && typeof window.onload === "function") {
  jujuCards.onload = window.onload;
}

window.onload = function () {
  if (jujuCards.onload) {
    jujuCards.onload();
  }
  jujuCards(demoDomain);
  jujuCards.updateHead();
};