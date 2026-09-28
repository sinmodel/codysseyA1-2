# 국내 여행 추천 프로그램

**과제 제출자 : 신 재 풍**

## 1. 프로그램 소개

Python으로 작성한 콘솔 기반 국내 여행 추천 프로그램입니다.

사용자가 여행 날짜를 입력하면 Gemini API를 이용하여 국내 여행지를 추천하고, Kakao Local API를 이용하여 각 추천 지역의 맛집을 검색합니다.

검색 결과를 JSON 파일로 저장하고, 추천 여행 정보와 맛집 정보를 바탕으로 Markdown 여행 리포트를 생성합니다.

---

## 2. 주요 기능

* 여행 날짜 입력 및 날짜 형식 확인
* Gemini API를 이용한 국내 여행지 추천
* 2~3개 추천 지역 제공
* 추천 지역별 날씨, 행사/볼거리, 추천 이유 생성
* Kakao Local API를 이용한 맛집 검색
* 지역별 맛집 최대 5개 검색
* 맛집 이름, 주소, 카테고리, URL, 위치 정보 저장
* API 오류 및 예외 상황 처리
* Gemini JSON 변환 실패 시 1회 재시도
* 실행 결과를 날짜별 JSON 파일로 저장
* 날짜별 Markdown 여행 리포트 생성

---

## 3. 개발 환경

* Python 3.10 이상
* Visual Studio Code
* Git
* Gemini API
* Kakao Local API

---

## 4. API를 이해하기

API(Application Programming Interface)는 프로그램과 외부 서비스가 정해진 규칙에 따라 데이터를 주고받을 수 있도록 연결해 주는 방법입니다.

API는 여러 방식으로 구분할 수 있지만, 이 프로젝트에서는 **사용 목적을 기준으로 두 가지 역할**로 나누어 이해합니다.

### 1) LLM API

LLM API는 대규모 언어 모델(LLM)을 프로그램에서 사용할 수 있도록 연결하는 API입니다.

주요 사용 용도:

* 질문에 대한 답변 생성
* 내용 요약
* 여행지 추천
* 여행 일정 작성
* 자연어 콘텐츠 생성

대표적인 서비스:

#### OpenAI API

OpenAI가 제공하는 생성형 AI API입니다.

프로그램에서 AI 모델을 호출하여 텍스트 생성 및 다양한 AI 기능을 활용할 수 있습니다.

#### Google Gemini API

Google의 Gemini 모델을 프로그램에서 사용할 수 있도록 제공하는 API입니다.

이 프로젝트에서는 Gemini API를 사용하여 여행지를 추천하고 여행 관련 내용을 생성합니다.

### 2) 장소 검색용 REST API

REST API는 HTTP 요청을 이용하여 서버와 데이터를 주고받는 일반적인 API 설계 방식입니다.

이 프로젝트에서는 REST API를 이용하여 **실제 장소 및 업체 검색 데이터**를 가져옵니다.

주요 사용 용도:

* 지역 및 장소 검색
* 음식점 검색
* 주소 및 위치 정보 조회
* 좌표 정보 확인
* 검색 결과를 프로그램에서 활용

대표적인 서비스:

#### Kakao Local API

Kakao Developers에서 제공하는 장소 검색 API입니다.

장소의 이름, 주소, 카테고리, 좌표 및 장소 URL 등의 정보를 검색할 수 있습니다.

이 프로젝트에서는 추천 여행 지역을 검색어로 사용하여 맛집 정보를 가져옵니다.

#### Naver 지역 검색 API

Naver 검색 API에서 제공하는 지역 검색 기능입니다.

지역 및 업체 검색 결과를 프로그램에서 활용할 수 있습니다.

### API 종류를 구분할 때 주의할 점

LLM API와 REST API는 서로 완전히 별개의 기술이라고 보기보다는 **서로 다른 기준으로 설명할 수 있는 개념**입니다.

예를 들어 LLM API도 REST 방식으로 호출할 수 있습니다.

따라서 이 프로젝트에서는 이해하기 쉽도록 다음과 같이 역할 중심으로 구분합니다.

```text
LLM API
→ AI가 여행지 추천과 내용을 생성

장소 검색 REST API
→ 실제 장소와 맛집 데이터를 검색
```

---

