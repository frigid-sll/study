```
npm install -g markdown-http-server
ln -s /www/server/nodejs/v14.17.6/bin/markdown-server /usr/local/bin/markdown-server
npm install -g pm2
ln -s /www/server/nodejs/v14.17.6/bin/pm2 /usr/local/bin/pm2
cd /www/odoo/
pm2 start markdown-server --name markdownServer -- -p 955 -d false
```



```
pm2 stop all
pm2 stop 进程号
```

