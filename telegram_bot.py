import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from agent_graph import graph

#Đọc bot token
load_dotenv()

#whitelist
TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

ALLOWED_USER_ID = int(
    os.getenv("TELEGRAM_ALLOWED_USER_ID")
)



#===========
#Tạo lệnh /start
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id

    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text(
            "Bạn không có quyền sử dụng bot này."
        )
        return

    await update.message.reply_text(
        "Xin chào! Tôi là Trisagent."
    )



#===========
#gửi tin nhắn đến agent
async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id

    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text(
            "Bạn không có quyền sử dụng bot này."
        )
        return

    user_input = update.message.text
    chat_id = update.effective_chat.id

    print(f"\n[TELEGRAM] Nhận: {user_input}")

    # code xử lý Agent phía dưới giữ nguyên

    config = {
        "configurable": {
            "thread_id": str(chat_id)
        }
    }

    print("[AGENT] Bắt đầu xử lý...")

    try:

        result = graph.invoke(
            {
                "messages": [
                    ("user", user_input)
                ]
            },
            config=config
        )

        print("[AGENT] Xử lý xong.")

        final_message = result["messages"][-1]

        if isinstance(final_message.content, list):

            answer = ""

            for block in final_message.content:

                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    answer += block["text"]

        else:
            answer = final_message.content

        print("[TELEGRAM] Đang gửi câu trả lời...")

        await update.message.reply_text(answer)

        print("[TELEGRAM] Đã gửi.")

    except Exception as e:

        print(f"[ERROR] {type(e).__name__}: {e}")

        await update.message.reply_text(
            "Trisagent gặp lỗi khi xử lý yêu cầu."
        )


#===========
#khởi động agent
def main():

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Trisagent đang chạy...")

    app.run_polling()


if __name__ == "__main__":
    main()
