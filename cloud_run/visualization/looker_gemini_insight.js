const CLOUD_RUN_URL = "<CLOUD_RUN_URL>"; // Automatically overridden by the server

looker.plugins.visualizations.add({
  id: "looker_gemini_insight",
  label: "Gemini Insight",
  options: {
    prompt: {
      type: "string",
      label: "Prompt",
      values: [{ Summary: "summarize" }, { Forecast: "predict" }],
      display: "radio",
      default: "summarize",
    },
  },

  create: function (element, config) {
    element.innerHTML = `
        <style>
          .vis {
            height: 100%;
            display: flex;
            text-align: center;
            font-size: 18px;
            font-family: sans-serif;
            margin: 0 30px;
          }
          .loading-text {
            color: grey;
            font-size: 15px;
            margin: auto;
            flex: 1;
          }
          .result-text {
            font-size: 15px;
            margin: auto;
            flex: 1;
          }
          .error-text {
            color: #F46D61;
            font-size: 15px;
            margin: auto;
            flex: 1;
          }
        </style>
      `;

    // Create containers and elements
    var container = element.appendChild(document.createElement("div"));
    container.className = "vis";

    this._imgElement = container.appendChild(document.createElement("div"));
    this._textElement = container.appendChild(document.createElement("div"));
    this._textElement.className = "result-text";

    this.datahash = 0;
  },

  // Render in response to the data or settings changing
  updateAsync: function (data, element, config, queryResponse, details, done) {
    // Compute data hash, to only update if prompt or data has changed
    if (data.length > 0) {
      var dataHash = this.stringToHash(config.prompt + JSON.stringify(data));
    } else {
      var dataHash = this.datahash;
    }

    // Only update if data is not empty and dataHash has changed
    if (data.length > 0 && dataHash != this.datahash) {
      this.datahash = dataHash;
      this._textElement.className = "loading-text";
      this._textElement.innerHTML = "Loading ...";
      this.clearErrors();

      // Update displays
      if (config.prompt == "predict") {
        this._imgElement.innerHTML =
          "<img src='" + CLOUD_RUN_URL + "fortune_teller.png' height='100%'/>";
      } else {
        this._imgElement.innerHTML = "";
      }

      // Perform API POST request
      var url = CLOUD_RUN_URL + config.prompt;

      var req = new XMLHttpRequest();
      req.open("POST", url, true);
      req.setRequestHeader("Content-Type", "application/json");
      req.send(JSON.stringify(queryResponse));

      console.log(JSON.stringify(queryResponse));

      req.onreadystatechange = () => {
        if (req.readyState === 4) {
          if (req.status === 200) {
            // Update content
            this._textElement.className = "result-text";
            this._textElement.innerHTML = req.responseText;
          } else {
            this._textElement.className = "error-text";
            this._textElement.innerHTML = "Error: " + req.responseText;
          }
        }
      };

      done();
    }
  },

  stringToHash: (string) => {
    let hash = 0;

    if (string.length == 0) return hash;

    for (i = 0; i < string.length; i++) {
      char = string.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }

    return hash;
  },
});
