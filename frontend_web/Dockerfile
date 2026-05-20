# Use a lightweight web server to serve the static HTML file
FROM nginx:alpine

# Copy the static frontend files to Nginx's default public directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
