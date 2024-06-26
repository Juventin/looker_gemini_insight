//// SAMPLE HELLO WORLD VISUALIZATION

looker.plugins.visualizations.add({
  // Id and Label are legacy properties that no longer have any function besides documenting
  // what the visualization used to have. The properties are now set via the manifest
  // form within the admin/visualizations page of Looker
  id: "looker_gemini_insight",
  label: "Gemini Insight",
  options: {
    font_size: {
      type: "string",
      label: "Prompt",
      values: [{ Summary: "large" }, { Forecast: "small" }],
      // TODO: Change values here
      display: "radio",
      default: "large",
    },
  },
  // Set up the initial state of the visualization
  create: function (element, config) {
    // Insert a <style> tag with some styles we'll use later.
    element.innerHTML = `
        <style>
          .hello-world-vis {
            /* Vertical centering */
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
          }
          .hello-world-text-large {
            font-size: 72px;
          }
          .hello-world-text-small {
            font-size: 18px;
          }
        </style>
      `;

    // Create a container element to let us center the text.
    var container = element.appendChild(document.createElement("div"));
    container.className = "hello-world-vis";

    // Create an element to contain the text.
    this._textElement = container.appendChild(document.createElement("div"));
  },
  // Render in response to the data or settings changing
  updateAsync: function (data, element, config, queryResponse, details, done) {
    // Clear any errors from previous updates
    this.clearErrors();

    // Grab the first cell of the data
    // var firstRow = data[0];
    // var firstCell = firstRow[queryResponse.fields.dimensions[0].name];

    // Insert the data into the page
    this._textElement.innerHTML =
      LookerCharts.Utils.htmlForCell("Hello World!");

    console.log(JSON.stringify(data));
    console.log(JSON.stringify(queryResponse));

    // Set the size to the user-selected size
    if (config.font_size == "small") {
      this._textElement.className = "hello-world-text-small";
    } else {
      this._textElement.className = "hello-world-text-large";
    }

    // We are done rendering! Let Looker know.
    done();
  },
});
