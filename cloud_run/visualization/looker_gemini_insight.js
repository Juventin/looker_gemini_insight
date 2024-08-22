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

          .custom-loader {
              width: 70px;
              height: 70px;
              display: grid;
              margin: auto;
          }
          .custom-loader::before,
          .custom-loader::after {    
              content:"";
              grid-area: 1/1;
              --c: radial-gradient(farthest-side,#69c3d8 92%,#0000);
              background: 
                var(--c) 50%  0, 
                var(--c) 50%  100%, 
                var(--c) 100% 50%, 
                var(--c) 0    50%;
              background-size: 12px 12px;
              background-repeat: no-repeat;
              animation: s2 1s infinite;
          }
          .custom-loader::before {
            margin:4px;
            filter:hue-rotate(35deg);
            background-size: 8px 8px;
            animation-timing-function: linear
          }

          @keyframes s2{ 
            100%{transform: rotate(.5turn)}
          }
        </style>
      `;

    // Create containers and elements
    var container = element.appendChild(document.createElement("div"));
    container.className = "vis";

    this._imgElement = container.appendChild(document.createElement("div"));
    this._textElement = container.appendChild(document.createElement("div"));
    this._textElement.className = "result-text";
    this._textElement.innerHTML = "<div class='custom-loader'></div>";

    this.datahash = 0;
  },

  // Render in response to the data or settings changing
  updateAsync: function (data, element, config, queryResponse, details, done) {
    // Compute data hash, to only update if prompt or data has changed
    if (data.length > 0 && typeof config.prompt !== "undefined") {
      var dataHash = this.stringToHash(config.prompt + JSON.stringify(data));
    } else {
      var dataHash = this.datahash;
    }

    // Only update if data is not empty and dataHash has changed
    if (
      data.length > 0 &&
      dataHash != this.datahash &&
      typeof config.prompt !== "undefined"
    ) {
      this.datahash = dataHash;
      this._textElement.className = "loading-text";
      this._textElement.innerHTML = "<div class='custom-loader'></div>";
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
