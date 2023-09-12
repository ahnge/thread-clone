var replyAppState = {
  replyUnitCount: htmx.findAll(".reply-unit").length,
};

var replyUnitLogic = (upperUnit) => {
  const replyImages = upperUnit.querySelector(".reply-images");
  const replyImgContainer = upperUnit.querySelector(
    ".new-reply-image-container"
  );
  const replyImgCount = upperUnit.querySelector(".reply-image-count");
  // When user input images, we want to display before uploading to the server.
  replyImages.addEventListener("change", () => {
    // Ensure uploaded images are not more than 10
    if (replyImages.files.length > 10) {
      alert("Images can't be more that 10.");
      replyImages.value = "";
    } else {
      const maxAllowedSize = 5 * 1024 * 1024;
      // Add images to img Container one by one
      for (const file of replyImages.files) {
        // Ensure file size is withing limit, else we don't add to ui
        if (file.size > maxAllowedSize) {
          alert("We don't allow file size greater that 5 MB.");
          continue;
        }
        let imgSrc = URL.createObjectURL(file);
        replyImgContainer.innerHTML += `
        <div class="carousel-item transition sm:max-w-xs xl:max-w-md relative reply-image" data-image-name="${file.name}">
            <img src="${imgSrc}" class="rounded-box w-auto max-h-[12rem] object-contain z-10" />
            <div class="reply-image-delete cursor-pointer absolute rounded-full text-white bg-black/40 top-3 right-3 px-2 z-20" data-image-delete-name="${file.name}">x</div>
        </div>
      `;
      }
      // Remove the file of size greater that limited size from threadImages.files
      const dt = new DataTransfer();
      for (const file of replyImages.files) {
        if (file.size < maxAllowedSize) dt.items.add(file);
      }
      replyImages.files = dt.files;
      // Update the imageCount
      replyImgCount.value = replyImages.files.length;

      // Update ui only if thread.images exist
      if (replyImages.files.length > 0) {
        // Display the image container
        replyImgContainer.classList.remove("hidden");
        // Hide the clip
        upperUnit.querySelector(".reply-clip").classList.add("hidden");
        // Enable the att btn
        let attBtnStillExists =
          upperUnit.querySelector(".reply-smallter") &&
          upperUnit.querySelector(".reply-att");
        if (attBtnStillExists) {
          upperUnit
            .querySelector(".reply-smallter")
            .classList.remove("opacity-30");
          upperUnit.querySelector(".reply-att").disabled = false;
        }
        const xButtons = replyImgContainer.querySelectorAll(
          ".reply-image-delete"
        );
        const newImages = replyImgContainer.querySelectorAll(".reply-image");
        // Listen for img remove buttons
        [...xButtons].forEach((btn) => {
          // We make a new dt instance and add all images except the one we want to delete
          btn.addEventListener("click", () => {
            const name = btn.dataset.imageDeleteName;
            const dt = new DataTransfer();
            for (let i = 0; i < replyImages.files.length; i++) {
              const file = replyImages.files[i];
              if (name !== file.name) dt.items.add(file);
            }
            // Update the FileList
            replyImages.files = dt.files;
            // Update the ImageCount
            replyImgCount.value = replyImages.files.length;
            // Update the ui
            // remove the image
            [...newImages].forEach((newImg) => {
              if (newImg.dataset.imageName === name) {
                newImg.remove();
              }
            });
            if (replyImages.files.length === 0) {
              // Show the clip back
              upperUnit.querySelector(".reply-clip").classList.remove("hidden");
              // Hide the img container
              replyImgContainer.classList.add("hidden");
            }
            // Enable the att button
            if (
              replyImages.files.length === 0 &&
              content.value.length === 0 &&
              attBtnStillExists
            ) {
              upperUnit
                .querySelector(".reply-smallter")
                .classList.add("opacity-30");
              upperUnit.querySelector(".reply-att").disabled = true;
            }
          });
        });
      }
    }
  });

  // text content logic
  const content = upperUnit.querySelector(".content");
  content.addEventListener("input", () => {
    // Make textarea grows as text input grows
    textareaRows = content.value.split("\n");
    if (textareaRows[0] != "undefined" && textareaRows.length < 12)
      counter = textareaRows.length;
    else if (textareaRows.length >= 12) counter = 12;
    else counter = 1;
    content.rows = counter;

    let attBtnStillExists =
      upperUnit.querySelector(".reply-smallter") &&
      upperUnit.querySelector(".reply-att");

    // toggle delete-unit btn accordinly and
    if (content.value.length > 0) {
      // Show the delete-unit btn
      upperUnit.querySelector(".reply-delete-unit").classList.remove("hidden");
      // disable or enable att btn only if they exists.
      if (attBtnStillExists) {
        upperUnit
          .querySelector(".reply-smallter")
          .classList.remove("opacity-30");
        upperUnit.querySelector(".reply-att").disabled = false;
      }
    } else {
      // Hide it only if unit count is one
      if (replyAppState.replyUnitCount === 1) {
        upperUnit.querySelector(".reply-delete-unit").classList.add("hidden");
      }
    }
    if (
      content.value.length === 0 &&
      replyImages.files.length === 0 &&
      attBtnStillExists
    ) {
      upperUnit.querySelector(".reply-smallter").classList.add("opacity-30");
      upperUnit.querySelector(".reply-att").disabled = true;
    }
  });
  // When content is focus, we hide all other clips and show the focus one if there is no images in threadImages
  content.addEventListener("focus", () => {
    // Hide all other clips
    [...replyUnits].forEach((ru) => {
      ru.querySelector(".reply-clip").classList.add("hidden");
    });
    // Show the focused unit's clip
    if (replyImages.files.length === 0) {
      upperUnit.querySelector(".reply-clip").classList.remove("hidden");
    }
  });

  // Delete unit logic
  const deleteUnit = upperUnit.querySelector(".reply-delete-unit");
  deleteUnit.addEventListener("click", () => {
    if (replyAppState.replyUnitCount === 1) {
      // Clear the text and hide the du btn
      content.value = "";
      deleteUnit.classList.add("hidden");
      // If thre are also no images in the unit, disable the att btn
      if (replyImages.files.length === 0) {
        upperUnit.querySelector(".reply-smallter").classList.add("opacity-30");
        upperUnit.querySelector(".reply-att").disabled = true;
      }
    } else {
      // Remove the parent upperUnit and update the state
      const parentUpperUnit = deleteUnit.parentNode.parentNode.parentNode;
      parentUpperUnit.remove();
      replyAppState.replyUnitCount--;
      // Update the upperUnits global varialbe
      replyUnits = htmx.findAll(".reply-unit");

      const lastReplyUnit = replyUnits[replyUnits.length - 1];
      // Show the att btn and att-parent of the last upperUnit in the upperUnits set
      lastReplyUnit.querySelector(".reply-att").classList.remove("hidden");
      lastReplyUnit.querySelector(".reply-smallter").classList.remove("hidden");
      lastReplyUnit
        .querySelector(".reply-att-parent")
        .classList.remove("hidden");
      // Show the clip of the last upperUnit if the unit's threadImages is empty
      if (lastReplyUnit.querySelector(".reply-images").files.length === 0) {
        lastReplyUnit.querySelector(".reply-clip").classList.remove("hidden");
      }
    }
  });
};

