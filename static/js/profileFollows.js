var profileFollowTabs = htmx.findAll(".profile-follow-tab");

[...profileFollowTabs].forEach((pft) => {
  pft.addEventListener("htmx:beforeRequest", (e) => {
    // abort infinite xhr if any
    const followPopupContainer = htmx.find("#follow-popup-container");
    const pfis = followPopupContainer.querySelectorAll(".profile-f-infinite");
    pfis.forEach((pi) => {
      htmx.trigger(pi, "htmx:abort");
    });
    // Switch tab
    for (let pft of profileFollowTabs) {
      pft.classList.remove("border-b-2", "border-black");
    }
    e.detail.requestConfig.elt.classList.add("border-b-2", "border-black");
    // empty the container
    followPopupContainer.innerHTML = "";
  });
});

var profileTab = htmx.find("#profile-tab");
htmx.find("#container").addEventListener("htmx:afterSwap", (evt) => {
  if (evt.detail.requestConfig.elt === profileTab) {
    var profileFollowTabs = htmx.findAll(".profile-follow-tab");

    [...profileFollowTabs].forEach((pft) => {
      pft.addEventListener("htmx:beforeRequest", (e) => {
        // abort infinite xhr if any
        const followPopupContainer = htmx.find("#follow-popup-container");
        const pfis = followPopupContainer.querySelectorAll(
          ".profile-f-infinite"
        );
        pfis.forEach((pi) => {
          htmx.trigger(pi, "htmx:abort");
        });
        // Switch tab
        for (let pft of profileFollowTabs) {
          pft.classList.remove("border-b-2", "border-black");
        }
        e.detail.requestConfig.elt.classList.add("border-b-2", "border-black");
        // empty the container
        followPopupContainer.innerHTML = "";
      });
    });

    // clear follow-popup-container before another request
    var followModal = htmx.find("#follow_modal");
    followModal.addEventListener("close", (e) => {
      htmx.find("#follow-popup-container").innerHTML = "";
      // Change back to followers tab
      for (let pft of profileFollowTabs) {
        pft.classList.remove("border-b-2", "border-black");
      }
      profileFollowTabs[0].classList.add("border-b-2", "border-black");
    });
  }
});

var followModal = htmx.find("#follow_modal");
if (followModal) {
  followModal.addEventListener("close", (e) => {
    htmx.find("#follow-popup-container").innerHTML = "";
    // Change back to followers tab
    for (let pft of profileFollowTabs) {
      pft.classList.remove("border-b-2", "border-black");
    }
    profileFollowTabs[0].classList.add("border-b-2", "border-black");
  });
}
