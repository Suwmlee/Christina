### Christina 


主机器人,可以控制一个 userbot 和任意数量的普通 bot.只需要编辑配置文件 __config.ini__ :

```ini
[<name of userbot>]
api_id = <api_id>
api_hash = <api_hash>
[<name of bot>]
token = <bot token>
[<name of bot>]
token = <bot token>
```

```python userbot.py``` 验证(第一次运行需要验证token/接收验证码)

```nohup python userbot.py > christina.log 2>&1 &``` 后台运行

#### 致谢

[SteamedFish](https://github.com/SteamedFish/emacs-china-bot)
[PagerMaid-Modify](https://github.com/Xtao-Labs/PagerMaid-Modify)
