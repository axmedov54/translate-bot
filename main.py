import asyncio
import logging
import sys
import os
from googletrans import Translator
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Translate
from config import token, text_to_speech
from buttons import menu, voice

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
tarjomion = Translator()

@dp.message(Command('start'))
async def StartCommand(messaga: types.Message, state: FSMContext):
    await state.set_state(Translate.lang)
    await messaga.answer("Assalomu alaykum translateda birini tanlang: ", reply_markup=menu)
# fdsafas

@dp.message(Translate.lang)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    t_lang = message.text
    await state.update_data(
        {'t_lang':t_lang}
    )
    await message.answer("Translate qilmoqchi textni kiriting ?")
    await state.set_state(Translate.trans)

@dp.message(Translate.trans)
async def TransCommand(message: types.Message, state: FSMContext):
    translate_text = message.text
    await state.update_data(
    {'translate_text':translate_text}
        )
    data = await state.get_data()
    t_lang = data.get('t_lang')
    if t_lang == "🇺🇿 Uzb - 🇬🇧 Eng":
        tarjima = tarjomion.translate(translate_text, dest="en")
        await message.answer(tarjima.text, reply_markup=voice)
        text_to_speech(tarjima.text, lang="en")
    elif t_lang == "🇬🇧 Eng - 🇺🇿 Uzb":
        tarjima = tarjomion.translate(translate_text, dest="uz")
        await message.answer(tarjima.text, reply_markup=voice)
        text_to_speech(tarjima.text, lang="tr")
    elif t_lang == "🇺🇿 Uzb - 🇷🇺 Rus":
        tarjima = tarjomion.translate(translate_text, dest="ru")
        await message.answer(tarjima.text, reply_markup=voice)
        text_to_speech(tarjima.text, lang="ru")
    elif t_lang == "🇷🇺 Rus - 🇺🇿 Uzb":
        tarjima = tarjomion.translate(translate_text, dest="uz")
        await message.answer(tarjima.text, reply_markup=voice)
        text_to_speech(tarjima.text, lang="tr")
    await state.set_state(Translate.audio)

@dp.callback_query(Translate.audio)
async def AudioCommand(call: types.CallbackQuery, state: FSMContext):
    audio = types.FSInputFile(path='audio.mp3', filename='audio.mp3')
    await call.message.answer_audio(audio=audio)
    os.remove('audio.mp3')
    await state.set_state(Translate.lang)



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())