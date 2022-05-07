import react, { useState, useEffect } from "react";
import { getBase64 } from "../utils/encoder";
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
      {prediction.search("Healthy") != -1 && prediction != null ? (
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

async function predict(image, prediction, setPrediction) {
  let URL = "http://localhost:5000/";

  var urlencoded = new URLSearchParams();
  urlencoded.append(
    "image",
    "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\n"
  );

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
    predict(image, prediction, setPrediction);
  };

  useEffect(() => {
    if (image != null && imageUrl == null)
      setImageUrl(URL.createObjectURL(image));
    console.log(imageUrl);
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
