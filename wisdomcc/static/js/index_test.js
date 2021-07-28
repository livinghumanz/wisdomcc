/* Toggle between adding and removing the "responsive" class to the navbar when the user clicks on the icon */
function myFunction() {
  var x = document.getElementById("nav");
  var foo = document.getElementById("footer");
  if (x.className == "wnavbar") {
    x.className += " responsive";
    foo.style.display='none';
  } else {
    x.className = "wnavbar";
    foo.style.display='block';
  }
} 

/*********** Login modal popup js ******************/
function loginpop() { 
  $('#loginModal').modal('show');
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
}
function admisionpop() { 
  $('#admisionModal').modal('show');
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
}