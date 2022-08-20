# Chord play Recommendation Service

코드 플레이 추천 서버입니다 V1 버전에서는 동영상 태그 데이터 정보와 자카드 유사도 알고리즘으로 사용자의 취향을 분석하고 비슷한 음악을 추천합니다.

---

## API (Version 1)

## 추천 데이터

특정 유저와 관련된 추천 데이터를 가져옵니다.

**요청 URL**

```
{recommendation_host}/recommendation
```

**요청 본문**

```
GET /{user_id}?offset={string}&limit={string}
```

**응답**

```typescript
{
  payload: {
    number: number;
    recommendation_list: [string];
  }
}
```
