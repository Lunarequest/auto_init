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
    path = os.path.expanduser("~/.dotfiles")
    git.Git(path).clone("git@github.com:advaithm/Dotfiles.git")
    print("stowing files")
    os.chdir("~/.dotfiles")
    os.system(
        "git clone https://github.com/kristijanhusak/vim-packager ~/.vim/pack/packager/opt/vim-packager"
    )
    os.system(
        "git clone https://github.com/kristijanhusak/vim-packager ~/.config/nvim/pack/packager/opt/vim-packager"
    )
    dirs = os.listdir()
    stow_command = "stow "
    for files in dirs:
        if os.path.isdir(f"~/.dotfiles/{files}"):
            stow_command = stow_command + " " + files
    if getpass.getuser() != "nullrequest":
        replcaer(path, getpass.getuser())
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
    print("wallpaper set")


def kde_theme(staging_dir):
    os.chdir(staging_dir)
    # url = "" need to make a new url too often stickig to keeping a copy in the repo
    # Download(url).download()
    subprocess.check_call(["sudo", "plasmapkg2", "-gi", "Neonyt-Global.zip"])
    subprocess.check_call(["lookandfeeltool", "-a", "Neonyt-Global"])


if __name__ == "__main__":
    staging_dir = os.getcwd()
    dot_files()
    kde_theme(staging_dir)
    wallpaper()
