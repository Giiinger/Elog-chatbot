import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# ✅ .env 파일 로드
load_dotenv()

# ✅ 환경변수 불러오기
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_ENDPOINT = os.getenv("AZURE_API_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Azure OpenAI 클라이언트 설정
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version = "2024-12-01-preview",
    azure_endpoint=AZURE_API_ENDPOINT
)
deployment = AZURE_DEPLOYMENT_NAME

# ✅ 사용자별 감정 로그 저장
user_logs = {}

# ✅ GPT 응답 생성 함수
def get_gpt_response(user_id: int, user_input: str):
    history = user_logs.get(user_id, [])
    history.append({"role": "user", "content": user_input})

    messages = [{"role": "system", "content": "당신은 감정 코칭 챗봇입니다. 사용자의 기분에 공감하고, 따뜻한 피드백을 주세요."}]
    messages += history[-6:]  # 최근 대화만 유지

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=4096,
        temperature = 1.0,
        top_p = 1.0
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    user_logs[user_id] = history

    return reply

# ✅ 메시지 처리 핸들러
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text
    reply = get_gpt_response(user_id, user_input)
    await update.message.reply_text(reply)

# ✅ /start 명령어 응답
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("안녕하세요! 오늘 기분이 어떤가요?")

# ✅ 메인 실행 함수
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
