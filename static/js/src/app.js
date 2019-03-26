// import modules
import {createNav} from '@canonical/global-nav';
import showContactDetails from './modules/show-contact-details';
import copySnippet from './modules/copy-snippet';
import lazyLoadImages from './modules/lazy-load-images';

// Instantiate modules
createNav({maxWidth: '64.875rem', showLogins: false});
showContactDetails();
copySnippet();
lazyLoadImages();
