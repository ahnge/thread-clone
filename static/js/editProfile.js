// Take the profile image input tag
var profileImage = htmx.find(".profile-image");

// When an image is selected
profileImage.addEventListener("change", (e) => {
  // Ensure it is within limited size
  const maxAllowedSize = 5 * 1024 * 1024;
  if (profileImage.files[0] > maxAllowedSize) {
    alert("We don't allow file size greater that 5 MB.");
  } else {
    // If it is within limit, create an img src
    const imgSrc = URL.createObjectURL(profileImage.files[0]);
    // Reflect it on ui
    const profileAvatar = htmx.find(".edit-profile-avatar");
    profileAvatar.classList.remove("placeholder");
    profileAvatar.innerHTML = `
        <div class="w-12 md:w-14">
            <img src="${imgSrc}"
                class="w-full rounded-full" />
        </div>
    `;
  }
});

var editForm = htmx.find("#profile-edit-form");
editForm.addEventListener("submit", () => {
  const btn = editForm.querySelector("button");
  btn.disabled = true;
  btn.style.opacity = "0.7";
});
