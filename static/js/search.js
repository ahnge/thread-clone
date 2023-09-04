const search = htmx.find("#search");

search.addEventListener("htmx:beforeRequest", () => {
  htmx.find("#search-results").innerHTML = "";
});
