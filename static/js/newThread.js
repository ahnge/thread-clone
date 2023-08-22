htmx.find("#new-thread-tab").addEventListener("click", () => {
  htmx.removeClass(htmx.find("#new-thread-popup"), "top-full");
  htmx.addClass(htmx.find("#new-thread-popup"), "top-5");
});

// Slide down
htmx.find("#new-thread-close").addEventListener("click", () => {
  htmx.removeClass(htmx.find("#new-thread-popup"), "top-5");
  htmx.addClass(htmx.find("#new-thread-popup"), "top-full");
});

// States
let appState = {
  unitCount: htmx.findAll(".upper-unit").length,
};

const unitLogic = (upperUnit) => {
  const threadImages = upperUnit.querySelector(".thread-images");
  const imgContainer = upperUnit.querySelector(".new-thread-image-container");
  // When user input images, we want to display before uploading to the server.
  threadImages.addEventListener("change", () => {
    // Ensure uploaded images are not more than 10
    if (threadImages.files.length > 2) {
      console.log("hey hey hey");
    } else {
      // Add images to img Container one by one
      for (const file of threadImages.files) {
        let imgSrc = URL.createObjectURL(file);
        imgContainer.innerHTML += `
        <div class="carousel-item transition sm:max-w-xs xl:max-w-md relative new-image" data-image-name="${file.name}">
            <img src="${imgSrc}" class="rounded-box w-auto max-h-[12rem] object-contain z-10" />
            <div class="new-image-delete cursor-pointer absolute rounded-full text-white bg-black/40 top-3 right-3 px-2 z-20" data-image-delete-name="${file.name}">x</div>
        </div>
      `;
      }
      // Display the image container
      imgContainer.classList.remove("hidden");

      // Hide the clip
      upperUnit.querySelector(".clip").classList.add("hidden");

      // Enable the att btn
      let attBtnStillExists =
        upperUnit.querySelector(".smallter") && upperUnit.querySelector(".att");

      if (attBtnStillExists) {
        upperUnit.querySelector(".smallter").classList.remove("opacity-30");
        upperUnit.querySelector(".att").disabled = false;
      }

      const xButtons = imgContainer.querySelectorAll(".new-image-delete");
      const newImages = imgContainer.querySelectorAll(".new-image");
      // Listen for remove buttons
      [...xButtons].forEach((btn) => {
        // We make a new dt instance and add all images except the one we want to delete
        btn.addEventListener("click", () => {
          const name = btn.dataset.imageDeleteName;
          const dt = new DataTransfer();
          for (let i = 0; i < threadImages.files.length; i++) {
            const file = threadImages.files[i];
            if (name !== file.name) dt.items.add(file);
          }
          // Update the FileList
          threadImages.files = dt.files;
          // Update the ui
          // remove the image
          [...newImages].forEach((newImg) => {
            if (newImg.dataset.imageName === name) {
              newImg.remove();
            }
          });
          // Show the clip back
          if (threadImages.files.length === 0) {
            upperUnit.querySelector(".clip").classList.remove("hidden");
          }
          // Enable the att button
          if (
            threadImages.files.length === 0 &&
            content.value.length === 0 &&
            attBtnStillExists
          ) {
            upperUnit.querySelector(".smallter").classList.add("opacity-30");
            upperUnit.querySelector(".att").disabled = true;
          }
        });
      });
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
      upperUnit.querySelector(".smallter") && upperUnit.querySelector(".att");

    // toggle delete-unit btn accordinly and
    if (content.value.length > 0) {
      // Show the delete-unit btn
      upperUnit.querySelector(".delete-unit").classList.remove("hidden");
      // disable or enable att btn only if they exists.
      if (attBtnStillExists) {
        upperUnit.querySelector(".smallter").classList.remove("opacity-30");
        upperUnit.querySelector(".att").disabled = false;
      }
    } else {
      // Hide it only if unit count is one
      if (appState.unitCount === 1) {
        upperUnit.querySelector(".delete-unit").classList.add("hidden");
      }
    }
    if (
      content.value.length === 0 &&
      threadImages.files.length === 0 &&
      attBtnStillExists
    ) {
      upperUnit.querySelector(".smallter").classList.add("opacity-30");
      upperUnit.querySelector(".att").disabled = true;
    }
  });

  // Delete unit logic
  const deleteUnit = upperUnit.querySelector(".delete-unit");
  deleteUnit.addEventListener("click", () => {
    if (appState.unitCount === 1) {
      content.value = "";
      deleteUnit.classList.add("hidden");
      if (threadImages.files.length === 0) {
        upperUnit.querySelector(".smallter").classList.add("opacity-30");
        upperUnit.querySelector(".att").disabled = true;
      }
    } else {
      const parentUpperUnit = deleteUnit.parentNode.parentNode.parentNode;
      parentUpperUnit.remove();
      appState.unitCount--;
    }
  });
};

let upperUnits = htmx.findAll(".upper-unit");

[...upperUnits].forEach(unitLogic);

const unitContainer = htmx.find("#unit-container");
unitContainer.addEventListener("htmx:afterSwap", (evt) => {
  // Update the unit count
  appState.unitCount++;

  // Update the upperUnits variable
  upperUnits = htmx.findAll(".upper-unit");

  // Delete the att btn of the above unit
  evt.detail.requestConfig.elt.remove();
  upperUnits[upperUnits.length - 2].querySelector(".smallter").remove();

  // run the logic for the comming unit
  const newUpperUnit = upperUnits[upperUnits.length - 1];
  unitLogic(newUpperUnit);
});
