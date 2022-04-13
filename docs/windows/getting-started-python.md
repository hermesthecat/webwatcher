This is a more in-depth guide on how to run on Windows.

# Install chocolatey

Chocolatey is a modern package manager for Windows.  Using this will make installing everything else MUCH easier.

1. Open the start menu and type `powershell`, then right click and run as administrator.
2. Paste in the following line and hit enter.
   ```shell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Close and reopen Powershell, then type `choco --version` to verify that it installed properly.

# Install Dependencies
This app runs on Python, so we will need that.  The latest version is 3.10, which is also the recommended version. FFmpeg is required for audio conversion.  ImageMagick is required for image conversion.  

We will install them all at once with only a couple commands.

1. Open Powershell as administrator
2. Type the following and hit Enter after each line
   ```shell
   choco install -y python --version=3.10
   choco install -y ffmpeg imagemagick
   ```

Once you run and install that, open a command prompt window and type `python --version` to verify that it installed properly.

It is recommended to close Powershell now to ensure the command paths are properly registered.


# Install WebWatcher

To install WebWatcher, we will download it from PyPi.  PyPi is a package repository for Python packages.  

1. Open the start menu and type `powershell`, right click, and run as administrator.
2. Type the following command and hit Enter
    ```shell
    pip install webwatcher
    ```
3. Verify that it is installed properly by running the command below
   ```
   python -m webwatcher --help
   ```


# Running WebWatcher

## Before running

- Ensure you have at least 1 folder that you want to watch for files
- Ensure that you have a folder to store the original copies in (if you wish to keep them, which is enabled by default)
- Take note of the full paths you want to watch and the path of the source folder.

## Actually running

1. Open Powershell
2. Type the following, modifying it slightly
   ```shell
   python -m webwatcher --path C:\Path\To\Folder\You\Want\To\Watch --source-dir C:\Path\To\Storage\For\Originals --dry-run
   ```
3. Add `--path C:\Path\To\Folder` for every folder you want to watch for files.  This can be added multiple times.
4. Quit anytime by pressing `Ctrl + C` in Powershell.

This will start WebWatcher in watch mode where it watches for new files that show up in the folder.  It will also convert existing files once when it starts up.

Note that `--dry-run` is in that command.  This will show you what files are going to be touched, without running any conversions or moving any files.  It is highly recommended you run it with this flag once, to confirm that the files you indend are the only ones being affected.  Once you are certain of this, you can run the command again without `--dry-run`.

