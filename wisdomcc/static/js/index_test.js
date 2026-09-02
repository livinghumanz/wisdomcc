/* Mobile nav toggle. The old version looked up a #footer element that did not
   exist and threw before opening the menu; the footer now carries that id. */
function myFunction() {
  var nav = document.getElementById("nav");
  var toggle = document.querySelector(".nav-toggle");
  if (!nav) { return; }
  var open = nav.classList.toggle("is-open");
  if (toggle) { toggle.setAttribute("aria-expanded", open ? "true" : "false"); }
}

/*********** Modal popups ******************/
function loginpop() {
  $('#loginModal').modal('show');
}

function admisionpop() {
  $('#admisionModal').modal('show');
}

/* Close the mobile menu after following a link inside it. */
document.addEventListener("DOMContentLoaded", function () {
  var nav = document.getElementById("nav");
  if (!nav) { return; }
  nav.addEventListener("click", function (event) {
    if (event.target.tagName === "A") { nav.classList.remove("is-open"); }
  });
});