## 5. API 키 보안 주의사항

API 키는 외부 서비스에 프로그램을 사용할 권한을 확인하기 위한 중요한 인증 정보입니다.

이 README에서 말하는 **“마스터 키”는 초보자의 이해를 돕기 위한 표현**이며, 실제 서비스에서는 API Key, REST API Key, Client ID, Client Secret 등 서비스별 공식 명칭을 사용합니다.

API 키를 다른 사람에게 공개하거나 GitHub와 같은 공개 저장소에 올리지 않도록 주의해야 합니다.

API 키를 다음 위치에 직접 입력하지 않습니다.

* Python 코드
* README.md
* GitHub에 업로드하는 결과 파일
* 공개된 이미지나 화면 캡처

API 키는 환경 변수 또는 `.env` 파일 등을 이용하여 별도로 관리합니다.

`.env` 파일을 사용하는 경우 Git에 올라가지 않도록 `.gitignore`에 추가해야 합니다.

```text
.env
__pycache__/
*.pyc
```

실습 환경에서 API 키를 설정하더라도 **다른 교육생에게 키 값을 그대로 보여주지 않는 것**이 중요합니다.

API 키가 노출되었다고 판단되면 해당 서비스의 관리 화면에서 키를 확인하고 필요한 보안 조치를 취합니다.

---

## 6. API 키 발급 및 제공받는 절차

API를 사용하려면 먼저 해당 서비스의 개발자 사이트에서 계정을 만들거나 로그인하고, 사용할 API에 필요한 인증 정보를 발급받아야 합니다.

서비스마다 발급 방법과 인증 정보의 이름이 다릅니다.

초보자는 아래 표를 먼저 확인하면 각 API의 전체 흐름을 쉽게 이해할 수 있습니다.

### API 발급 절차 비교표

| 서비스               | 주요 용도                | 발급 또는 인증 정보               | 일반적인 발급 순서                                                                    |
| ----------------- | -------------------- | ------------------------- | ----------------------------------------------------------------------------- |
| OpenAI API        | LLM, 텍스트·이미지 등 AI 기능 | API Key                   | OpenAI 계정 로그인 → API 관리 화면 → API Key 생성 → 안전하게 보관 → 환경 변수 등록                   |
| Google Gemini API | LLM, 콘텐츠 생성 및 분석     | API Key                   | Google AI Studio 로그인 → API Keys 화면 → API Key 생성 또는 확인 → 안전하게 보관 → 환경 변수 등록    |
| Naver 검색/지역 API   | 검색 및 지역·업체 정보 조회     | Client ID + Client Secret | Naver 개발자 센터 로그인 → 애플리케이션 등록 → 사용할 API 설정 → Client ID/Secret 확인 → 환경 변수 등록    |
| Kakao Local API   | 장소·맛집 검색 및 위치 정보 조회  | REST API Key              | Kakao Developers 가입/로그인 → 앱 생성 → Platform Key 확인 → REST API Key 확인 → 환경 변수 등록 |

> 주의: 위 표는 초보자를 위한 **일반적인 발급 흐름**입니다. 서비스의 화면 구성과 정책은 변경될 수 있으므로 실제 발급 시 해당 서비스의 최신 공식 문서를 확인합니다.

### 1) OpenAI API

OpenAI API는 API 관리 화면에서 API Key를 생성하여 사용합니다.

일반적인 순서:

```text
OpenAI 로그인
    ↓
API 관리 화면
    ↓
API Key 생성
    ↓
키 안전하게 보관
    ↓
OPENAI_API_KEY 환경 변수 등록
```

### 2) Google Gemini API

Google AI Studio에서는 Gemini API Key를 관리할 수 있습니다.

일반적인 순서:

```text
Google AI Studio 로그인
    ↓
API Keys 화면
    ↓
API Key 확인 또는 생성
    ↓
키 안전하게 보관
    ↓
GEMINI_API_KEY 환경 변수 등록
```

### 3) Naver 검색/지역 API

Naver Open API를 사용하려면 개발자 센터에서 애플리케이션을 등록하고 Client ID와 Client Secret을 발급받아야 합니다.

일반적인 순서:

