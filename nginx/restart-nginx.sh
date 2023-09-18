#!/bin/sh

# Install inotify-tools if not already installed
if ! command -v inotifywait &> /dev/null; then
    echo "Installing inotify-tools..."
    apt-get update
    apt-get install -y inotify-tools
    echo "Installation complete."
fi

# Watch for changes in Nginx configuration files and reload Nginx
while true; do
    inotifywait -e modify,create,delete -r /etc/nginx/
    echo "Reloading Nginx..."
    nginx -s reload
done
