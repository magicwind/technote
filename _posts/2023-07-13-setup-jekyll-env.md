---
layout: post
title:  "如何搭建jekyll环境"
categories: jekyll
---

Linux OS: Ubuntu, Debian (root user)

## Install Ruby Using RVM
```bash
$ apt update
$ apt-get install gnupg2
$ gpg2 --keyserver keyserver.ubuntu.com --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
$ \curl -sSL https://get.rvm.io | bash -s stable
Downloading https://github.com/rvm/rvm/archive/1.29.12.tar.gz
Downloading https://github.com/rvm/rvm/releases/download/1.29.12/1.29.12.tar.gz.asc
gpg: Signature made Sat Jan 16 02:46:22 2021 CST
gpg:                using RSA key 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
gpg: Good signature from "Piotr Kuczynski <piotr.kuczynski@gmail.com>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 7D2B AF1C F37B 13E2 069D  6956 105B D0E7 3949 9BDB
GPG verified '/usr/local/rvm/archives/rvm-1.29.12.tgz'
Creating group 'rvm'
Installing RVM to /usr/local/rvm/
Installation of RVM in /usr/local/rvm/ is almost complete:

  * First you need to add all users that will be using rvm to 'rvm' group,
    and logout - login again, anyone using rvm will be operating with `umask u=rwx,g=rwx,o=rx`.

  * To start using RVM you need to run `source /etc/profile.d/rvm.sh`
    in all your open shell windows, in rare cases you need to reopen all shell windows.
  * Please do NOT forget to add your users to the rvm group.
     The installer no longer auto-adds root or users to the rvm group. Admins must do this.
     Also, please note that group memberships are ONLY evaluated at login time.
     This means that users must log out then back in before group membership takes effect!
  * WARNING:  version This account is currently not available. detected - Zsh 4.3.12 / 5.0.0+ is recommended,
     with current one errors to be expected - bugs in shell code interpretation.
Thanks for installing RVM 🙏

$ source /etc/profile.d/rvm.sh
$ rvm install "ruby-3.2.2"
```

## Install Ruby Using Rbenv
```bash
$ apt update
$ apt install git curl autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev $ zlib1g-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev
$ curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash

# Bash
$ echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(rbenv init -)"' >> ~/.bashrc
$ source ~/.bashrc

# Zsh
$ echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.zshrc
$ echo 'eval "$(rbenv init -)"' >> ~/.zshrc
$ source ~/.zshrc

$ rbenv -v
$ rbenv install -l
$ rbenv install 3.2.2
$ rbenv global 3.2.2
```

## Install Gems
```
gem install bundler jekyll
bundle install
```