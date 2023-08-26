// Ok, future me. This file seems like confusing and not wanting to read again. Let me break it down for you before I forget. All of the logic within is base upon "upper-unit", which is just a html section of a form that contains a textarea and multiple images input. Check out _new_thread_form.html to see the primary upper unit. The problem is we might want more than just a unit for a form. If the user want to add more to a thread, we want to add another unit dynamically. We solve this with the htmx request to the server and we send another unit and add this unit within the form. All the interactivity is than listen on the newly added unit. That is.

// Slide up
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
  const imgCount = upperUnit.querySelector(".image-count");
  // When user input images, we want to display before uploading to the server.
  threadImages.addEventListener("change", () => {
    // Ensure uploaded images are not more than 10
    if (threadImages.files.length > 10) {
      alert("Images can't be more that 10.");
      threadImages.value = "";
    } else {
      const maxAllowedSize = 5 * 1024 * 1024;
      // Add images to img Container one by one
      for (const file of threadImages.files) {
        // Ensure file size is withing limit, else we don't add to ui
        if (file.size > maxAllowedSize) {
          alert("We don't allow file size greater that 5 MB.");
          continue;
        }
        let imgSrc = URL.createObjectURL(file);
        imgContainer.innerHTML += `
        <div class="carousel-item transition sm:max-w-xs xl:max-w-md relative new-image" data-image-name="${file.name}">
            <img src="${imgSrc}" class="rounded-box w-auto max-h-[12rem] object-contain z-10" />
            <div class="new-image-delete cursor-pointer absolute rounded-full text-white bg-black/40 top-3 right-3 px-2 z-20" data-image-delete-name="${file.name}">x</div>
        </div>
      `;
      }
      // Remove the file of size greater that limited size from threadImages.files
      const dt = new DataTransfer();
      for (const file of threadImages.files) {
        if (file.size < maxAllowedSize) dt.items.add(file);
      }
      threadImages.files = dt.files;
      // Update the imageCount
      imgCount.value = threadImages.files.length;

      // Update ui only if thread.images exist
      if (threadImages.files.length > 0) {
        // Display the image container
        imgContainer.classList.remove("hidden");
        // Hide the clip
        upperUnit.querySelector(".clip").classList.add("hidden");
        // Enable the att btn
        let attBtnStillExists =
          upperUnit.querySelector(".smallter") &&
          upperUnit.querySelector(".att");
        if (attBtnStillExists) {
          upperUnit.querySelector(".smallter").classList.remove("opacity-30");
          upperUnit.querySelector(".att").disabled = false;
        }
        const xButtons = imgContainer.querySelectorAll(".new-image-delete");
        const newImages = imgContainer.querySelectorAll(".new-image");
        // Listen for img remove buttons
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
            // Update the ImageCount
            imgCount.value = threadImages.files.length;
            // Update the ui
            // remove the image
            [...newImages].forEach((newImg) => {
              if (newImg.dataset.imageName === name) {
                newImg.remove();
              }
            });
            if (threadImages.files.length === 0) {
              // Show the clip back
              upperUnit.querySelector(".clip").classList.remove("hidden");
              // Hide the img container
              imgContainer.classList.add("hidden");
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
  // When content is focus, we hide all other clips and show the focus one if there is no images in threadImages
  content.addEventListener("focus", () => {
    // Hide all other clips
    [...upperUnits].forEach((uu) => {
      uu.querySelector(".clip").classList.add("hidden");
    });
    // Show the focused unit's clip
    if (threadImages.files.length === 0) {
      upperUnit.querySelector(".clip").classList.remove("hidden");
    }
  });

  // Delete unit logic
  const deleteUnit = upperUnit.querySelector(".delete-unit");
  deleteUnit.addEventListener("click", () => {
    if (appState.unitCount === 1) {
      // Clear the text and hide the du btn
      content.value = "";
      deleteUnit.classList.add("hidden");
      // If thre are also no images in the unit, disable the att btn
      if (threadImages.files.length === 0) {
        upperUnit.querySelector(".smallter").classList.add("opacity-30");
        upperUnit.querySelector(".att").disabled = true;
      }
    } else {
      // Remove the parent upperUnit and update the state
      const parentUpperUnit = deleteUnit.parentNode.parentNode.parentNode;
      parentUpperUnit.remove();
      appState.unitCount--;
      // Update the upperUnits global varialbe
      upperUnits = htmx.findAll(".upper-unit");

      const lastUpperUnit = upperUnits[upperUnits.length - 1];
      // Show the att btn and att-parent of the last upperUnit in the upperUnits set
      lastUpperUnit.querySelector(".att").classList.remove("hidden");
      lastUpperUnit.querySelector(".smallter").classList.remove("hidden");
      lastUpperUnit.querySelector(".att-parent").classList.remove("hidden");
      // Show the clip of the last upperUnit if the unit's threadImages is empty
      if (lastUpperUnit.querySelector(".thread-images").files.length === 0) {
        lastUpperUnit.querySelector(".clip").classList.remove("hidden");
      }
    }
  });
};

let upperUnits = htmx.findAll(".upper-unit");

[...upperUnits].forEach(unitLogic);

// New unit logic
const unitContainer = htmx.find("#unit-container");
unitContainer.addEventListener("htmx:afterSwap", (evt) => {
  // Update the unit count
  appState.unitCount++;

  // Update the upperUnits variable
  upperUnits = htmx.findAll(".upper-unit");

  const aboveUnit = upperUnits[upperUnits.length - 2];
  // Hide the att btn of the above unit and att-parent
  evt.detail.requestConfig.elt.classList.add("hidden");
  aboveUnit.querySelector(".smallter").classList.add("hidden");
  aboveUnit.querySelector(".att-parent").classList.add("hidden");

  // Hide the clip icon of the above unit
  aboveUnit.querySelector(".clip").classList.add("hidden");

  // run the logic for the comming unit
  const newUpperUnit = upperUnits[upperUnits.length - 1];
  unitLogic(newUpperUnit);

  // Show all the du buttons
  [...upperUnits].forEach((uu) => {
    uu.querySelector(".delete-unit").classList.remove("hidden");
  });
});
