# WebWatcher

WebWatcher is a small docker image meant to be a sidecar container to other applications.

WebWatcher will watch folders you specify for new audio or image files and convert them to the much smaller webm/webp formats.

Configurable to do things like keep source files, lossless compression, and quality control.


### To run
`docker run --rm -it -v /path/to/media/dir:/watch/media webwatcher:latest watch`