var replyUnits = htmx.findAll(".reply-unit");

[...replyUnits].forEach(replyUnitLogic);

// New unit logic
var replyUnitContainer = htmx.find("#reply-unit-container");
replyUnitContainer.addEventListener("htmx:afterSwap", (evt) => {
  // Update the unit count
  replyAppState.replyUnitCount++;

  // Update the upperUnits variable
  replyUnits = htmx.findAll(".reply-unit");

  const aboveUnit = replyUnits[replyUnits.length - 2];
  // Hide the att btn of the above unit and att-parent
  evt.detail.requestConfig.elt.classList.add("hidden");
  aboveUnit.querySelector(".reply-smallter").classList.add("hidden");
  aboveUnit.querySelector(".reply-att-parent").classList.add("hidden");

  // Hide the clip icon of the above unit
  aboveUnit.querySelector(".reply-clip").classList.add("hidden");

  // run the logic for the comming unit
  const newReplyUnit = replyUnits[replyUnits.length - 1];
  replyUnitLogic(newReplyUnit);

  // Show all the du buttons
  [...replyUnits].forEach((uu) => {
    uu.querySelector(".reply-delete-unit").classList.remove("hidden");
  });
});

// Disable the form submit btn after posting
var threadReplyForm = htmx.find("#thread-reply-form");
if (threadReplyForm) {
  threadReplyForm.addEventListener("submit", () => {
    const btn = threadReplyForm.querySelector("button[type='submit']");
    btn.disabled = true;
    btn.style.opacity = "0.7";
  });
}

var commentReplyForm = htmx.find("#comment-reply-form");
if (commentReplyForm) {
  commentReplyForm.addEventListener("submit", () => {
    const btn = commentReplyForm.querySelector("button[type='submit']");
    btn.disabled = true;
    btn.style.opacity = "0.7";
  });
}
