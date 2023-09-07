var copyToClipBoards = htmx.findAll(".copy-to-clipboard");

const showNoti = () => {
  htmx.find(".ctcb").classList.remove("-top-full");
  htmx.find(".ctcb").classList.add("top-4");
  setTimeout(() => {
    htmx.find(".ctcb").classList.remove("top-4");
    htmx.find(".ctcb").classList.remove("-top-full");
  }, 3000);
};

[...copyToClipBoards].forEach((ctcp) => {
  ctcp.addEventListener("click", showNoti);
});

document.addEventListener("htmx:afterSwap", () => {
  var copyToClipBoards = htmx.findAll(".copy-to-clipboard");
  [...copyToClipBoards].forEach((ctcp) => {
    ctcp.removeEventListener("click", showNoti);
  });
  [...copyToClipBoards].forEach((ctcp) => {
    ctcp.addEventListener("click", showNoti);
  });
});
