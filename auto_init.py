import os
import subprocess
from git import Repo  # type: ignore
import dbus  # type: ignore
import getpass
import tarfile
import shutil
import time


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
    print("cloning dotfiles")
    Repo.clone_from("git clone https://github.com/advaithm/Dotfiles.git", path)
    print("Done clone")
    print("-" * 35)
    print("Installing vim-packager")
    os.chdir(os.path.expanduser("~/"))
    Repo.clone_from(
        "https://github.com/kristijanhusak/vim-packager",
        os.path.expanduser("~/.vim/pack/packager/opt/vim-packager"),
    )
    Repo.clone_from(
        "https://github.com/kristijanhusak/vim-packager",
        os.path.expanduser("~/.config/nvim/pack/packager/opt/vim-packager"),
    )
    print("Installed vim-packager")
    print("-" * 35)
    os.chdir(path)
    dirs = os.listdir()
    print("installing dotfiles")
    stow_command = "stow "
    for files in dirs:
        if os.path.isdir(files) and files.startswith(".") == False:
            stow_command = stow_command + " " + files
            if getpass.getuser() != "nullrequest":
                replcaer(path, getpass.getuser())
    subprocess.Popen(stow_command.split())
    print("finished installing dotfiles")
    print("-" * 35)
    print("installing zshrc deps")
    subprocess.check_call(
        [
            "pacman",
            "-S",
            "--noconfirm",
            "zsh-autosuggestions zsh-history-substring-search zsh-syntax-highlighting",
        ]
    )
    if os.path.exists("/usr/bin/yay") == False:
        os.chdir(f"/home/{getpass.getuser()}")
        git.Git().clone("https://aur.archlinux.org/yay.git")
        os.chdir("yay")
        os.system("makepkg -si")
    os.system(
        """sh -c '$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)'"""
    )
    subprocess.check_call(["yay", "-S", "--noconfirm", "zsh-theme-powerlevel10k-git"])
    print(
        "done installing deps. the prompt to configure power level 10k will start in 5 seconds"
    )
    print("-" * 35)
    time.sleep(5)
    subprocess.check_call(["p10k", "configure"])
    shutil.rmtree(f"/home/{getpass.getuser()}/.zshrc")
    subprocess.Popen(["stow", "zsh"])  # this is a hack since omz writes its own zshrc


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
    plasma.evaluateScript(
        jscript % (plugin, plugin, path)
    )  # I had no idea plasma could run js!?!?!?
    print("wallpaper set")


def kde_theme(staging_dir: str):
    os.chdir(staging_dir)
    # url = "" need to make a new url too often sticking to keeping a copy in the repo
    # Download(url).download()
    subprocess.check_call(["sudo", "plasmapkg2", "-gi", "Neonyt-Global.zip"])
    subprocess.check_call(["lookandfeeltool", "-a", "Neonyt-Global"])
    icons_nya(staging_dir)
    sddm_theme(staging_dir)


def icons_nya(staging_dir: str):
    if (
        os.path.exists(
            f"/home/{getpass.getuser()}/.local/share/icons/Mojave-CT-Night-Mode"
        )
        != True
    ):
        os.chdir(staging_dir)
        icon_set = tarfile.open("Mojave-CT-Night-Mode.tar.xz")
        icon_set.extractall(f"/home/{getpass.getuser()}/.local/share/icons")
    subprocess.Popen(
        ["/usr/lib/plasma-changeicons", "Mojave-CT-Night-Mode"]
    )  # this is a weird thing introduced in plasma 5.18, just happy it works


def sddm_theme(staging_dir: str):
    os.system("sudo tar -xvf -C /usr/share/sddm/themes/")
    os.system(
        "sudo mv kde_settings.conf /etc/sddm.conf.d/kde_settings.conf"
    )  # another hack, this time to set the sddm theme.


if __name__ == "__main__":
    staging_dir = os.getcwd()
    dot_files()
    kde_theme(staging_dir)
    wallpaper()
