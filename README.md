# Auto init

auto init is a python script that sets up plasma the way I like it, It also installs my zshrc, my configs for vim/neovim and finally my neofetch.conf. Auto init has 2 parts. `auto_init.py` installs everything including the plasma theme. `auto_init` will replace the username in all dotfiles so you can ignore changing them. If for whatever reason you want only a small part i.e. only the dotfiles or only the wallpaper you can use `gui.py` which uses kivy as a gui framework. feel free to use anything from this repo for whatever you want to do. I do plan to use the new tools created add in plasma 5.22 to setup as much as possible in the future

after you run this plasma should look a bit like this(latte dock and plasma 5.21 not included)

![plasma](.github/desktop.png)
## Future plans
I plan to reduce my usage of vscode(and any derivites) as much as possible due to personal reasons. This can be seen with the heavy work put into my on the vim and neovim configs on my dotfiles repo. I also am looking forward to plasma 5.22 as it adds many userspace utilites which should reduce the amount of weird js and things I am running.

I also plan to work on making as much of this code mypy complaint.
