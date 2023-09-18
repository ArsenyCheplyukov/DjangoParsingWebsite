# Use the official Nginx base image
FROM nginx:1.25.2-alpine

# Remove the default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom configuration
COPY default.conf /etc/nginx/conf.d

# Expose port 80
EXPOSE 80

# Create a shell script for restarting Nginx
#COPY restart-nginx.sh /usr/local/bin/
#RUN chmod +x /usr/local/bin/restart-nginx.sh

# Start Nginx and then execute the restart script
#CMD ["sh", "-c", "nginx && /usr/local/bin/restart-nginx.sh"]
