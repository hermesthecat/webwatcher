# WebWatcher

WebWatcher is a small docker image meant to be a sidecar container to other applications.

WebWatcher will watch folders you specify for new audio or image files and convert them to the much smaller webm/webp formats.

Configurable to do things like keep source files, lossless compression, and quality control.

# Getting Started

## Running

### Python
`python -m webwatcher --path <dir> --source-path <dir> [...args] [command]`

### Docker

```shell
docker run --rm -it -v /path/to/media/dir:/watch/media -v /path/to/storage:/source webwatcher:latest watch
```

Simply, you run the container, mounting any number of directories under `/watch`, and, if you wish to keep the original files, a folder under `/source`

### Docker Compose
```yaml
---
version: "2.1"
services:
  radarr:
    image: registry.gitlab.com/cclloyd1/webwatcher:latest
    container_name: webwatcher
    environment:
      - AUDIO_DELETE=true
      - IMAGE_DELETE=true
      - IS_WINDOWS=true # Only required if running on a Windows host
    volumes:
      - /path/to/media:/watch/media
      - /path/to/storage:/source
    restart: unless-stopped
```



## Subcommands 

| Command   | Description                                                                                                                                                               |
|:----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `clean`   | Moves old files to source if a converted file was found and deletes old files (respecting configuration options)                                                          |
| `watch`   | Default command that is run when no command is specified.  Watches the directories for new files and converts them if it matches a filetype, then cleans up the old file. |
| `convert` | Run a one-time pass of the `watch` command on the directories that will scan all existing files and process them.                                                         |



# Configuration Options

There are a few configuration options available when running the module.  Environment variables have higher priority than command line arguments.

Some CLI args are inverse of the environment variable, because the default behavior is True.

### Default File Types
- **Images:** .png, .jpg, .bmp, .jpeg
- **Audio:** .mp3, .aac, .flac, .wav, .wma, .aac, .m4a, .ogg

## All options

| CLI Argument            | Env Variable    | Description                                                                       | Default   |
|:------------------------|:----------------|:----------------------------------------------------------------------------------|:----------|
| `--path <dir>`          | `WATCH_DIRS`    | Path(s) to watch for.  You can use `--path` multiple times.                       | `/watch`  |
| `--source-path <path>`  | `SOURCE_PATH`   | Where to store original files                                                     | `/source` |
| `--dry-run`             | `DRY_RUN`       | Print output but perform no file/conversion operations                            | `False`   |
| `--no-keep-source`      | `KEEP_SOURCE`   | Moves source file to folder after converting                                      | `True`    |
| `--no-watch-audio`      | `WATCH_AUDIO`   | Watch for new audio files                                                         | `True`    |
| `--audio-delete`        | `AUDIO_DELETE`  | Delete audio files once converted                                                 | `False`   |
| `--audio-format <str>`  | n/a             | Specify another extension to watch for as an audio file.  Can use multiple times. | -         |
| `--no-watch-images`     | `WATCH_IMAGES`  | Watch for new image files                                                         | `True`    |
| `--image-delete`        | `IMAGE_DELETE`  | Delete image files once converted                                                 | `False`   |
| `--image-format <str>`  | n/a             | Specify another extension to watch for as an image file.  Can use multiple times. | -         |
| `--webp-command <path>` | `WEBP_COMMAND`  | Set the executable path of ImageMagick, when running as a module[^1]              | `convert` |
| `--webp-quality <int>`  | `WEBP_QUALITY`  | Quality when converting to webp.  0 - 100 (lossless).                             | `60`      |
| `--webp-lossless`       | `WEBP_LOSSLESS` | Losslessly convert to webp (average 20% size reduction)                           | `False`   |
| `--windows`             | `IS_WINDOWS`    | Use compatibility polling for watching filesystem changes[^2]                     | `False`   |

[^1]: On Windows, you would want to set this to `magick`
[^2]: If you are running from docker and mounting a Windows volume, you must specify this for the container to be able to see filesystem changes.


# Planned Changes
- Upload to PyPi
- Give CLI arguments priority over environment variables
- More conversion options
- Exclude sub-directories
- 