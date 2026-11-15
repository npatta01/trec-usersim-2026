# TREC UserSim 2026 approach film

The film connects the two official tasks to the draft-and-edit control flow,
then follows the WikiANN and WikiNeural search described in the [notebook paper](../usersim2026.pdf).
The [preliminary organizer results](../organizer-results-2026-11-07.md)
supply the aggregate scores, reply lengths, and editor audit.

- [Narration and captions](story.json)
- [Layout and animation](film.html)
- [Workshop artwork](../slides/talk-assets/README.md)

Narration uses the local Kokoro `af_heart` synthetic voice from the TRECVID
approach film. The conversation example paraphrases the published notebook.

## Render

Use Python with `kokoro-onnx==0.6.1` and `soundfile==0.13.1`, Node with
Playwright and Chromium, and FFmpeg with libx264. Place the public
[Kokoro ONNX model](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx)
and [voice bank](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin)
in a build directory outside the checkout. Install Playwright in that
directory or set `USERSIM_FILM_PLAYWRIGHT` to its module path. To select an
installed Chrome binary, set `USERSIM_FILM_CHROME`.

From the repository root, with `film_build_dir` set to the build directory:

```bash
python docs/paper/approach-film/narrate.py "$film_build_dir"
node docs/paper/approach-film/render.cjs "$film_build_dir" --preview
node docs/paper/approach-film/render.cjs "$film_build_dir"
```

The renderer writes `approach.mp4` and the narrator writes `captions.vtt`.
The project page uses those files and the opening preview frame in [assets](../../../assets/).
