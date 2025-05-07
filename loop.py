from openai import AzureOpenAI

# Azure 설정
client = AzureOpenAI(
    api_key="AmFZuaTGrztL25vymqftEVD6qMvpYtCdZpW07FW5pPWZ2C7YzVeBJQQJ99BEACHYHv6XJ3w3AAAAACOGvxnP",
    api_version="2024-12-01-preview",
    azure_endpoint="https://ginge-mac10f7n-eastus2.cognitiveservices.azure.com/"
)

deployment = "o3-mini"  # 너가 Azure에 배포한 모델 이름

# 🎯 무한 대화 루프 시작
print("🧠 감정 코칭 챗봇에 오신 것을 환영합니다. (종료하려면 '그만'이라고 입력하세요.)\n")

while True:
    user_input = input("오늘 감정 상태를 입력해 주세요:\n> ")
    
    if user_input.strip().lower() in ["그만", "exit", "quit"]:
        print("👋 감정 기록을 종료합니다. 좋은 하루 되세요!")
        break

    # GPT에 전달할 메시지
    messages = [
        {
            "role": "system",
            "content": """
                당신은 감정 코칭 챗봇입니다.
                - 사용자가 감정을 입력하면 공감하고, 상황을 물어봅니다.
                - 감정이 부정적일 경우 자동사고를 탐색하고 대체사고로 유도하세요.
                - 말투는 따뜻하고 간결하게 유지하세요.
                """
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # 응답 생성
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_completion_tokens=500,
        )

        print("\n🤖 챗봇:", response.choices[0].message.content, "\n")

    except Exception as e:
        print("⚠️ 오류가 발생했어요:", str(e))
