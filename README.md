# BoBoChicken-BBS
钵钵鸡BSS
## Git 使用公告
1. 先pull再push
2. 设置branch为main
3. commit message 写详尽一点
## 环境
### 后端
1. 后端环境是WSL2gi
2. 在WSL2里~文件夹下
3. 创建一个文件夹mkdir bbs
4. git init
5. git checkout -b main
6. git remote add origin git@github.com:Kurt232/BoBoChicken-BBS.git
7. git pull origin main
8. git push --set-upstream origin main
9. 不要在main分支上写代码，先在本地分支写，没有问题再本地merge，再pull main, 再push