---
description: 캐릭터를 쉽게 고르는 간단 도움말
---
`scripts/catalog.json`을 읽되 내부 축 목록은 기본 도움말에 노출하지 마세요. 캐릭터를 `웃기게`, `동물`, `판타지`, `전문가`, `애니` 팩으로 묶어 표시하고 다음 사용법만 먼저 안내하세요.

```text
/with-character:set dog
/with-character:set orangutan pure
/with-character:set caveman
/with-character:set random comedy
```

`subtitle`은 캐릭터 언어+통역, `pure`는 통역 없는 순수 개그, `reaction`은 정상 설명+짧은 캐릭터 반응이라고 한 줄씩 설명하세요. 고급 조합은 사용자가 요청할 때만 별도 안내하세요.
