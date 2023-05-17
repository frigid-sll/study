##### 第一个历程：环境准备

```
tree nfs-file/
nfs-file/
├── nfs-client
└── nfs-server

cd /etc/ansible/ansible-playbook/nfs-file/nfs-server
echo '/data 172.16.1.0/24(rw,sync)' >exports
```

##### 第二个历程：编写剧本信息

- 剧本内容

  ```
  vim nfs-server.yaml
  
  - hosts: nfs
    tasks:
      - name: 01-install nfs software
        yum:
          name: ['nfs-utils','rpcbind']
          state: installed
  
  - hosts: nfs_server
    tasks:
      - name: 01-copy conf file
        copy: src=/etc/ansible/ansible-playbook/nfs-file/nfs-server/exports dest=/etc
        notify: restart nfs server
      - name: 02-create data dir
        file: path=/data state=directory owner=nfsnobody group=nfsnobody
      - name: 03-boot server
        service: name={{ item }} state=started enabled=yes
        with_items:
          - rpcbind
          - nfs
    handlers:
      - name: restart nfs server
        service: name=nfs state=restarted
  
  - hosts: nfs_client
    tasks:
      - name: 01-mount
        mount: src=172.16.1.31:/data path=/mnt fstype=nfs state=mounted
      - name: 02-check mount info
        shell: df -h|grep /data
        register: mount_info
      - name: display mount info
        debug: msg={{ mount_info.stdout_lines }}
  ```

- 修改主机清单文件

  ```
  vim /etc/ansible/hosts
  
  [nfs:children]
  nfs_server
  nfs_client
  
  [nfs_server]
  172.16.1.31
  
  [nfs_client]
  172.16.1.7
  172.16.1.8
  ```

  

##### 第三个历程：进行剧本测试

```
ansible-playbook --syntax-check nfs-server.yaml

#如果挂载那块有问题是正常的，因为客户端没有挂载进行调取查看的时候是空的
ansible-playbook -C nfs-server.yaml

ansible-playbook nfs-server.yaml
```

