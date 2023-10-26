

## Nginx setting in ubuntu server for docker Django, Nginx


* Enter default.conf:
```
nano /etc/nginx/conf.d/default.conf
```

* Configure Nginx forward to Docker Nginx:
```
server {
   server_name jobir.uz www.jobir.uz;

   location / {
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_pass http://localhost:8080;
   }
}
```