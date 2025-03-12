import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/notifications/"  # WebSocket manzili
    print("WebSocket ulanishga harakat qilmoqda...")

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket muvaffaqiyatli ulandi!\n")

            xabarlar = []  # Xabarlarni saqlash uchun ro‘yxat
            
            # WebSocket orqali kelayotgan xabarlarni olish
            for _ in range(5):  # 5 ta xabarni kutish
                response = await websocket.recv()
                data = json.loads(response)
                xabarlar.append(data)
                print(f"📩 Olingan xabar #{len(xabarlar)}: {data}")

            # Agar xabar bo'lsa, umumiy sonini chiqaramiz
            if xabarlar:
                print(f"\n📊 Jami qabul qilingan xabarlar soni: {len(xabarlar)}")
            else:
                print("\n🚫 Hech qanday xabar kelmadi.")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")

# Skriptni ishga tushirish
asyncio.run(test_websocket())
