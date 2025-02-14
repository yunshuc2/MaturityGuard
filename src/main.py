import config
from excel_parser import parse_excel
from calendar_manager import create_calendar_events
from timeline_plot import plot_timeline


def main():
    data = parse_excel()
    create_calendar_events(data)
    plot_timeline(data)
    print("处理完成！生成文件：\n- reminders.ics\n- timeline.png")

if __name__ == "__main__":
    main()