import argparse
import json
from datetime import datetime
from pathlib import Path


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_travel_recommendation(date_text):
    recommendation = {
        "recommended_cities": [
            "대전",
            "공주",
            "청주"
        ],
        "weather": "맑고 선선한 가을 날씨",
        "events": [
            "가을 단풍 명소 방문"
        ],
        "reason": "가을 풍경과 자연을 즐기기 좋은 지역을 추천했습니다."
    }

    return recommendation

def search_restaurants(city):
    restaurants = {
        "대전": [
            {
                "name": "대전 맛집 1",
                "address": "대전광역시 중구",
                "category": "한식",
                "url": "",
                "x": "127.3845",
                "y": "36.3504"
            },
            {
                "name": "대전 맛집 2",
                "address": "대전광역시 서구",
                "category": "한식",
                "url": "",
                "x": "127.3680",
                "y": "36.3550"
            }
        ],
        "공주": [
            {
                "name": "공주 맛집 1",
                "address": "충청남도 공주시",
                "category": "한식",
                "url": "",
                "x": "127.1190",
                "y": "36.4465"
            },
            {
                "name": "공주 맛집 2",
                "address": "충청남도 공주시",
                "category": "한식",
                "url": "",
                "x": "127.1100",
                "y": "36.4500"
            }
        ],
        "청주": [
            {
                "name": "청주 맛집 1",
                "address": "충청북도 청주시",
                "category": "한식",
                "url": "",
                "x": "127.4890",
                "y": "36.6424"
            },
            {
                "name": "청주 맛집 2",
                "address": "충청북도 청주시",
                "category": "한식",
                "url": "",
                "x": "127.4850",
                "y": "36.6350"
            }
        ]
    }

    return restaurants.get(city, [])

def generate_travel_report(date_text, recommendation):
    report = []

    report.append("# 국내 가을 여행 추천")
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
    report.append("- 가을 단풍 명소와 자연 풍경을 감상합니다.")
    report.append("")
    report.append("### 오후")
    report.append("- 지역 맛집에서 점심을 먹고 주변 관광지를 둘러봅니다.")
    report.append("")
    report.append("### 저녁")
    report.append("- 여유롭게 주변 풍경을 즐긴 후 여행을 마무리합니다.")
    report.append("")

    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="대전 중심 국내 가을 여행 추천 프로그램"
    )

    parser.add_argument(
        "-date",
        "--date",
        required=True,
        help="여행 날짜 (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    if not validate_date(args.date):
        print("오류: 날짜 형식이 올바르지 않습니다.")
        print("사용법: python travel_planner.py --date YYYY-MM-DD")
        return

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    print("========================================")
    print("     🍁 대전 가을 여행 추천 프로그램")
    print("========================================")
    print(f"여행 날짜: {args.date}")
    
    recommendation = get_travel_recommendation(args.date)
    print(recommendation)

    restaurant_results = {}

    for city in recommendation["recommended_cities"]:
        restaurant_results[city] = search_restaurants(city)

    recommendation["restaurants"] = restaurant_results
    recommendation["errors"] = []

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
    print("[1/3] 여행 날짜 확인 완료")
    print("[2/3] 여행지 추천 준비 중...")
    print("[3/3] 맛집 검색 및 여행 리포트 준비 중...")
    print()
    print("프로그램 기본 설정이 완료되었습니다.")


if __name__ == "__main__":
    main()
