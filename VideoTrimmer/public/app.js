const { fetchFile } = FFmpegUtil;
const { FFmpeg } = FFmpegWASM;
let ffmpeg = null;

// Create a function to trim our video without blocking our webpage
const trim = async ({ target: { files } }) => {
  const message = document.getElementById('message');
  if (ffmpeg === null) {
      ffmpeg = new FFmpeg();
      ffmpeg.on("log", ({ message }) => {
          console.log(message);
      })
      ffmpeg.on("progress", ({ progress }) => {
          message.innerHTML = `${progress * 100} %`;
      });
      await ffmpeg.load({
          coreURL: "/assets/core/package/dist/umd/ffmpeg-core.js",
      });
  }
  const { name } = files[0];
  await ffmpeg.writeFile(name, await fetchFile(files[0]));
  message.innerHTML = 'Start trimming';
  await ffmpeg.exec(['-i', name, '-ss', '0', '-to', '1', 'output.mp4']);
  message.innerHTML = 'Complete trimming';
  const data = await ffmpeg.readFile('output.mp4');

  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";

  a.href = URL.createObjectURL(new Blob([data.buffer], { type: 'video/mp4' }));
  a.download = 'trimed-video.mp4';
  a.click();
}

const elm = document.getElementById('uploader');
elm.addEventListener('change', trim);