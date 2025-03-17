### 制造快照(show ip ospf nei)
```shell
pyats parse "show ip ospf nei" --testbed-file ../top.yaml --output ./pyats_files/netdevops_ospf_nei_snapshot
```

### 快照对比(show ip ospf nei) <尝试去改router-id制造diff>
```shell
pyats diff ./pyats_files/ospf_nei_snapshot ./pyats_files/netdevops_ospf_nei_snapshot 
```

### 制造快照(show ip route ospf)
```shell
pyats parse "show ip route ospf" --testbed-file ../top.yaml --output ./pyats_files/netdevops_ip_route_ospf_snapshot
```

### 快照对比(show ip route ospf) <只是让宣告的网络不同即可>
```shell
pyats diff ./pyats_files/ip_route_ospf_snapshot ./pyats_files/netdevops_ip_route_ospf_snapshot 
```