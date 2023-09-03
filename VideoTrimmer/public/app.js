const { fetchFile } = FFmpegUtil;
const { FFmpeg } = FFmpegWASM;
let ffmpeg = null;

// Create a function to trim our video without blocking our webpage
const trim = async ({ target: { files } }) => {
  // Load ffmpeg
  if (ffmpeg === null) {
      ffmpeg = new FFmpeg();
      await ffmpeg.load({
          coreURL: "/assets/core/package/dist/umd/ffmpeg-core.js",
      });
  }

  // Write file into name
  const { name } = files[0];
  await ffmpeg.writeFile(name, await fetchFile(files[0]));

  // Get the start and end times of our form
  var start = document.getElementById('start').value;
  var end = document.getElementById('end').value;

  // Start trimming and write out our message
  const message = document.getElementById('message');
  message.innerHTML = 'Start trimming';
  await ffmpeg.exec(['-i', name, '-ss', start, '-to', end, 'output.mp4']);
  message.innerHTML = 'Complete trimming';
  
  // Download file
  const data = await ffmpeg.readFile('output.mp4');  
  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  a.href = URL.createObjectURL(new Blob([data.buffer], { type: 'video/mp4' }));
  a.download = 'trimed-video.mp4';
  a.click();
}

// When a file is uploaded, run the trim function
const elm = document.getElementById('uploader');
elm.addEventListener('change', trim);