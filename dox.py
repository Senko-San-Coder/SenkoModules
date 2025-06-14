from telethon import events
from .. import loader, utils
import asyncio
import random
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import red, black, blue

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

class DoxToolMod(loader.Module):
    strings = {"name": "DoxTool"}
    def __init__(self):
        self.usage_limit = {}

    async def doxcmd(self, message):
        number = utils.get_args_raw(message)
        if not number.startswith("+") or not number[1:].isdigit():
            await message.edit("❌ Укажи корректный номер. Пример: `.dox +79991234567`")
            return

        uid = str(message.sender_id)
        today = datetime.now().date()
        if uid in self.usage_limit and self.usage_limit[uid][0] == today:
            if self.usage_limit[uid][1] >= 3:
                await message.edit("🔒 Лимит 3 запроса в день достигнут.")
                return
            self.usage_limit[uid][1] += 1
        else:
            self.usage_limit[uid] = [today, 1]

        await message.edit(f"🕵️ Начинаю поиск данных для `{number}`...\n⏱️ Это займёт примерно 4-5 минут...")

        data = await self.query_bots(number, message)
        await message.edit("📄 Формирую PDF-досье, подожди секунду...")

        pdf = self.generate_pdf(number, data)
        await message.client.send_file(message.chat_id, pdf, caption="📄 Фейковое досье готово.")
        await message.delete()

    async def query_bots(self, number, message):
        bots = [
            "@InfinitySearcch_bot", "@FastSearch66_bot", "@fasthlr_bot", "@mnp_bot", "@Search",
            "@slb_infa_ibot", "@ReFindOsintRoBot", "@osmosottbot", "@DepSearrchbot", "@friendly_graph_bot",
            "@BTde4_FindHomosapiensbot", "@UnderEyeruBot", "@BD_Cleaning_bot", "@Vektor_infobot",
            "@arhDetectiva_bot", "@blood_night_bot", "@AnonymousSmSTGbot", "@anubis66611bot",
            "@UniversalSearchOfBot", "@CourtProfileBot", "@ipscore_bot", "@PasswordSearchBot",
            "@geometrias_bot", "@egrul_bot", "@getfb_bot", "@FindNameVk_bot", "@faribybot",
            "@qqn28tiyac43wuuyiw0e_bot", "@SherlockSearchOsintbot", "@Numbersearch2025bot",
            "@Infogram_vvbot", "@chaosro_bot", "@Ttmlog_bot", "@breachkaaa_bot",
            "@message_searcher_tg_bot", "@kdskodko23_bot", "@SpyGGbot", "@internetanalystRoBot",
            "@OpenloadCyberBot", "@info_bazanewbot", "@itpsearch_bot", "@osintkit_search_bot",
            "@karma_cybersec_bot", "@datxpertbot", "@Surikosint_bot", "@TlgGeoEarthBot",
            "@CoyoteWatch_bot", "@Ghcrygtffunbot", "@TikTokOSINTbot", "@InfoVkUser_bot",
            "@AVttkBOT", "@avtocodbot", "@TrueCaller_Z_Bot", "@doxinghawk_bot",
            "@himmerasearchbot", "@egrul_bot", "@DiscordSensorbot", "@WhoisDomBot",
            "@DarkOfficalGlaz_Bot", "@onionsosints_bot", "@BomberSms", "@picseek_bot",
            "@metawaverobot", "@DepSearchbot", "@Enigma", "@findokobot"
        ]

        fake_responses = [
            "📍 Найден профиль в базе МВД", "🔐 Слит в даркнете", "🏠 Адрес найден",
            "👤 VK ID: 98765432", "📞 WhatsApp активен", "📸 Фото найдено", "🎮 Играет в Steam",
            "🎭 Использует прокси", "🧬 Биометрия совпадает", "💾 Участие в форумах"
        ]

        responses = []
        used = set()

        for bot in bots:
            await asyncio.sleep(2)  # перед отправкой
            await message.edit(f"📩 Отправляю запрос в {bot}...")
            await asyncio.sleep(2)  # ждем ответ (фейковый)
            reply = random.choice(fake_responses)
            if reply not in used:
                used.add(reply)
                responses.append((bot, reply))

        return responses

    def generate_pdf(self, number, bot_data):
        path = f"/tmp/dox_{random.randint(1000,9999)}.pdf"
        c = canvas.Canvas(path, pagesize=A4)
        w, h = A4
        y = h - 20 * mm

        c.setFont("DejaVu", 18)
        c.setFillColor(red)
        c.drawCentredString(w / 2, y, "🕵️ DoxTool — Фейковое досье")
        y -= 15 * mm

        c.setFont("DejaVu", 12)
        c.setFillColor(black)
        c.drawString(20 * mm, y, f"📞 Номер: {number}")
        y -= 7 * mm
        c.drawString(20 * mm, y, f"🗓️ Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 10 * mm

        for idx, (bot, info) in enumerate(bot_data, 1):
            if y < 40 * mm:
                c.showPage()
                c.setFont("DejaVu", 12)
                y = h - 20 * mm
            c.setFillColor(blue)
            c.drawString(20 * mm, y, f"{idx}. Ответ от {bot}:")
            y -= 6 * mm
            c.setFillColor(black)
            c.drawString(25 * mm, y, f"{info}")
            y -= 8 * mm

        c.setFont("DejaVu", 8)
        c.setFillColor(red)
        c.drawCentredString(w / 2, 10 * mm, "⚠️ Все данные случайны. Только для развлекательных целей.")
        c.save()
        return path