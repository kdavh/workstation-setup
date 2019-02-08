os_flavor=$((test $(uname) = 'Darwin' && echo 'mac') || \cat /etc/*-release | grep -Po '(?<=^ID\=)\w*')

if [ '$os_flavor' = 'mac' ]; then
    ### DO: Manually export mac-terminal-app-profile to $DOTFILES/sh/mac-terminal-app-profile

    # TODO: make automatic
    # /usr/libexec/PlistBuddy -c "print :'Window Settings':mac-terminal-app-profile" ~/Library/Preferences/com.apple.Terminal.plist
    # plutil -h
fi

$HOME/dev/dotfiles-work/export.sh
