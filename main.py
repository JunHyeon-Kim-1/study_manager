import json
import calendar
from datetime import datetime


# ==============================
# JSON 파일 불러오기
# ==============================

def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # JSON이 딕셔너리가 아닌 경우
        if not isinstance(data, dict):
            print("data.json의 형식이 잘못되었습니다.")
            return {"data": []}

        # data 항목이 없는 경우
        if "data" not in data:
            print("data.json에 'data' 항목이 없습니다.")
            return {"data": []}

        # data가 리스트가 아닌 경우
        if not isinstance(data["data"], list):
            print("data.json의 데이터 형식이 잘못되었습니다.")
            return {"data": []}

        return data

    except FileNotFoundError:
        print("data.json 파일이 없어 새로 생성합니다.")
        return {"data": []}

    except json.JSONDecodeError:
        print("data.json의 형식이 잘못되었습니다.")
        return {"data": []}


# ==============================
# JSON 파일 저장
# ==============================

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ==============================
# 이번 달 공부 현황
# ==============================

def show_calendar(data):

    today = datetime.today()

    year = today.year
    month = today.month
    today_day = today.day

    print()
    print(f"========== {year}년 {month}월 공부 현황 ==========")
    print("일   월   화   수   목   금   토")

    month_calendar = calendar.monthcalendar(year, month)

    for week in month_calendar:

        for day in week:

            # 해당 월이 아닌 빈칸
            if day == 0:
                print("     ", end="")
                continue

            # 아직 오지 않은 날짜
            if day > today_day:
                print("     ", end="")
                continue

            date = f"{year}-{month:02d}-{day:02d}"

            studied = False

            for item in data["data"]:

                if not isinstance(item, dict):
                    continue

                if item.get("date") == date:
                    studied = True
                    break

            if studied:
                print(f"{day:2d}● ", end="")
            else:
                print(f"{day:2d}○ ", end="")

        print()

    print()
    print("● = 공부함")
    print("○ = 공부하지 않음")


# ==============================
# 날짜별 공부 기록 보기
# ==============================

def show_day(data):

    date = input("확인할 날짜 (YYYY-MM-DD): ").strip()

    # 빈 입력
    if date == "":
        print("날짜를 입력해야 합니다.")
        return

    # 날짜 형식 확인
    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        print("잘못된 날짜입니다.")
        print("YYYY-MM-DD 형식으로 입력하세요.")
        return

    records = []

    for item in data["data"]:

        if not isinstance(item, dict):
            continue

        if item.get("date") == date:
            records.append(item)

    print()
    print(f"========== {date} 공부 기록 ==========")

    if not records:
        print("이 날짜에는 공부 기록이 없습니다.")
        return

    for index, item in enumerate(records, start=1):

        print(f"{index}. 과목명 : {item.get('subject', '과목명 없음')}")
        print(f"   내용   : {item.get('content', '내용 없음')}")
        print("-" * 30)


# ==============================
# 공부 기록 추가
# ==============================

def add_study(data):

    today = datetime.today().strftime("%Y-%m-%d")

    print()
    print(f"오늘 날짜: {today}")

    date = input(
        "공부 날짜를 입력하세요 "
        "(Enter = 오늘 날짜): "
    ).strip()

    # Enter를 누르면 오늘 날짜
    if date == "":
        date = today

    # 날짜 검사
    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        print("잘못된 날짜입니다.")
        print("YYYY-MM-DD 형식으로 입력하세요.")
        return

    subject = input("과목명: ").strip()
    content = input("공부 내용: ").strip()

    # 과목명 검사
    if subject == "":
        print("과목명을 입력해야 합니다.")
        return

    # 내용 검사
    if content == "":
        print("공부 내용을 입력해야 합니다.")
        return

    new_data = {
        "subject": subject,
        "content": content,
        "date": date
    }

    # 기존 데이터에 추가
    data["data"].append(new_data)

    # JSON 저장
    save_data(data)

    print()
    print("공부 기록이 저장되었습니다.")


# ==============================
# 공부 기록 삭제
# ==============================

def delete_study(data):

    date = input("삭제할 날짜 (YYYY-MM-DD): ").strip()

    # 빈 입력
    if date == "":
        print("날짜를 입력해야 합니다.")
        return

    # 날짜 검사
    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        print("잘못된 날짜입니다.")
        print("YYYY-MM-DD 형식으로 입력하세요.")
        return

    # 해당 날짜의 기록 찾기
    records = []

    for index, item in enumerate(data["data"]):

        if not isinstance(item, dict):
            continue

        if item.get("date") == date:
            records.append((index, item))

    print()

    # 기록이 없는 경우
    if not records:
        print(f"{date}에는 공부 기록이 없습니다.")
        return

    print(f"========== {date} 공부 기록 ==========")

    for number, (index, item) in enumerate(records, start=1):

        print(f"{number}. 과목명 : {item.get('subject', '과목명 없음')}")
        print(f"   내용   : {item.get('content', '내용 없음')}")
        print("-" * 30)

    # 삭제할 기록 선택
    try:
        choice = input("삭제할 번호 (Enter = 취소): ").strip()

        if choice == "":
            print("삭제를 취소했습니다.")
            return

        choice = int(choice)

    except ValueError:
        print("번호를 숫자로 입력하세요.")
        return

    # 번호 범위 확인
    if choice < 1 or choice > len(records):
        print("존재하지 않는 번호입니다.")
        return

    # 실제 JSON 리스트의 위치
    delete_index = records[choice - 1][0]
    delete_item = records[choice - 1][1]

    subject = delete_item.get("subject", "과목명 없음")

    # 삭제 확인
    confirm = input(
        f"'{subject}' 공부 기록을 삭제하시겠습니까? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("삭제를 취소했습니다.")
        return

    # 데이터 삭제
    data["data"].pop(delete_index)

    # JSON 저장
    save_data(data)

    print("공부 기록이 삭제되었습니다.")


# ==============================
# 메인 프로그램
# ==============================

data = load_data()


while True:

    print()
    print("========== 공부 관리 프로그램 ==========")
    print("1. 캘린더 보기")
    print("2. 공부 기록 추가")
    print("3. 날짜별 공부 기록 보기")
    print("4. 공부 기록 삭제")
    print("5. 종료")

    choice = input("선택: ").strip()

    # 빈 입력
    if choice == "":
        continue

    # 캘린더
    if choice == "1":
        show_calendar(data)

    # 공부 기록 추가
    elif choice == "2":
        add_study(data)

    # 날짜별 기록
    elif choice == "3":
        show_day(data)

    # 기록 삭제
    elif choice == "4":
        delete_study(data)

    # 종료
    elif choice == "5":
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 선택입니다.")