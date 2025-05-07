import asyncio
import os
import threading
import queue
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent as EventComment
from TikTokLive.events import FollowEvent as EventFollow
from TikTokLive.events import GiftEvent as EventGift
from gtts import gTTS
from pydub import AudioSegment
from playsound import playsound  # playsound をインポート
import tempfile
import traceback

class TikTokLiveClientWithQueue():
    def __init__(self, max_queue_size=20):
        self._queue = queue.Queue(maxsize=max_queue_size)
        self._loop = asyncio.new_event_loop()  # 新しいイベントループを作成
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

    def add_to_queue(self, text):
        try:
            self._queue.put(text, timeout=5)  # キューが満杯の場合は5秒待機
        except queue.Full:
            print("Queue is full. Dropping message:", text)

    def _run_event_loop(self):
        asyncio.set_event_loop(self._loop)  # スレッド専用のイベントループを設定
        try:
            self._loop.run_until_complete(self._process_queue())
        except Exception as e:
            print(f"Error in event loop: {e}")
            traceback.print_exc()

    async def _process_queue(self):
        while True:
            try:
                text = self._queue.get()
                print(f"Processing text: {text}")
                await speak_sync(text)
                self._queue.task_done()
            except Exception as e:
                print(f"Error processing queue: {e}")
                traceback.print_exc()

async def speak_sync(text, lang='ja'):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3_file:
            temp_mp3_path = temp_mp3_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
            temp_wav_path = temp_wav_file.name

        tts = gTTS(text=text, lang=lang)
        tts.save(temp_mp3_path)

        audio = AudioSegment.from_mp3(temp_mp3_path)
        audio.export(temp_wav_path, format="wav")

        print("Playing WAV file...")
        playsound(temp_wav_path)  # playsound を使用して再生
        print("Audio playback completed.")
    except Exception as e:
        print(f"Error during speech synthesis or playback: {e}")
        traceback.print_exc()
    finally:
        if os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

USERNAME = ""
client = TikTokLiveClient(unique_id=USERNAME)
th = TikTokLiveClientWithQueue()

@client.on(EventComment)
async def on_comment(event: EventComment):
    text = f"{event.user.nickname}さんのコメント。{event.comment}"
    print(f"Received comment: {text}")
    th.add_to_queue(text)


@client.on(EventFollow)
async def on_follow(event: EventFollow):
    text = f"{event.user.nickname}さんがフォローしました。ありがとうございます。"
    print(f"Received follow: {text}")
    th.add_to_queue(text)

@client.on(EventGift)
async def on_gift(event: EventGift):
    text = f"{event.user.nickname}さんがギフトをくれました。ありがとうございます。"
    print(f"Received gift: {text}")
    th.add_to_queue(text)


async def main():
    try:
        if not client.connected:
            print("Connecting to TikTokLive...")
            await client.start()
        await asyncio.sleep(1)
    except Exception as e:
        print("Stopping...")
        if client.connected:
            await client.disconnect()
        break

if __name__ == "__main__":
    asyncio.run(main())
