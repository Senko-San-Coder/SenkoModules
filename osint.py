from hikkatl.types import Message
from hikkatl.utils import get_display_name
from hikkatl.errors import RPCError
import asyncio
import os
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Список ботов
bots = [
    "@InfinitySearcch_bot", "@FastSearch66_bot", "@fasthlr_bot", "@mnp_bot", "@Search",
    "@slb_infa_ibot", "@ReFindOsintRoBot", "@osmosottbot", "@DepSearrchbot", "@friendly_graph_bot",
    "@BTde4_FindHomosapiensbot", "@UnderEyeruBot", "@BD_Cleaning_bot", "@Vektor_infobot", "@arhDetectiva_bot",
    "@blood_night_bot", "@AnonymousSmSTGbot", "@UniversalSearchOfBot", "@CourtProfileBot", "@ipscore_bot",
    "@PasswordSearchBot", "@geometrias_bot", "@egrul_bot", "@getfb_bot", "@FindNameVk_bot",
    "@faribybot", "@qqn28tiyac43wuuyiw0e_bot", "@SherlockSearchOsintbot", "@Numbersearch2025bot", "@Infogram_vvbot",
    "@chaosro_bot", "@Ttmlog_bot", "@breachkaaa_bot", "@message_searcher_tg_bot", "@kdskodko23_bot",
    "@SpyGGbot", "@internetanalystRoBot", "@OpenloadCyberBot", "@info_bazanewbot", "@itpsearch_bot",
    "@osintkit_search_bot", "@karma_cybersec_bot", "@datxpertbot", "@Surikosint_bot", "@TlgGeoEarthBot",
    "@CoyoteWatch_bot", "@Ghcrygtffunbot", "@TikTokOSINTbot", "@InfoVkUser_bot", "@AVttkBOT",
    "@avtocodbot", "@TrueCaller_Z_Bot", "@doxinghawk_bot", "@DiscordSensorbot", "@WhoisDomBot",
    "@onionsosints_bot", "@BomberSms", "@picseek_bot", "@metawaverobot", "@DepSearchbot",
    "@Enigma", "@findokobot"
]

# Глобальные переменные
request_count = {}

@loader.tds
class DoxModule(loader.Module):
    """Модуль для OSINT-досье по номеру телефона"""
    
    strings = {"name": "Dox", "help": "Используйте .dox +79999999999 для создания OSINT-досье."}
    
    async def doxcmd(self, message: Message):
        user_id = message.sender_id
        current_time = time.time()
        
        if user_id not in request_count:
            request_count[user_id] = {"count": 0, "last_reset": current_time}
        
        if current_time - request_count[user_id]["last_reset"] > 86400:
            request_count[user_id] = {"count": 0, "last_reset": current_time}
        
        if request_count[user_id]["count"] >= 3:
            await utils.answer(message, "Лимит запросов (3 в день) исчерпан. Попробуйте завтра.")
            return
        
        phone = utils.get_args_raw(message)
        if not phone or not phone.startswith("+") or not phone[1:].isdigit():
            await utils.answer(message, "Используйте команду в формате: .dox +79999999999")
            return
        
        request_count[user_id]["count"] += 1
        await utils.answer(message, f"Запуск поиска для {phone}...")
        
        responses = {}
        chat = await self._client.get_entity(message.chat_id)
        for bot in bots:
            try:
                await self._client.send_message(bot, phone)
                time.sleep(2)  # Задержка 2-3 секунды
                response = await self._client.get_messages(bot, limit=1)
                if response and response[0].text:
                    responses[bot] = response[0].text
                time.sleep(1)  # Дополнительная задержка
            except RPCError:
                continue
            await asyncio.sleep(2)  # Ждём 2 секунды на ответ
        
        # Удаление дубликатов и сортировка
        unique_responses = list(dict.fromkeys(responses.values()))
        unique_responses.sort()  # Сортировка по алфавиту
        
        # Генерация PDF
        pdf_file = f"dox_{user_id}_{int(current_time)}.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            name='CustomStyle',
            parent=styles['BodyText'],
            fontSize=12,
            leading=16,
            textColor=colors.black
        )
        elements = []
        
        elements.append(Paragraph("OSINT Досье", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Номер телефона: {phone}", custom_style))
        elements.append(Spacer(1, 12))
        
        for i, response in enumerate(unique_responses, 1):
            elements.append(Paragraph(f"Источник {i}: {response}", custom_style))
            elements.append(Spacer(1, 12))
        
        doc.build(elements)
        with open(pdf_file, 'rb') as f:
            await self._client.send_file(chat, f, caption="OSINT Досье готово!")
        
        os.remove(pdf_file)