
  function showform(dowhat) {
    /*
    * 1 - Citation for this function:
    * 2 - Date: 10/01/2024
    * 3 - Adapted from the starter code.
    * 4 - Copied and used this starter code as a starting point
    *     for my project. 
    * 
    *     Changed the names of the individual entities
    *     to a generic 'Entry' to make my templating design easier.
    * 
    *     Modified the deleteEntry() function to serve as a 
    *     confirmation window.
    * 
    *     The rest is basically the same as the starter code, 
    *     it is used to reveal forms in my table pages that are
    *     initially hidden.
    * 
    * 5 - Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master/bsg_people_app
    * 
    * four DIVS: browse, insert, update, delete
    * this function sets one visible the others not
    */
    if (dowhat == 'insert'){
      document.getElementById('browse').style.display = 'none';
      document.getElementById('insert').style.display = 'block';
      document.getElementById('update').style.display = 'none';
      document.getElementById('delete').style.display = 'none';
    }
    else if (dowhat == 'update'){
      document.getElementById('browse').style.display = 'none';
      document.getElementById('insert').style.display = 'none';
      document.getElementById('update').style.display = 'block';
      document.getElementById('delete').style.display = 'none';
    }
    else if (dowhat == 'delete'){
      document.getElementById('browse').style.display = 'none';
      document.getElementById('insert').style.display = 'none';
      document.getElementById('update').style.display = 'none';
      document.getElementById('delete').style.display = 'block';
    }
    else if (dowhat == 'all'){
      document.getElementById('browse').style.display = 'block';
      document.getElementById('insert').style.display = 'block';
      document.getElementById('update').style.display = 'block';
      document.getElementById('delete').style.display = 'block';
    }
    else { //by default display browse
      document.getElementById('browse').style.display = 'block';
      document.getElementById('insert').style.display = 'none';
      document.getElementById('update').style.display = 'none';
      document.getElementById('delete').style.display = 'none';
    }
  }
  function newEntry() { showform('insert'); }
  function updateEntry(pid) { showform('update'); }

  // DELETE CONFIRM WINDOW
  function deleteEntry(itemId, itemName) { 
    if (confirm(`Are you sure you want to delete: ${itemName}?`)) {
      window.location.href = `/delete_{{obj_name}}/${itemId}`;
    }
  }

  function browseEntries() { showform ('browse'); }
  function showAll() { showform ('all'); }