```text
Naver 개발자 센터 로그인
    ↓
애플리케이션 등록
    ↓
사용할 검색 API 설정
    ↓
Client ID / Client Secret 확인
    ↓
안전하게 보관
    ↓
환경 변수 등록
```

### 4) Kakao Local API

Kakao API를 사용하려면 Kakao Developers에서 개발자 계정으로 로그인하고 앱을 생성한 후 앱의 Platform Key에서 REST API Key를 확인합니다.

일반적인 순서:

```text
Kakao Developers 로그인
    ↓
앱 생성
    ↓
Platform Key 확인
    ↓
REST API Key 확인
    ↓
안전하게 보관
    ↓
KAKAO_REST_API_KEY 환경 변수 등록
```

---

## 7. API 키 설정

API 키는 Python 코드나 README.md에 직접 입력하지 않습니다.

Windows CMD에서 환경 변수로 설정합니다.

### Gemini API 키

```cmd
set GEMINI_API_KEY=발급받은_Gemini_API_키
```

### Kakao REST API 키

```cmd
set KAKAO_REST_API_KEY=발급받은_Kakao_REST_API_키
```

OpenAI 또는 Naver API를 사용할 경우에도 같은 원칙으로 환경 변수에 저장합니다.

예:

```text
OPENAI_API_KEY
NAVER_CLIENT_ID
NAVER_CLIENT_SECRET
```

설정한 환경 변수는 현재 CMD 창에서 사용할 수 있습니다.

API 키가 설정되지 않은 경우 프로그램은 API 호출 전에 안내 메시지를 출력하고 종료합니다.

---

## 8. 실행 방법

프로젝트 폴더에서 다음 명령어를 실행합니다.

```text
python travel_planner.py --date 2026-10-15
```

또는 다음과 같이 사용할 수 있습니다.

```text
python travel_planner.py -date 2026-10-15
```

날짜는 `YYYY-MM-DD` 형식으로 입력합니다.

---

## 9. 결과 파일

프로그램 실행 결과는 `results` 폴더에 날짜별로 저장됩니다.

예:

```text
results/
├── 2026-10-15.json
└── 2026-10-15.md
```

### JSON 파일

JSON 파일에는 다음 정보가 저장됩니다.

* recommended_cities
* weather
* events
* reason
* restaurants
* errors

추천 지역별 맛집 검색 결과도 함께 저장됩니다.

### Markdown 파일

Markdown 파일에는 다음 항목이 포함됩니다.

* 추천 여행지와 이유
* 날씨
* 행사/축제
* 지역별 맛집
* 1일 여행 일정

  * 오전
  * 오후
  * 저녁

---

## 10. 오류 처리

프로그램 실행 중 문제가 발생하더라도 가능한 범위에서 프로그램이 계속 진행되도록 예외 처리를 적용했습니다.

### Gemini API

Gemini 응답을 JSON으로 변환하지 못하면 JSON 형식으로 한 번 더 요청합니다.

두 번째 요청에서도 JSON 변환에 실패하면 오류 메시지를 출력하고 프로그램을 종료합니다.

### Kakao Local API

다음 오류를 처리합니다.

* 401: API 인증 실패
* 403: API 접근 권한 없음
* 네트워크 및 요청 오류

맛집 검색 결과가 없는 경우에는 오류로 처리하지 않고 데이터가 없는 상태로 계속 진행합니다.

발생한 API 오류는 `errors` 항목에 기록합니다.

---

## 11. 프로젝트 파일 구조

```text
travel_planner/
├── travel_planner.py
├── README.md
├── README_SJP.md
├── .gitignore
└── results/
    ├── YYYY-MM-DD.json
    └── YYYY-MM-DD.md
```

`results` 폴더의 JSON 파일은 API 결과와 프로그램 처리 결과를 확인하는 데 사용할 수 있으며, Markdown 파일은 최종 여행 리포트로 확인할 수 있습니다.

---

## 12. 프로젝트 목적

이 프로젝트는 Python에서 외부 API를 활용하는 방법을 학습하고, API 응답 데이터를 JSON으로 처리한 후 다른 API의 검색 결과와 결합하여 최종 결과물을 만드는 것을 목적으로 합니다.

또한 예외 처리, 환경 변수 관리, JSON 파일 저장, Markdown 파일 생성, Git 버전 관리 등을 함께 실습할 수 있도록 구성했습니다.
