/**
  Allows users to click button on code snippet pattern to copy contents to clipboard
* */
const copySnippet = () => {
  /**
    Copies string to clipboard
    @method copySnippet.copyToClipboard
    @param str {String} String to be copied to clipboard
    @static
  * */
  const copyToClipboard = (str) => {
    const el = document.createElement('textarea'); // Create a <textarea> element
    el.value = str; // Set its value to the string that you want copied
    el.setAttribute('readonly', ''); // Make it readonly to be tamper-proof
    el.style.position = 'absolute';
    el.style.left = '-9999px'; // Move outside the screen to make it invisible
    document.body.appendChild(el); // Append the <textarea> element to the HTML document
    const selected =
      document.getSelection().rangeCount > 0 // Check if there is any content selected previously
        ? document.getSelection().getRangeAt(0) // Store selection if found
        : false; // Mark as false to know no selection existed before
    el.select(); // Select the <textarea> content
    document.execCommand('copy'); // Copy - only works as a result of a user action (e.g. click events)
    document.body.removeChild(el); // Remove the <textarea> element
    if (selected) {
      // If a selection existed before copying
      document.getSelection().removeAllRanges(); // Unselect everything on the HTML document
      document.getSelection().addRange(selected); // Restore the original selection
    }
  };

  /**
    Activate copy button on code snippets
    @method copySnippet.instantiateCopyButtons
    @static
  * */
  const instantiateCopyButtons = () => {
    const codeSnippetActions = document.querySelectorAll('.p-code-copyable__action');
    codeSnippetActions.forEach((codeSnippetAction) => {
      codeSnippetAction.addEventListener(
        'click',
        () => {
          const clipboardValue = codeSnippetAction.previousElementSibling.getAttribute(
            'value'
          );
          copyToClipboard(clipboardValue);
        },
        false
      );
    });
  };

  // Check to ensure code snippet elements exist on the page
  const codeSnippets = document.querySelectorAll('p-code-snippet');
  // If so, instantiate.
  if (codeSnippets) {
    instantiateCopyButtons();
  }
};

export default copySnippet;
