import os
import subprocess
import git
import dbus
from downloader_cli.download import Download
import getpass


def replcaer(path, user):
    for file in os.listdir(path):
        if os.path.isdir(f"{path}{file}"):
            replcaer(f"{path}{file}/", user)
        else:
            with open(f"{path}{file}", "r") as f:
                file_contents = f.read()
                file_contents.replace("nullrequest", user)
            f.close()
            with open(f"{path}{file}", "w") as f:
                f.write(file_contents)
            f.close()


def dot_files():
    user = getpass.getuser()
    path = os.path.expanduser("~/.dotfiles")
    git.Git(path).clone("git@github.com:advaithm/Dotfiles.git")
    print("stowing files")
    os.chdir("~/.dotfiles")
    dirs = os.listdir()
    stow_command = "stow "
    for files in dirs:
        if os.path.isdir(f"~/.dotfiles/{files}"):
            stow_command = stow_command + files + " "
    if user != "nullrequest":
        replcaer(path, user)
    subprocess.Popen(stow_command)
    print("finished stow")
    print("installing p10k")
    subprocess.check_call(["yay", "-S", "--noconfirm", "zsh-theme-powerlevel10k-git"])


def wallpaper():
    jscript = """
        var allDesktops = desktops();
        print (allDesktops);
        for (i=0;i<allDesktops.length;i++) {
                d = allDesktops[i];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                d.writeConfig("Image", "file://%s")
        }
        """
    print("setting wallpaper")
    plugin = "org.kde.image"
    session = dbus.SessionBus()
    path = os.path.expanduser("~/.dotfiles/wallpaper.png")
    plasma = dbus.Interface(
        session.get_object("org.kde.plasmashell", "/PlasmaShell"),
        dbus_interface="org.kde.PlasmaShell",
    )
    plasma.evaluateScript(jscript % (plugin, plugin, path))


def kde_theme(staging_dir):
    os.chdir(staging_dir)
    url = "https://dllb2.pling.com/api/files/download/j/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE2MTMxMjM1NjIiLCJ1IjpudWxsLCJsdCI6ImRvd25sb2FkIiwicyI6IjdiMDBlMDBkOThlOGVmNjhjZjcwMmEzNmQxYTQ5YjE4YjVmZTMxOGY3ODg2MGFlYmM0Y2NhMjVjYWQwNTZjNmU4ZjJiNDA1YjUyN2VlZmZkOGM1MDlkMDE1MmRmODUyY2E4YmJhNjMwMDdjMzVhMTk5MTg3ZmFmNTI0NjAyMmYwIiwidCI6MTYxMzQ0ODA0NSwic3RmcCI6IjJmYTY5NjlmYmMzNWRjYjRhNGVhNmFjN2E3YmJkMGYyIiwic3RpcCI6IjEyMi4xNjcuMTAwLjE1NSJ9.d0-ot0ssV7Nzy_vyJ47G42w_XvX1yTPKiXw3xuTIP2E/Neonyt-Global.zip"
    Download(url).download()
    subprocess.check_call(["sudo", "plasmapkg2", "-gi", "Neonyt-Global.zip"])
    subprocess.check_call(["lookandfeeltool", "-a", "Neonyt-Global"])


if __name__ == "__main__":
    staging_dir = os.getcwd()
    dot_files()
    kde_theme(staging_dir)
    wallpaper()
