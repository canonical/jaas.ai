// import modules
import {createNav} from '@canonical/global-nav';
import searchPanel from './modules/search-panel';
import showContactDetails from './modules/show-contact-details';
import copySnippet from './modules/copy-snippet';

// Instantiate modules
createNav({maxWidth: '72rem', showLogins: false});
showContactDetails();
copySnippet();
searchPanel();
