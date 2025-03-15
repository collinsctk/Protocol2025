### 解决字体问题
```shell
wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJK-Regular.ttc.zip
unzip NotoSansCJK-Regular.ttc.zip
sudo mv NotoSansCJK-Regular.ttc /usr/share/fonts/
fc-cache -fv

```