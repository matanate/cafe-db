document.addEventListener("DOMContentLoaded", function () {
  // Fetch data from your /all endpoint
  fetch("/all")
    .then((response) => response.json())
    .then((data) => {
      // Call function to create cafe list
      createCafeList(data.cafes);
    })
    .catch((error) => console.error("Error fetching data:", error));

  const searchInput = document.getElementById("search-input");
  const byNameCheckbox = document.getElementById("flexRadioDefault1");

  // Debounce the toggleSearchList function
  const debouncedToggleSearchList = _.debounce(() => {
    const searchInputValue = searchInput.value.trim();
    toggleSearchFilter(searchInputValue);
  }, 300);

  searchInput.addEventListener("input", debouncedToggleSearchList);

  function toggleSearchFilter() {
    const searchTerm = searchInput.value.toLowerCase();

    // Determine which checkbox is selected
    const checkboxSelected = byNameCheckbox.checked ? "name" : "loc";

    // Fetch cafes based on the selected checkbox and search term
    fetch(`/search_${checkboxSelected}?${checkboxSelected}=${searchTerm}`)
      .then((response) => response.json())
      .then((data) => {
        // Call function to create cafe list
        createCafeList(data.cafes);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }

  // Function to create the cafe list
  function createCafeList(cafes) {
    const container = document.getElementById("cafes-container");
    container.innerHTML = "";
    if (cafes.error && cafes.error["Not Found"]) {
      // Handle case when no results are found
      const noResultsMessage = document.createElement("div");
      noResultsMessage.classList.add("no-results");
      noResultsMessage.textContent = cafes.error["Not Found"];
      container.appendChild(noResultsMessage);
    } else {
      // Loop through cafes and create a div for each one
      cafes.forEach((cafe) => {
        const cafeDiv = document.createElement("div");
        cafeDiv.classList.add("cafe-item");
        cafeDiv.id = `cafe-${cafe.id}`;
        const deleteForm = `<form action="/report-closed/${cafe.id}" method="POST">
        <button class="btn btn-danger" type="submit">Delete</button>
        </form>`;
        const editForm = `<form action="/edit-cafe/${cafe.id}" method="GET">
        <button class="btn btn-primary" type="submit">Edit</button>
        </form>`;

        // Add cafe information to the div
        cafeDiv.innerHTML = `
                <h2>${cafe.name}</h2>
                <p>Location: <b>${cafe.location}</b></p>
                <p><a href="${cafe.map_url}" target="_blank">View on Map</a></p>
                <p><b>Seating:</b> ${cafe.seats}</p>
                <p><b>Price:</b> ${cafe.coffee_price}</p>
                <p><b>Has Wi-Fi:</b> ${cafe.has_wifi ? "Yes" : "No"}</p>
                <p><b>Has Sockets:</b> ${cafe.has_sockets ? "Yes" : "No"}</p>
                <p><b>Has Toilet:</b> ${cafe.has_toilet ? "Yes" : "No"}</p>
                <p><b>Can Take Calls:</b> ${
                  cafe.can_take_calls ? "Yes" : "No"
                }</p>
                <img src="${cafe.img_url}" alt="${
          cafe.name
        }" style="max-width: 100%; height: auto;">
        <p>Added by <b>${cafe.author_name}</b></p>
        ${userId == 1 ? deleteForm : ""}
        ${userId == 1 || userId == cafe.author_id ? editForm : ""}
            `;

        // Append the cafe div to the container
        container.appendChild(cafeDiv);
      });
    }
  }
});
