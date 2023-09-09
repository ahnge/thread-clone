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

htmx.find("#container").addEventListener("htmx:afterSwap", (evt) => {
  var replyActions = htmx.findAll(".reply-action");
  if (htmx.find("#container") == evt.detail.target) {
    window.scrollTo(0, 0);
  }

  [...replyActions].forEach((ra) => {
    ra.addEventListener("click", () => {
      htmx.removeClass(htmx.find("#reply-popup"), "top-full");
      htmx.addClass(htmx.find("#reply-popup"), "top-5");
    });
  });
});

// clear likes-users-container before another request
htmx.find("#likes_modal").addEventListener("close", (e) => {
  htmx.find("#likes-users-container").innerHTML = "";
});

// Clear reddot if noti page is hit
htmx.find("#notification-tab").addEventListener("click", () => {
  htmx.find("#reddot").innerHTML = "";
});
