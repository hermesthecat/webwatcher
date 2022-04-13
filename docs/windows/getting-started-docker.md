This is a more in-depth guide on how to run on Windows using Docker.

# Install Docker

Docker is a container management platform for Windows.  Containers are just bundled apps that run in their own virtual machine of sorts.

1. Download Docker Desktop from their website [here](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe) ([docs](https://docs.docker.com/desktop/windows/install/#install-docker-desktop-on-windows))
2. Once installed, go to start menu and type `docker` and open Docker Desktop.  It will open to the system tray, not a window.  It may take a few minutes to start up if it needs to update anything.




# Running WebWatcher

## Before running

- Ensure you have at least 1 folder that you want to watch for files
- Ensure that you have a folder to store the original copies in (if you wish to keep them, which is enabled by default)
- Take note of the full paths you want to watch and the path of the source folder.

## Actually running

### Command line
1. Open Powershell
2. Type the following, modifying it slightly
   ```shell
   docker run --name webwatcher --rm -D -e IS_WINDOWS=true  -v C:\Path\To\Media\Files:/watch/media -v /path/to/more/media/dir:/watch/extra -v /path/to/storage:/source webwatcher:latest
   ```
3. To stop the container, type `docker stop webwatcher`.
   
You can add the `-v` flag unlimited times.  Every folder you want to watch should be mounted somewhere under `/watch`.

### Docker Compose (recommended)

Docker compose provides a way to save a template of your run command above for later so that you don't have to type it in every time.  It is HIGHLY recommended you use this over the `docker run` command.

1. Download the example [docker-compose.yml](https://gitlab.com/cclloyd1/webwatcher/-/raw/main/docs/windows/docker-compose.yml?inline=false) file.  Make note of where you save it.
2. Open the file in Notepad (or similar) and modify the volumes so that it is using the correct folder
3. In powershell, type `cd C:\Path\To\folder\with\compose\file`
4. Run `docker-compose up -d` to start the container in the background.
5. To stop, type `docker-compose down`, or `docker stop webwatcher`.

