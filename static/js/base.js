var replyActions = htmx.findAll(".reply-action");

[...replyActions].forEach((ra) => {
  ra.addEventListener("click", () => {
    htmx.removeClass(htmx.find("#reply-popup"), "top-full");
    htmx.addClass(htmx.find("#reply-popup"), "top-5");
  });
});

// Slide down new reply
htmx.find("#reply-close").addEventListener("click", () => {
  htmx.removeClass(htmx.find("#reply-popup"), "top-5");
  htmx.addClass(htmx.find("#reply-popup"), "top-full");
});

htmx.find("#container").addEventListener("htmx:afterSwap", () => {
  var replyActions = htmx.findAll(".reply-action");

  [...replyActions].forEach((ra) => {
    ra.addEventListener("click", () => {
      htmx.removeClass(htmx.find("#reply-popup"), "top-full");
      htmx.addClass(htmx.find("#reply-popup"), "top-5");
    });
  });
});
