# FFmpeg Reference Guide

A practical reference for using **FFmpeg for audio/video processing, encoding, and streaming**.

FFmpeg is a powerful command-line multimedia framework used to:

* convert media formats
* compress videos
* extract audio
* record streams
* edit media
* stream video
* inspect media metadata

It is widely used in:

* video pipelines
* streaming services
* automation scripts
* media servers
* video editing workflows

---

# 1. Core Components

FFmpeg project consists of several tools.

| Tool          | Purpose                   |
| ------------- | ------------------------- |
| `ffmpeg`      | convert/process media     |
| `ffprobe`     | inspect media information |
| `ffplay`      | simple media player       |
| `libavcodec`  | encoding/decoding library |
| `libavformat` | container formats         |
| `libavfilter` | filters                   |

---

# 2. Basic Command Structure

General syntax:

```bash
ffmpeg [global options] \
       -i input \
       [options] \
       output
```

Example:

```bash
ffmpeg -i input.mp4 output.mkv
```

---

# 3. Inspect Media

Use **ffprobe** to view metadata.

```bash
ffprobe video.mp4
```

Show streams only:

```bash
ffprobe -hide_banner -show_streams video.mp4
```

Show format info:

```bash
ffprobe -show_format video.mp4
```

Show JSON output:

```bash
ffprobe -print_format json -show_format -show_streams video.mp4
```

Useful for scripting.

---

# 4. Convert Media Formats

Basic conversion:

```bash
ffmpeg -i input.mov output.mp4
```

Convert video container:

```bash
ffmpeg -i input.mkv output.mp4
```

Convert audio:

```bash
ffmpeg -i input.wav output.mp3
```

---

# 5. Copy Streams Without Re-encoding

Fast remux:

```bash
ffmpeg -i input.mkv -c copy output.mp4
```

Useful when:

* container incompatible
* no codec change needed

---

# 6. Extract Streams

## Extract Audio

```bash
ffmpeg -i video.mp4 -vn audio.mp3
```

`-vn` disables video.

---

## Extract Video Only

```bash
ffmpeg -i video.mp4 -an video_only.mp4
```

---

## Extract Subtitles

```bash
ffmpeg -i video.mkv -map 0:s:0 subtitles.srt
```

---

# 7. Encode Video

Example H264 encoding:

```bash
ffmpeg -i input.mov -c:v libx264 output.mp4
```

Adjust quality:

```bash
ffmpeg -i input.mov -c:v libx264 -crf 23 output.mp4
```

CRF scale:

| Value | Quality           |
| ----- | ----------------- |
| 18    | visually lossless |
| 23    | default           |
| 28    | lower quality     |

---

# 8. Encode Audio

Example MP3 encoding:

```bash
ffmpeg -i input.wav -c:a libmp3lame output.mp3
```

Set bitrate:

```bash
ffmpeg -i input.wav -b:a 192k output.mp3
```

---

# 9. Resize Video

Scale resolution:

```bash
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4
```

Maintain aspect ratio:

```bash
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4
```

---

# 10. Trim Media

Trim by time:

```bash
ffmpeg -ss 00:00:10 -i input.mp4 -to 00:00:20 output.mp4
```

Fast seek:

```bash
ffmpeg -ss 10 -i input.mp4 -t 5 output.mp4
```

---

# 11. Change Frame Rate

```bash
ffmpeg -i input.mp4 -r 30 output.mp4
```

---

# 12. Capture Screenshots

Single frame:

```bash
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 screenshot.png
```

Multiple frames:

```bash
ffmpeg -i video.mp4 frames/frame_%04d.png
```

---

# 13. Record Screen

Linux example:

```bash
ffmpeg -f x11grab -i :0.0 screen.mp4
```

Specify resolution:

```bash
ffmpeg -video_size 1920x1080 -f x11grab -i :0.0 output.mp4
```

---

# 14. Record Webcam

```bash
ffmpeg -f v4l2 -i /dev/video0 output.mp4
```

---

# 15. Add Subtitles

Burn subtitles:

