

## Nginx setting in ubuntu server for docker Django, Nginx


* Enter default.conf:
```
nano /etc/nginx/conf.d/default.conf
```

* Configure Nginx forward to Docker Nginx:
```
server {
   server_name imodels.uz www.imodels.uz;

   client_max_body_size 100M;

   proxy_connect_timeout 600s;
   proxy_read_timeout 300s;

   location /backend/ {
       proxy_http_version 1.1;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_pass http://127.0.0.1:8080;
   }

   location /media/ {
       proxy_http_version 1.1;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_pass http://127.0.0.1:8080/backend/media/;
   }

   location / {
      alias /var/www/iModels/;
      try_files $uri $uri/ /index.html;
   }
}
```