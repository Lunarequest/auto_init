import os
import subprocess
import git# type: ignore
import dbus# type: ignore
import getpass
import tarfile
import shutil
# from downloader_cli.download import Download
# add this downloader-cli = "*" to pip file if you want to renable above^


def replcaer(path: str, user: str):
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
    if not os.path.exists(path):
        os.mkdir(path)
    elif os.listdir(path):
        shutil.rmtree(path)
        os.mkdir(path)
    git.Git(path).clone("https://github.com/advaithm/Dotfiles.git")
    print("stowing files")
    os.chdir(path)
    os.mkdir("~/.vim/pack/packager/opt/vim-packager")
    git.Git("~/.vim/pack/packager/opt/vim-packager").clone(
        "https://github.com/kristijanhusak/vim-packager"
    )
    os.mkdir("~/.config/nvim/pack/packager/opt/vim-packager")
    git.Git("~/.config/nvim/pack/packager/opt/vim-packager").clone(
        "https://github.com/kristijanhusak/vim-packager"
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
    if not os.path.exists("/usr/bin/yay"):
        os.mkdir("yay")
        git.Git("yay").clone("https://aur.archlinux.org/yay.git")
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


def kde_theme(staging_dir:str):
    os.chdir(staging_dir)
    # url = "" need to make a new url too often sticking to keeping a copy in the repo
    # Download(url).download()
    subprocess.check_call(["sudo", "plasmapkg2", "-gi", "Neonyt-Global.zip"])
    subprocess.check_call(["lookandfeeltool", "-a", "Neonyt-Global"])
    icons_nya(staging_dir)
    sddm_theme(staging_dir)


def icons_nya(staging_dir:str):
    if (
        os.path.exists(
            f"/home/{getpass.getuser()}/.local/share/icons/Mojave-CT-Night-Mode"
        )
        != True
    ):
        os.chdir(staging_dir)
        icon_set = tarfile.open("Mojave-CT-Night-Mode.tar.xz")
        icon_set.extractall(f"/home/{getpass.getuser()}/.local/share/icons")


def sddm_theme(staging_dir:str):
    os.system("sudo tar -xvf -C /usr/share/sddm/themes/")
    os.system("sudo mv kde_settings.conf /etc/sddm.conf.d/kde_settings.conf")


if __name__ == "__main__":
    staging_dir = os.getcwd()
    dot_files()
    kde_theme(staging_dir)
    wallpaper()