```bash
ffmpeg -i video.mp4 -vf subtitles=subs.srt output.mp4
```

Add soft subtitles:

```bash
ffmpeg -i video.mp4 -i subs.srt -c copy -c:s mov_text output.mp4
```

---

# 16. Combine Audio and Video

```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
```

---

# 17. Create GIF

```bash
ffmpeg -i video.mp4 -vf "fps=10,scale=320:-1" output.gif
```

Better quality GIF:

```bash
ffmpeg -i video.mp4 -vf palettegen palette.png
ffmpeg -i video.mp4 -i palette.png -lavfi paletteuse output.gif
```

---

# 18. Concatenate Videos

Create list file:

```
file 'part1.mp4'
file 'part2.mp4'
file 'part3.mp4'
```

Run:

```bash
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

---

# 19. Audio Filters

Normalize volume:

```bash
ffmpeg -i input.wav -af loudnorm output.wav
```

Increase volume:

```bash
ffmpeg -i input.wav -af "volume=2.0" output.wav
```

---

# 20. Video Filters

Example blur:

```bash
ffmpeg -i input.mp4 -vf boxblur output.mp4
```

Crop video:

```bash
ffmpeg -i input.mp4 -vf crop=1280:720:0:0 output.mp4
```

Rotate video:

```bash
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4
```

---

# 21. Streaming

Stream to RTMP:

```bash
ffmpeg -re -i input.mp4 -f flv rtmp://server/live/stream
```

---

# 22. Hardware Acceleration

Example using NVENC:

```bash
ffmpeg -i input.mp4 -c:v h264_nvenc output.mp4
```

Intel QuickSync:

```bash
ffmpeg -i input.mp4 -c:v h264_qsv output.mp4
```

---

# 23. Useful Flags

| Flag   | Purpose          |
| ------ | ---------------- |
| `-i`   | input file       |
| `-c`   | codec            |
| `-c:v` | video codec      |
| `-c:a` | audio codec      |
| `-vf`  | video filter     |
| `-af`  | audio filter     |
| `-ss`  | seek position    |
| `-t`   | duration         |
| `-r`   | frame rate       |
| `-b:v` | video bitrate    |
| `-b:a` | audio bitrate    |
| `-map` | select stream    |
| `-y`   | overwrite output |

---

# 24. Debugging

Show detailed logs:

```bash
ffmpeg -loglevel debug -i input.mp4 output.mp4
```

Show available codecs:

```bash
ffmpeg -codecs
```

List formats:

```bash
ffmpeg -formats
```

List filters:

```bash
ffmpeg -filters
```

---

# 25. Automation Examples

Batch convert videos:

```bash
for f in *.mov; do
    ffmpeg -i "$f" "${f%.mov}.mp4"
done
```

Convert directory audio:

```bash
for f in *.wav; do
    ffmpeg -i "$f" "${f%.wav}.mp3"
done
```

---

# 26. Learning Resources

Official documentation:

* [https://ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)
* [https://trac.ffmpeg.org/wiki](https://trac.ffmpeg.org/wiki)
* [https://ffmpeg.org/ffmpeg.html](https://ffmpeg.org/ffmpeg.html)

---

# 27. Advanced Topics

Topics worth studying:

### Encoding

* CRF encoding
* two-pass encoding
* bitrate control

### Streaming

* RTMP
* HLS
* DASH

### Filters

* filter graphs
* complex filters
* overlay filters

### Hardware acceleration

* NVENC
* VAAPI
* QuickSync

---

# 28. Useful Tools Around FFmpeg

| Tool        | Purpose                |
| ----------- | ---------------------- |
| `ffprobe`   | inspect media          |
| `yt-dlp`    | download video streams |
| `HandBrake` | GUI transcoder         |
| `OBS`       | live streaming         |
| `GStreamer` | media pipelines        |

---

# 29. Practical Exercises

Good exercises:

1. compress large videos
2. extract audio from movies
3. create GIF clips
4. batch convert videos
5. stream video to RTMP
6. automate video pipelines

---
