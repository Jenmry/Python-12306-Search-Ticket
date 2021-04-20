#!usr/bin/python
# -*- coding = utf-8 -*-
"""
@author: Jenmry
@time: 2021/4/16
@tool: Pycharm2020.3
"""

import requests
from StationInfo import stations
from pprint import pprint
import sys


class Ticket(object):

    def __init__(self, _date, _from, _to):
        self.url1 = 'https://kyfw.12306.cn/otn/leftTicket/query'
        self.url2 = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        self.url3 = 'https://kyfw.12306.cn/otn/login/checkUser'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77',
            # 'Cookie': input('请输入Cookie值：') # 可以自行选择方式 以下cookie值可能会失效
            'Cookie': '_uab_collina=161857219977662805771049; JSESSIONID=179028BD1AE5EF6B5C79C7E2E89A1B1F; RAIL_EXPIRATION=1618754109893; RAIL_DEVICEID=OGkyA3C7P75lIY83O6RitBP7zfKLGhAk3z8JqXPWJ7nEGNifu9htdPZEMrPW5r3iyXueDCpbIYnkfCDZgBWaRXhQ1AwNZjRMUIsUusZ6ka2OJTmfk2Ulv2toyeTjnj04OGPrqXHeNt5Yz-T-LUnXPUkslkwUBujh; _jc_save_wfdc_flag=dc; _jc_save_toDate=2021-04-17; BIGipServerpassport=904397066.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; current_captcha_type=Z; BIGipServerportal=3151233290.17183.0000; BIGipServerotn=837812746.64545.0000; BIGipServerpool_passport=216269322.50215.0000; _jc_save_fromStation=%u6D1B%u9633%u9F99%u95E8%2CLLF; _jc_save_toStation=%u90D1%u5DDE%u4E1C%2CZAF; _jc_save_fromDate=2021-04-26'
        }
        self.params = {
            'leftTicketDTO.train_date': _date,
            'leftTicketDTO.from_station': _from,
            'leftTicketDTO.to_station': _to,
            'purpose_codes': '0X00'
        }

    def get_ticket(self):
        global response1
        response1 = requests.get(url=self.url1, params=self.params, headers=self.headers)
        # pprint(response.json())
        info = response1.json()['data']['map']  # 字典
        travel = response1.json()['data']['result']  # 列表
        print('本次查询共{}趟列车:'.format(len(travel)))
        print('经筛选后剩余：')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('序号  |  车次    |    出发地    |   到达地    |   出发时间   |   到达时间   |    历时    |  二等座  |  一等座  |  商务座  |  动卧  |  无座  |  软卧  |  硬卧  |  硬座')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
        nu = 0
        G_ticket_number = {
            'business_seat': '',
            'first_class_seat': '',
            'second_class_seat': ''
        }
        D_ticket_number = {
            'no_seat': '',
            'first_class_seat': '',
            'second_class_seat': '',
            'move_sleep': ''
        }
        T_ticket_number = {
            'hard_seat': '',
            'hard_sleep': '',
            'soft_sleep': '',
            'no_seat': ''
        }
        for i, k in enumerate(travel, 1):
            index = k.split('|')
            # print(index)
            if index[3][0] == 'G':
                G_ticket_number['business_seat'] = index[32]
                G_ticket_number['first_class_seat'] = index[31]
                G_ticket_number['second_class_seat'] = index[30]
            elif index[3][0] == 'D':
                D_ticket_number['no_seat'] = index[26]
                D_ticket_number['first_class_seat'] = index[30]
                D_ticket_number['second_class_seat'] = index[31]
                D_ticket_number['move_sleep'] = index[33]
            else:
                T_ticket_number['hard_seat'] = index[29]
                T_ticket_number['hard_sleep'] = index[28]
                T_ticket_number['soft_sleep'] = index[26]
                T_ticket_number['no_seat'] = index[23]
            if index[6] == self.params['leftTicketDTO.from_station'] and index[7] == self.params['leftTicketDTO.to_station']:
                nu += 1
                index[6] = info[index[6]]
                index[7] = info[index[7]]
            else:
                continue
            if index[3][0] == 'G':
                print(f'{nu:<3}  |  {index[3]:<5}   |   {index[6]:<4}   |   {index[7]:<3}    |    {index[8]:<5}    |    {index[9]:<5}   |    {index[10]:<5}   |   {G_ticket_number["second_class_seat"]:<1}   |   {G_ticket_number["first_class_seat"]:<1}   |    {G_ticket_number["business_seat"]:<1}    |   --   |   --   |   --   |   --   |   --')
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
            elif index[3][0] == 'D':
                print(
                    f'{nu:<3}  |  {index[3]:<5}   |   {index[6]:<4}   |   {index[7]:<3}    |    {index[8]:<5}    |    {index[9]:<5}   |    {index[10]:<5}   |   {D_ticket_number["second_class_seat"]:<1}   |   {D_ticket_number["first_class_seat"]:<1}   |   --   |   {D_ticket_number["move_sleep"]:<1}   |   {D_ticket_number["no_seat"]:<1}   |   --   |   --   |   --')
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
            else:
                print(
                    f'{nu:<3}  |  {index[3]:<5}   |   {index[6]:<4}   |   {index[7]:<3}    |    {index[8]:<5}    |    {index[9]:<5}   |    {index[10]:<5}   |   --   |   --   |   --   |   --   |   {T_ticket_number["no_seat"]:<1}   |   {T_ticket_number["soft_sleep"]:<1}   |   {T_ticket_number["hard_sleep"]:<1}   |   {T_ticket_number["hard_seat"]:<1}')
                print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('序号  |  车次    |    出发地    |   到达地    |   出发时间   |   到达时间   |    历时    |  二等座  |  一等座  |  商务座  |  动卧  |  无座  |  软卧  |  硬卧  |  硬座')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('查询到{}趟列车'.format(nu))


if __name__ == '__main__':
    print('==============================')
    print('欢迎使用12306查票小程序！')
    print('==============================')
    while True:
        d = input('请输入日期(格式为：1970-01-01)：\n')  # '2021-05-01'
        if len(d.split('-')[1]) == 2 and len(d.split('-')[2]) == 2:
            break
        else:
            print('格式错误！请重新输入！')
            continue
    f = None
    t = None
    while True:
        f1 = input('请输入出发站点(如洛阳龙门站输入：洛阳龙门)：\n')  # '洛阳龙门'
        if f1 in stations.values():
            for f, m in stations.items():
                if f1 == m:
                    break
                else:
                    continue
        else:
            print('未查询到此列车站点！请重新输入！')
            continue
        break
    while True:
        t1 = input('请输入目的地站点(如郑州东站输入：郑州东)：\n')  # '郑州东'
        if t1 in stations.values():
            for t, n in stations.items():
                if t1 == n:
                    break
                else:
                    continue
        else:
            print('未查询到此列车站点！请重新输入！')
            continue
        break
    ticket = Ticket(d, f, t)
    ticket.get_ticket()
