/**
  Converts a DOM list by splitting the text by '/' into a nested tree list.
**/
window.app.treeifyFileList = () => {
  /**
    Loop through the list a files passing the file title and children.
    Skipping the rootAttribute object.

    @method treeifyFileList.addList
    @param folderContents {Object} Object representation of a file path
    @static
  **/
  function addList(folderContents) {
    for (var key in folderContents) {
      if (key !== rootAttribute) {
        addItem(key, folderContents[key]);
      }
    }
  }

  var files = {},
    DOMList = document.querySelector('#files .p-list-tree'),
    rootAttribute = '_root',
    renderedList = '',
    fileUrl = '';

  if (DOMList) {
    fileUrl = DOMList.querySelector('a').href;
    fileUrl = fileUrl.substr(0, fileUrl.indexOf('/archive/') + 9);

    DOMList.querySelectorAll('li').forEach((e) => parsePath(e.innerText.trim()));
    addList(files);
    DOMList.innerHTML = renderedList;

    var listTreeToggle = document.querySelectorAll('.p-list-tree__toggle');
    for (var i = 0; i < listTreeToggle.length; i++) {
      listTreeToggle[i].addEventListener('click', function (e) {
        e.preventDefault();
        var listTree = this.nextElementSibling;
        var expand = this.getAttribute('aria-expanded') === 'true' ? false : true;
        this.setAttribute('aria-expanded', expand);
        listTree.setAttribute('aria-hidden', !expand);
      });
    }
  }

  /**
    Splits a path string by '/' into a multidimensional object.

    @method treeifyFileList.parsePath
    @param fileURL {String} Path string
    @static
  **/
  function parsePath(fileURL) {
    var cur = files;
    fileURL.split('/').forEach(function (node) {
      cur[node] = cur[node] || {};
      cur[node][rootAttribute] = fileURL;
      cur = cur[node];
    });
  }

  /**
    Appends the appoporiate markup based on a node or leaf element.

    @method treeifyFileList.addItem
    @param key {String} node title
    @param folder {Object} nodes object
    @static
  **/
  function addItem(key, folder) {
    if (isEmpty(folder)) {
      renderedList += '<li class="p-list-tree__item">';
      renderedList +=
        '<a href="' + fileUrl + folder[rootAttribute] + '" target="_blank">' + key + '</a>';
      renderedList += '</li>';
    } else {
      renderedList +=
        '<li class="p-list-tree__item p-list-tree__item--group"><button class="p-list-tree__toggle" role="tab" aria-controls="sub-1" aria-expanded="false">/' +
        key +
        '</button>';
      renderedList += '<ul class="p-list-tree"></li>';
      addList(folder);
      renderedList += '</ul>';
    }
  }

  /**
    Tests the passed object for contents other then a path object.

    @method treeifyFileList.isEmpty
    @param obj {Object} test object for emptyness
    @static
  **/
  function isEmpty(obj) {
    for (var prop in obj) {
      if (prop !== rootAttribute && obj.hasOwnProperty(prop)) {
        return false;
      }
    }
    return true;
  }
};
