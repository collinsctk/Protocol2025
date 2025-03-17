### C8Kv1
```shell
router bgp 65001
 bgp log-neighbor-changes
 network 172.16.1.0 mask 255.255.255.0
 neighbor 10.1.1.2 remote-as 65002
 neighbor 10.1.1.2 ebgp-multihop 255

```

### C8Kv2
```shell
router bgp 65002
 bgp log-neighbor-changes
 network 2.2.2.2 mask 255.255.255.255
 network 192.168.1.0
 neighbor 10.1.1.1 remote-as 65001
 neighbor 10.1.1.1 ebgp-multihop 255

```