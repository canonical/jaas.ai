import {fetchLatestNews} from '@canonical/latest-news';

// Pull latest news from blog feed
fetchLatestNews({
  articlesContainerSelector: '#latest-news-container',
  articleTemplateSelector: '#articles-template',
  limit: 2,
  tagId: 1286,
  hostname: 'ubuntu.com',
});
