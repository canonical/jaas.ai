// import modules
import * as Sentry from '@sentry/browser';
import {createNav} from '@canonical/global-nav';
import {cookiePolicy} from '@canonical/cookie-policy';
import {fetchLatestNews} from '@canonical/latest-news';
import searchPanel from './modules/search-panel';
import showContactDetails from './modules/show-contact-details';
import copySnippet from './modules/copy-snippet';
import modal from './modules/modal';

// Init Sentry JS tracking
Sentry.init({dsn: 'https://5b54e6946be34749935c4dd2d9d01cb8@sentry.is.canonical.com//7'});

// Global nav strip
createNav({maxWidth: '72rem', showLogins: false});

// Contact CTA for /experts
showContactDetails();

// Copy deploy script to clipboard in entity header
copySnippet();

// Display search panel overlay when user clicks in nav search box
searchPanel();

// Show modal windows
modal();

// Pull latest news from blog feed
fetchLatestNews({
  articlesContainerSelector: '#latest-news-container',
  articleTemplateSelector: '#articles-template',
  limit: 2,
  id: 3612,
  hostname: 'ubuntu.com',
});

// Add cookie policy on page load
cookiePolicy();
