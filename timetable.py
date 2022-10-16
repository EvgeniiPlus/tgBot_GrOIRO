import os
from config import ttable_url


def show_list_timetable():
    list_ttables = os.listdir('Timetable')
    dict_ttables = {}
    for _, v in enumerate(list_ttables):
        # print(f"{v[:5]} {v.split('.')[0][6:]}")
        dict_ttables[v[:5]] = v.split('.')[0][6:]
    # print(dict_ttables)
    return dict_ttables



def get_timetable(number_PK):
    tt_list = os.listdir('Timetable')
    # print(tt_list[0].split()[0])
    for _, v in enumerate(tt_list):
        if v.split()[0] == number_PK:
            # print(number_PK)
            tt_item = v.split('.')[0]
            tt_url = f'{ttable_url}/{v}'
            # print(tt_item, tt_url)
    return [tt_item, tt_url]


    # print(f"Ваше ПК: {tt_item}\n\n"
    #       f"Ваше расписание: {tt_url} (скачать)\n")


def main():
    show_list_timetable()
    # get_timetable(input('Выберите номер Вашего ПК: '))


if __name__ == '__main__':
    main()
