import ImagePicker from "./components/ImagePicker";

const technologies = [
  {
    title: "ReactJS",
    logo: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9Ii0xMS41IC0xMC4yMzE3NCAyMyAyMC40NjM0OCI+CiAgPHRpdGxlPlJlYWN0IExvZ288L3RpdGxlPgogIDxjaXJjbGUgY3g9IjAiIGN5PSIwIiByPSIyLjA1IiBmaWxsPSIjNjFkYWZiIi8+CiAgPGcgc3Ryb2tlPSIjNjFkYWZiIiBzdHJva2Utd2lkdGg9IjEiIGZpbGw9Im5vbmUiPgogICAgPGVsbGlwc2Ugcng9IjExIiByeT0iNC4yIi8+CiAgICA8ZWxsaXBzZSByeD0iMTEiIHJ5PSI0LjIiIHRyYW5zZm9ybT0icm90YXRlKDYwKSIvPgogICAgPGVsbGlwc2Ugcng9IjExIiByeT0iNC4yIiB0cmFuc2Zvcm09InJvdGF0ZSgxMjApIi8+CiAgPC9nPgo8L3N2Zz4K",
  },
  {
    title: "Python",
    logo: "http://assets.stickpng.com/images/5848152fcef1014c0b5e4967.png",
  },
  {
    title: "Tensoorflow Extended",
    logo: "https://tensorflow.google.cn/site-assets/images/project-logos/tensorflow-extended-tfx-logo-social.png?hl=fr",
  },
  {
    title: "Tensorflow",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Tensorflow_logo.svg/1200px-Tensorflow_logo.svg.png",
  },
  {
    title: "Keras",
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Keras_logo.svg/1200px-Keras_logo.svg.png",
  },
];

function App() {
  return (
    <div className="App">
      <div className="gradient"></div>
      <div className="titleContainer">
        <h1 className="page-title">🌱 Plant Disease Detection 🌱</h1>
      </div>
      <ImagePicker />
      {/* <div className="techsContainer">
        <h2>Technological Stack:</h2>
        <div className="techs">
          {technologies.map((tech) => (
            <div className="tech">
              <img src={tech.logo} />
              <h4>{tech.title}</h4>
            </div>
          ))}
        </div>
      </div> */}
    </div>
  );
}

export default App;
