/**
  Allows users to click button on code snippet pattern to copy contents to clipboard
**/
const copySnippet = () => {
  /**
    Activate copy button on code snippets
    @method copyCodeSnippets.instantiateCopyButtons
    @static
  **/
  const instantiateCopyButtons = () => {
    var codeSnippetActions = document.querySelectorAll('.p-code-copyable__action');
    for (var codeSnippetAction of codeSnippetActions) {
      codeSnippetAction.addEventListener(
        'click',
        function () {
          const clipboardValue = this.previousSibling.previousSibling.value;
          copyToClipboard(clipboardValue);
        },
        false
      );
    }
  };

  /**
    Copies string to clipboard
    @method copyCodeSnippets.copyToClipboard
    @param str {String} String to be copied to clipboard
    @static
  **/
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

  // Check to ensure code snippet elements exist on the page
  const codeSnippets = document.querySelectorAll('p-code-snippet');
  // If so, instantiate.
  if (codeSnippets) {
    instantiateCopyButtons();
  }
};

export default copySnippet;
