FROM nginx:alpine

# Copy static assets once available
# COPY ./dashboard /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
