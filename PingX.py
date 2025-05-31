# meta developer: @SenkoSanModules
# meta name: PingX
# meta description: Проверка пинга и аптайма с настраиваемым шаблоном

from .. import loader
import time
import datetime

@loader.tds
class PingXMod(loader.Module):
    strings = {
        "name": "PingX",
        "default_template": (
            "⚡ <b>Ping:</b> <code>{ping}ms</code>\n"
            "⏱ <b>Uptime:</b> <code>{uptime}</code>"
        ),
        "default_loading": "⏳ Пинг...",
    }

    def __init__(self):
        self._start_time = time.time()
        self.config = loader.ModuleConfig(
            {
                "template": self.strings["default_template"],
                "loading_text": self.strings["default_loading"],
            },
            self
        )

    async def pinxcmd(self, message):
        start = time.time()
        loading = self.config["loading_text"]
        m = await message.edit(loading)

        ping = round((time.time() - start) * 1000)
        uptime = str(datetime.timedelta(seconds=int(time.time() - self._start_time)))

        template = self.config["template"]

        try:
            result = template.format(ping=ping, uptime=uptime)
        except Exception as e:
            result = f"❌ Ошибка в шаблоне: <code>{e}</code>"

        await m.edit(result)