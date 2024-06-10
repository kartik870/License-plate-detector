const uploader = document.getElementById("file_uploader");
const file_input = document.getElementById("upload_input");
const file_upload_info = document.getElementById("file_upload_info");
const tick = document.getElementById("tick");
const progress_bar = document.getElementById("progress_bar");
const progress_indicator = document.getElementById("progress_indicator");
let load = 0;
let process = "";

// Trigger click on file of input type
uploader.addEventListener("click", () => {
  file_input.click();
});

file_input.onchange = (e) => {
  const file_detail = document.getElementById("file_detail");
  file_upload_info.style.display = "block";
  file_detail.innerText = e.target.files[0].name;
  console.log(e.target.files[0]);
  load = 0;
  process = setInterval(upload, 10);
};

const upload = () => {
  if (load >= 100) {
    clearInterval(process);
    progress_indicator.innerText = "100% Upload Completed!";
    tick.style.display = "block";
  } else {
    tick.style.display = "hidden";
    load++;
    progress_bar.style.width = load + "%";
    progress_indicator.innerText = "Uploaded : " + load + "%";
  }
};

document.getElementById("startButton").addEventListener("click", function () {
  var loader = document.getElementById("loader");
  loader.style.display = "block";
});

document.getElementById("startButton").addEventListener("click", function () {
  var loader = document.getElementById("loader-text");
  loader.style.display = "block";
});
