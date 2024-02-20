document
  .getElementById("cafeForm")
  .addEventListener("submit", function (event) {
    // Get the values from the number input and currency dropdown
    var numberValue = document.getElementById("coffee_price_number").value;
    var currencySymbol = document.getElementById("currency_symbol").value;

    // Combine the values
    var combinedValue = numberValue + " " + currencySymbol;

    // Update the hidden input with the combined value
    var hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "coffee_price";
    hiddenInput.value = combinedValue;

    // Append the hidden input to the form
    document.getElementById("cafeForm").appendChild(hiddenInput);
  });
