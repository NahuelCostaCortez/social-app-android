docker run --rm -d --network pruebas --name nginx \
       -v $(pwd)/sitios_nginx:/etc/nginx/conf.d \
       -p 80:80 nginx
