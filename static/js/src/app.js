// import modules
import * as Sentry from '@sentry/browser';
import {createNav} from '@canonical/global-nav';
import {cookiePolicy} from '@canonical/cookie-policy';

// Init Sentry JS tracking
Sentry.init({dsn: 'https://5b54e6946be34749935c4dd2d9d01cb8@sentry.is.canonical.com//7'});

// Global nav strip
createNav({maxWidth: '72rem', showLogins: false, hiring: 'https://juju.is/careers'});

// Add cookie policy on page load
cookiePolicy();
