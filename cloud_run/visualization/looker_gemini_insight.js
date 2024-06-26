looker.plugins.visualizations.add({
  id: "looker_gemini_insight",
  label: "Gemini Insight",
  options: {
    prompt: {
      type: "string",
      label: "Prompt",
      values: [
        { Summary: "summarize" },
        { Forecast: "predict" },
        { "(Show prompt)": "showprompt" },
      ],
      display: "radio",
      default: "summarize",
    },
  },

  create: function (element, config) {
    element.innerHTML = `
        <style>
          .hello-world-vis {
            height: 100%;
            display: flex;
            text-align: center;
            font-size: 18px;
            font-family: sans-serif;
            margin: 0 30px;
          }
          .hello-world-text {
            font-size: 15px;
            margin: auto;
            flex: 1;
          }
        </style>
      `;

    // Create containers and elements
    var container = element.appendChild(document.createElement("div"));
    container.className = "hello-world-vis";

    this._imgElement = container.appendChild(document.createElement("div"));
    this._textElement = container.appendChild(document.createElement("div"));
    this._textElement.className = "hello-world-text";

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
      this._textElement.innerHTML = "";
      this.clearErrors();

      // Update displays
      if (config.prompt == "predict") {
        this._imgElement.innerHTML =
          "<img src='https://gemini-insight-jht3hnrd2a-ew.a.run.app/fortune_teller.png' height='100%' />";
      } else {
        this._imgElement.innerHTML = "";
      }

      // Perform API POST request
      var url =
        "https://gemini-insight-jht3hnrd2a-ew.a.run.app/" + config.prompt;

      var req = new XMLHttpRequest();
      req.open("POST", url, true);
      req.setRequestHeader("Content-Type", "application/json");
      req.send(JSON.stringify(queryResponse));

      console.log(JSON.stringify(queryResponse));

      req.onreadystatechange = () => {
        if (req.readyState === 4) {
          if (req.status === 200) {
            var result = req.responseText;
          } else {
            console.log("Error: " + req.responseText);
          }

          // Update content
          this._textElement.innerHTML = result;
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

// Developed by Jeremy Juventin
