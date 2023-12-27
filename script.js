const imageList = [
  "quest_items",
  "customs",
  "woods",
  "factory",
  "interchange",
  "shoreline",
  "reserve",
  "streets_of_tarkov",
  "lighthouse",
  "ground_zero",
  "Laboratory",
];
for (let i = 0; i < imageList.length; i++) {
  document.getElementById("select_bar").innerHTML +=
    "<button type='button' onclick=\"ChangeImage('" +
    imageList[i] +
    "')\">" +
    FormatName(imageList[i]) +
    "</button>";
}

function FormatName(fileName) {
  return (
    fileName.charAt(0).toUpperCase() + fileName.slice(1).toLowerCase()
  ).replace(/_/g, " ");
}

function ChangeImage(fileName) {
  document.getElementById("image").src = "images/" + fileName + ".jpg";
}

let hasZoomed = false;
function ZoomImage(event) {
  const body = document.body;
  const selectBar = document.getElementById("select_bar");
  const imageWrapper = document.getElementById("image_wrapper");
  const image = document.getElementById("image");
  if (hasZoomed) {
    body.style.overflow = "hidden";
    selectBar.style.display = "flex";
    imageWrapper.style.justifyContent = "center";
    imageWrapper.style.alignItems = "center";
    image.style.transform = "none";
    image.style.cursor = "zoom-in";
    hasZoomed = false;
  } else {
    imageWidth = image.clientWidth;
    imageHeight = image.clientHeight;
    offsetX = event.offsetX;
    offsetY = event.offsetY;
    body.style.overflow = "scroll";
    selectBar.style.display = "none";
    imageWrapper.style.justifyContent = "start";
    imageWrapper.style.alignItems = "start";
    image.style.transform = "scale(2)";
    image.style.cursor = "zoom-out";
    document.documentElement.scrollLeft =
      (offsetX / imageWidth) *
      (document.documentElement.scrollWidth -
        document.documentElement.clientWidth);
    document.documentElement.scrollTop =
      (offsetY / imageHeight) *
      (document.documentElement.scrollHeight -
        document.documentElement.clientHeight);
    hasZoomed = true;
  }
}
