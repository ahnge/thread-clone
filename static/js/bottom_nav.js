document.body.addEventListener("htmx:beforeRequest", function (evt) {
  const myTabs = document.getElementsByClassName("mytab");
  for (let tab of myTabs) {
    tab.classList.remove("text-black");
    tab.classList.add("text-gray-400");
  }
  evt.detail.requestConfig.elt.classList.remove("text-gray-400");
  evt.detail.requestConfig.elt.classList.add("text-black");
});
