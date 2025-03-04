from youtubesearchpython import VideosSearch
import os
from os import path
import random
import asyncio
import shutil
from time import time
import yt_dlp
from .. import converter
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from Yukki import (app, BOT_USERNAME, BOT_ID)
from ..YukkiUtilities.tgcallsrun import (yukki, convert, download, clear, get, is_empty, put, task_done, smexy)
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.database.onoff import (is_on_off, add_on, add_off)
from Yukki.YukkiUtilities.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from Yukki.YukkiUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Yukki.YukkiUtilities.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from Yukki.YukkiUtilities.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from Yukki.YukkiUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from ..config import DURATION_LIMIT, ASS_ID
from ..YukkiUtilities.helpers.decorators import errors
from ..YukkiUtilities.helpers.filters import command, other_filters
from ..YukkiUtilities.helpers.gets import (get_url, themes, random_assistant)
from ..YukkiUtilities.helpers.thumbnails import gen_thumb
from ..YukkiUtilities.helpers.chattitle import CHAT_TITLE
from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from ..YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, )


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",]   


@Client.on_message(command(["playlist", "playlist@VeezMegaBot"]) & other_filters)
async def start_playlist_cmd(_, message):
    thumb ="cache/playlist.png"
    await message.reply_photo(
    photo=thumb, 
    caption=("**❓ Which playlist do you want to play ?**"),    
    reply_markup=play_list_keyboard) 
    return 


@Client.on_message(command(["delmyplaylist", "delmyplaylist@VeezMegaBot"]) & other_filters)
async def delmyplaylist(_, message):
    usage = ("usage:\n\n/delmyplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delmyplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"💡 **Confirmation** !!\n\nAre you sure want to delete your whole playlist ?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("You not have playlist on database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"✅ Deleted the {count} music in playlist")
                else:
                    return await message.reply_text("no such saved music in playlist !")                                
        await message.reply_text("You not have such music in playlist !")                             


@Client.on_message(command(["delchatplaylist", "delchatplaylist@VeezMegaBot"]) & other_filters)
async def delchatplaylist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("You're missing admin rights to use this command.\n\n» ❌ can_manage_voice_chats")
    usage = ("usage:\n\n/delchatplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delchatplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 21:
        return await message.reply_text(f"💡 Confirmation !\n\nAre you sure want to delete your whole Group playlist ?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("Group's has no playlist on database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"**✅ Deleted the {count} music in group's playlist**")
                else:
                    return await message.reply_text(f"**no such saved music in group playlist !**")                                
        await message.reply_text("You not have such music in Group's playlist !")
