---
description: 캐릭터를 쉽게 고르는 간단 도움말
---
`scripts/catalog.json`의 프리셋을 팩별로 보여주되 내부 축 전체는 기본 도움말에 노출하지 마세요. 다음 네 단계를 먼저 안내하세요.

```text
/with-character:set dog                     # 프리셋
/with-character:set random                  # 검증된 프리셋 랜덤
/with-character:set dog chaos               # dog 기반 일부 혼돈 조합
/with-character:set chaos random            # 축 단위 완전 랜덤
/with-character:set 강아지를 로봇으로 바꿔줘   # 자연어 상세 설정
/with-character:set 건달이                    # 헴 프리셋
/with-character:set 쿠데레                    # 애니 11종 중 하나
/with-character:set random comedy
/with-character:set random fantasy
```

`random`은 완성된 프리셋 중 선택하고 `chaos random`은 완전 조합이라는 차이를 강조하세요. 상세 축과 말하기 모드는 사용자가 "상세 설정 보여줘"라고 요청할 때만 안내하세요.
