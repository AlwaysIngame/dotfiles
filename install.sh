#!/bin/sh

cd ~
sudo pacman -S --needed --noconfirm git

echo Whats your name in format: First Last
read name
echo Whats your email
read email

git config --global user.name "$name"
git config --global user.email "$email"

git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -sic
cd ..
rm -rf yay

yay -S --needed - < packages.txt

sudo systemctl enable sddm.service
sudo systemctl enable bluetooth.service
sudo systemctl enable tlp.service

#zsh stuff
sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

git clone https://github.com/NvChad/NvChad ~/.config/nvim --depth 1
sudo pacman -S --needed --noconfirm ripgrep

cd dotfiles
cp .zshrc ~
cp .p10k.zsh ~
cp -R Wallpapers ~/Wallpapers
cp -R .config ~
