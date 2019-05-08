// import modules
import {createNav} from '@canonical/global-nav';
import {cookiePolicy} from '@canonical/cookie-policy';
import searchPanel from './modules/search-panel';
import showContactDetails from './modules/show-contact-details';
import copySnippet from './modules/copy-snippet';

// Global nav strip
createNav({maxWidth: '72rem', showLogins: false});

// Contact CTA for /experts
showContactDetails();

// Copy deploy script to clipboard in entity header
copySnippet();

// Display search panel overlay when user clicks in nav search box
searchPanel();

// Add cookie policy on page load
const cookiePolicyOptions = {
  content: `We use cookies to improve your experience. By your continued use of this site you accept such use. To change your settings please <a href="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy#cookies">see our policy.</a>`,
  duration: 5000
};
cookiePolicy(cookiePolicyOptions);
