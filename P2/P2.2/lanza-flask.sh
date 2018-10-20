docker run --name amigos \
   -e DEPLOYMENT_MODE=production \
   -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
   --rm -d --network pruebas amigos:1.0
