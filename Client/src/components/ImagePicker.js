import react, { useState, useEffect } from "react";

import flatten from "lodash/flatten";
import { decode as base64_decode, encode as base64_encode } from "base-64";
import axios from "axios";

function Selector(props) {
  var { onImageChange } = props;
  let inputRef;

  return (
    <div className="selector">
      <h2>Select your plant image</h2>
      <div
        onClick={() => {
          inputRef.click();
        }}
        className="fileButtonContainer"
      >
        <svg
          width="336px"
          height="195px"
          preserveAspectRatio="xMidYMid meet"
          viewBox="0 0 30 30"
        >
          <defs>
            <linearGradient
              id="logo-gradient"
              x1="50%"
              y1="0%"
              x2="50%"
              y2="100%"
            >
              <stop offset="0%" stopColor="#44bd32">
                <animate
                  attributeName="stopColor"
                  values="#44bd32; #C4E538; #44bd32"
                  dur="4s"
                  repeatCount="indefinite"
                ></animate>
              </stop>

              <stop offset="100%" stopColor="#C4E538">
                <animate
                  attributeName="stopColor"
                  values="#C4E538; #44bd32; #C4E538"
                  dur="4s"
                  repeatCount="indefinite"
                ></animate>
              </stop>
            </linearGradient>
          </defs>

          <g>
            <path
              className="plant"
              fill="url('#logo-gradient')"
              d="M 23 3 C 19 3 15 5 15 10 C 15 11.14495 15.16959 12.035484 15.474609 12.734375 C 15.268194 13.210299 15.089973 13.679465 14.927734 14.142578 C 14.555256 13.352857 14.100903 12.612734 13.574219 11.925781 C 13.382101 11.675204 13.18125 11.430283 12.972656 11.191406 C 12.988706 11.068882 13 10.946803 13 10.832031 C 13 6.6660312 9.6660312 5 6.3320312 5 L 3 5 L 3 7.5 C 3 12.5 6.3320312 15 8.8320312 15 C 9.3360312 15 9.7755938 14.913969 10.183594 14.792969 C 9.4995937 13.790969 8.3406562 12.306141 6.7226562 10.994141 C 6.2936562 10.646141 6.2262188 10.016891 6.5742188 9.5878906 C 6.9222187 9.1588906 7.5514688 9.0904531 7.9804688 9.4394531 C 9.4068576 10.595757 10.848947 11.971916 11.589844 12.6875 C 11.718953 12.840128 11.866777 12.986648 11.986328 13.142578 C 13.258627 14.802033 14.003662 16.629437 14 18.998047 C 14.000044 19.002421 13.999949 19.007351 14 19.011719 L 15 19 L 16 19.001953 C 16.000007 18.997303 15.999998 18.992928 16 18.988281 C 15.98278 17.500702 16.531197 15.017276 17.769531 12.539062 C 18.072958 11.93183 18.417981 11.32414 18.802734 10.726562 C 19.507643 9.7209071 20.253801 8.7081308 20.945312 8.0136719 C 21.335313 7.6226719 21.968375 7.6197656 22.359375 8.0097656 C 22.751375 8.3997656 22.753281 9.0328281 22.363281 9.4238281 C 20.709281 11.084828 19.549844 12.9165 18.839844 14.9375 C 19.206844 14.9795 19.593 15 20 15 C 23 15 27 12 27 6 L 27 3 L 23 3 z M 15 21 C 13.318171 21 11.800298 21.694033 10.710938 22.808594 C 9.9288089 22.301474 9.0013685 22 8 22 C 5.239 22 3 24.239 3 27 L 9 27 L 13 27 L 19 27 L 24 27 L 27 27 C 27 24.791 25.209 23 23 23 C 22.691505 23 22.393919 23.043255 22.105469 23.109375 C 21.250187 22.425456 20.180024 22 19 22 C 18.789351 22 18.582715 22.017666 18.378906 22.042969 C 17.416556 21.385962 16.253303 21 15 21 z"
            ></path>
          </g>
        </svg>
        <p>Upload your image from here!</p>
      </div>
      <input
        hidden={true}
        className="image-picker"
        type="file"
        accept="image/*"
        onChange={onImageChange}
        ref={(refParam) => (inputRef = refParam)}
      />
      <div className="fileButton"></div>
    </div>
  );
}

