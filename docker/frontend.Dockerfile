FROM nginx:alpine

# Copy static assets once available
# COPY ./frontend /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
