import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai._gaos.lib.compat_errors import RateLimitError
import requests

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_travel_recommendation(date_text):
    client = genai.Client()

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=f"""
    {date_text} 국내 여행지를 추천해줘.

    다음 JSON 형식으로만 답해줘.
    {{
        "recommended_cities": ["지역1", "지역2", "지역3"],
        "weather": "날씨 설명",
        "events": ["행사 또는 볼거리"],
        "reason": "추천 이유"
    }}

    설명이나 마크다운은 넣지 말고 JSON만 출력해줘.
    """
        )

    except RateLimitError:
        print("[오류] Gemini API 사용량 제한(429)에 도달했습니다.")
        print("무료 사용량 제한을 확인한 후 다시 실행하세요.")
        return None

    print("Gemini 응답:", interaction.output_text)

    try:
        recommendation = json.loads(interaction.output_text)

    except json.JSONDecodeError:
        print("[안내] Gemini 응답을 JSON으로 변환하지 못했습니다.")
        print("[안내] JSON 형식으로 다시 요청합니다.")

        try:
            retry_interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=f"""
        {date_text} 국내 여행지를 추천해줘.

        반드시 아래 JSON 형식만 출력해줘.
        다른 설명, 마크다운, 코드 블록은 절대 포함하지 마.

        {{
            "recommended_cities": ["지역1", "지역2", "지역3"],
            "weather": "날씨 설명",
            "events": ["행사 또는 볼거리"],
            "reason": "추천 이유"
        }}
         """
            )

            recommendation = json.loads(retry_interaction.output_text)

        except json.JSONDecodeError:
            print("[오류] 재시도 후에도 JSON 형식으로 변환하지 못했습니다.")
            return None

    required_keys = ["recommended_cities", "weather", "events", "reason"]

    if not all(key in recommendation for key in required_keys):
        print("[오류] Gemini 응답에 필요한 항목이 없습니다.")
        return None

    if not isinstance(recommendation["recommended_cities"], list):
        print("[오류] recommended_cities 형식이 올바르지 않습니다.")
        return None

    if not 2 <= len(recommendation["recommended_cities"]) <= 3:
        print("[오류] 추천 지역은 2~3개여야 합니다.")
        return None

    if not isinstance(recommendation["events"], list):
        print("[오류] events 형식이 올바르지 않습니다.")
        return None

    if not isinstance(recommendation["weather"], str):
        print("[오류] weather 형식이 올바르지 않습니다.")
        return None

    if not isinstance(recommendation["reason"], str):
        print("[오류] reason 형식이 올바르지 않습니다.")
        return None
    print("Python 데이터:", recommendation)

    return recommendation

def search_restaurants(city, errors):
    api_key = os.getenv("KAKAO_REST_API_KEY")

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }

    params = {
        "query": f"{city} 맛집",
        "size": 5
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            print(f"[오류] {city}: Kakao API 인증 실패 (401)")
            errors.append(f"{city}: Kakao API 인증 실패 (401)")
            return []

        if response.status_code == 403:
            print(f"[오류] {city}: Kakao API 접근 권한 없음 (403)")
            errors.append(f"{city}: Kakao API 접근 권한 없음 (403)")
            return []

        response.raise_for_status()

        data = response.json()

        if not data["documents"]:
            print(f"[안내] {city}: 검색 결과가 없습니다.")
            return []

        restaurants = []

        for place in data["documents"]:
            restaurants.append({
                "name": place["place_name"],
                "address": place["road_address_name"] or place["address_name"],
                "category": place["category_name"],
                "url": place["place_url"],
                "x": place["x"],
                "y": place["y"]
            })

        return restaurants

    except requests.RequestException as e:
        print(f"[오류] {city}: Kakao API 요청 실패 - {e}")
        errors.append(f"{city}: Kakao API 요청 실패 - {e}")
        return []

def generate_travel_report(date_text, recommendation):
    report = []

    report.append("# 국내 여행 추천")
    report.append("")
    report.append(f"- 여행 날짜: {date_text}")
    report.append("")

    report.append("## 추천 여행지와 이유")
    report.append("")

    for city in recommendation["recommended_cities"]:
        report.append(f"- **{city}**")
    report.append("")
    report.append(recommendation["reason"])
    report.append("")

    report.append("## 날씨")
    report.append("")
    report.append(recommendation["weather"])
    report.append("")

    report.append("## 행사/축제")
    report.append("")

    for event in recommendation["events"]:
        report.append(f"- {event}")
    report.append("")

    report.append("## 맛집")
    report.append("")

    for city, restaurants in recommendation["restaurants"].items():
        report.append(f"### {city}")
        report.append("")

        if not restaurants:
            report.append("- 데이터 없음")
            report.append("")
            continue

        for restaurant in restaurants:
            report.append(
                f"- **{restaurant['name']}** / "
                f"{restaurant['category']} / "
                f"{restaurant['address']}"
            )

        report.append("")

    report.append("## 1일 여행 일정")
    report.append("")
    report.append("### 오전")
    report.append("- 국내 명소와 자연 풍경을 감상합니다.")
    report.append("")
    report.append("### 오후")
    report.append("- 지역 맛집에서 점심을 먹고 주변 관광지를 둘러봅니다.")
    report.append("")
    report.append("### 저녁")
    report.append("- 여유롭게 주변 풍경을 즐긴 후 여행을 마무리합니다.")
    report.append("")

    return "\n".join(report)

def check_api_keys():
    gemini_key = os.getenv("GEMINI_API_KEY")
    kakao_key = os.getenv("KAKAO_REST_API_KEY")

    if not gemini_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print("Windows CMD에서 다음과 같이 설정하세요:")
        print("set GEMINI_API_KEY=발급받은_Gemini_API_키")
        return False

    if not kakao_key:
        print("KAKAO_REST_API_KEY가 설정되지 않았습니다.")
        print("Windows CMD에서 다음과 같이 설정하세요:")
        print("set KAKAO_REST_API_KEY=발급받은_Kakao_REST_API_키")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(
        description="국내 여행 추천 프로그램"
    )

    parser.add_argument(
        "-date",
        "--date",
        required=True,
        help="여행 날짜 (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    if not check_api_keys():
        return

    if not validate_date(args.date):
        print("오류: 날짜 형식이 올바르지 않습니다.")
        print("사용법: python travel_planner.py --date YYYY-MM-DD")
        return
    print("[1/3] 여행 날짜 확인 완료")
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    print("========================================")
    print("      [KR] 국내 여행 추천 프로그램")
    print("========================================")
    print(f"여행 날짜: {args.date}")
    print("[2/3] 여행지 추천 준비 중...")
    recommendation = get_travel_recommendation(args.date)

    if recommendation is None:
        return
    
    print(recommendation)
    print("[3/3] 맛집 검색 및 여행 리포트 준비 중...")
    recommendation["errors"] = []
    restaurant_results = {}

    for city in recommendation["recommended_cities"]:
        restaurant_results[city] = search_restaurants(city, recommendation["errors"])
    recommendation["restaurants"] = restaurant_results
    result_file = results_dir / f"{args.date}.json"

    with open(result_file, "w", encoding="utf-8") as file:
        json.dump(recommendation, file, ensure_ascii=False, indent=2)
    print(f"결과 저장: {result_file}")

    report = generate_travel_report(args.date, recommendation)
    report_file = results_dir / f"{args.date}.md"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report)
    print(f"리포트 저장: {report_file}")

    print()
    print("프로그램 기본 설정이 완료되었습니다.")


if __name__ == "__main__":
    main()
