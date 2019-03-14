// import modules
import {createNav} from '@canonical/global-nav';
import handleSearch from './modules/header-search';
import showContactDetails from './modules/show-contact-details';
import copySnippet from './modules/copy-snippet';

// Instantiate modules
createNav({maxWidth: '64.875rem', showLogins: false});
showContactDetails();
copySnippet();
handleSearch();