const suggestions = [
  {
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1200px-Google_%22G%22_Logo.svg.png",
    title: "Google",
    baseurl: "https://www.google.com/search?q=",
    description:
      "Use Speedtest on all your devices with our free desktop and mobile apps.",
  },
  {
    logo: "https://cdn.vox-cdn.com/thumbor/JiRzoaU535Vs9YjU6LcJSvIGFBs=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/19224216/mb_yahoo_02.jpg",
    title: "Yahoo",
    baseurl: "https://search.yahoo.com/search?p=",
    description:
      "Use Speedtest on all your devices with our free desktop and mobile apps.",
  },
  {
    logo: "https://cdn.vox-cdn.com/thumbor/wBRCdEaZtpAd2bJBlOhtRC6euVk=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/21937385/binglogo.jpg",
    title: "Bing",
    baseurl: "https://www.bing.com/search?q=",
    description:
      "Use Speedtest on all your devices with our free desktop and mobile apps.",
  },
  {
    logo: "https://www.iconninja.com/files/375/9/268/search-engine-duckduckgo-icon.svg",
    title: "DuckDuckGo",
    baseurl: "https://duckduckgo.com/?q=",
    description:
      "Use Speedtest on all your devices with our free desktop and mobile apps.",
  },
];
function getBase64(file, cb) {
  let reader = new FileReader();
  console.log(file);
  reader.readAsDataURL(file);
  reader.onload = function () {
    cb(reader.result);
  };
  reader.onerror = function (error) {
    console.log("Error: ", error);
  };
}

function Suggestion(props) {
  let { title, baseurl, description, logo, query } = props;
  query = query.replaceAll("_", "++");
  return (
    <div
      onClick={() => {
        window.open("https://www.google.com/search?q=" + query, "_blank");
      }}
      className="suggestion"
    >
      <img className="suggestion-logo" width={100} height={100} src={logo} />
      <div>
        <div className="suggestion-title">{title}</div>
        <div className="suggestion-url">{baseurl + query}</div>
        <div className="suggestion-description">{description}</div>
      </div>
    </div>
  );
}
function SuggestionsFromGoogle(props) {
  const { query } = props;
  return (
    <div className="suggestions">
      {suggestions.map((suggestion) => (
        <Suggestion
          title={suggestion.title}
          baseurl={suggestion.baseurl}
          description={suggestion.description}
          logo={suggestion.logo}
          query={query}
          key={suggestion.title}
        />
      ))}
    </div>
  );
}

function Visualizer(props) {
  var { imageUrl, inProp } = props;
  return (
    <div className="visualizer">
      <img className="classification-image" src={imageUrl} />
    </div>
  );
}
function Healthyplant() {
  return (
    <>
      <h2 className="result">🎉​ Congrats 🎉​</h2>
      <h2 className="healthy">Your plant is Healthy​</h2>
    </>
  );
}
function Infectedplant(props) {
  let { prediction } = props;
  return (
    <>
      <h2 className="result">😟</h2>
      <h2 className="infected">Your plant is infected</h2>
      <h2 className="bold">
        The Disease is : {prediction.replaceAll("_", " ")}
      </h2>
      <h2 className="medium">
        🤩 Don't worry we got potential solutions for you from Search Engines 🤩
      </h2>
      <SuggestionsFromGoogle query={prediction} />
      {/* <button
        onClick={() =>
          window.open("https://www.google.com/search?q=" + prediction, "_blank")
        }
        class="help"
      >
        Click here to know more about the disease
      </button> */}
    </>
  );
}

function Predictor(props) {
  var { prediction, inProp } = props;
  return (
    <div className="predictor">
      {prediction.toLowerCase().search("healthy") != -1 &&
      prediction != null ? (
        <Healthyplant />
      ) : (
        <Infectedplant prediction={prediction} />
      )}
    </div>
  );
}
function convertImage() {
  return;
}

function predict(image, prediction, setPrediction) {
  let URL = "http://localhost:5000/";

  var urlencoded = new URLSearchParams();

  getBase64(image, async (img) => {
    await urlencoded.append("image", img);
    console.log(img);
    await fetch(URL, {
      method: "POST",
      mode: "cors",
      body: urlencoded,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      },
      withCredentials: false,
    })
      .then(async (response) => await response.text())
      .then((result) => {
        setPrediction(result);
      })
      .catch((error) => {
        console.log(error);
      });
  });
}

function keyToLabel() {
  const Labels = {};
}

export default function ImagePicker() {
  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);

  let onImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  useEffect(() => {
    if (image != null && imageUrl == null) {
      setImageUrl(URL.createObjectURL(image));

      console.log(image);
      console.log("URL: " + URL.createObjectURL(image));
      predict(image, prediction, setPrediction);
    }
  }, [image, imageUrl, prediction]);

  return (
    <div className="container">
      {image == null ? <Selector onImageChange={onImageChange} /> : null}
      {imageUrl != null ? <Visualizer imageUrl={imageUrl} /> : null}
      {prediction != null && imageUrl != null ? (
        <Predictor prediction={prediction} />
      ) : null}
    </div>
  );
}
