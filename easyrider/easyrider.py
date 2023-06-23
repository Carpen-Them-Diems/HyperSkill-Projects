import json
import re
import unittest
import sys


test_json = [{"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": 8.1}, {"bus_id": 128, "stop_id": 3, "stop_name": "", "next_stop": 5, "stop_type": "", "a_time": "08:19"}, {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": "O", "a_time": "08:25"}]


class RunCheckers:
    def __init__(self, choices=input('Enter checkers to run or All for all checkers:\n> ')):
        self.choices = [choices]
        self.choices_lowered = []
        if len(self.choices) > 1:
            for choice in self.choices:
                self.choices_lowered.append(choice.lower())
        else:
            self.choices_lowered.append(self.choices[0].lower())

    def run_(self):
        data=input('Enter JSON formatted string data:\n> ')
        data_type_checker = DataTypeChecker(data=data)
        format_checker = FormatChecker(data=data)
        bus_line_checker = BusLineChecker(data=data)
        bus_stop_checker = BusStopChecker(data=data)
        stop_times_checker = StopTimesChecker(data=data)
        on_demand_stop_checker = OnDemandStopChecker(data=data)

        if 'all' in self.choices_lowered:
            data_type_checker.type_checker_()
            data_type_checker.print_results()
            print()
            format_checker.format_checker_()
            format_checker.print_results()
            print()
            bus_line_checker.bus_line_checker_()
            bus_line_checker.print_results()
            print()
            bus_stop_checker.bus_stop_checker_()
            bus_stop_checker.print_results()
            print()
            stop_times_checker.stop_times_checker_()
            stop_times_checker.print_results()
            print()
            on_demand_stop_checker.on_demand_stop_checker_()
            on_demand_stop_checker.print_results()

        if 'datatypechecker' in self.choices_lowered:
            data_type_checker.type_checker_()
            data_type_checker.print_results()

        if 'formatchecker' in self.choices_lowered:
            format_checker.format_checker_()
            format_checker.print_results()

        if 'buslinechecker' in self.choices_lowered:
            bus_line_checker.bus_line_checker_()
            bus_line_checker.print_results()

        if 'busstopchecker' in self.choices_lowered:
            bus_stop_checker.bus_stop_checker_()
            bus_stop_checker.print_results()

        if 'stoptimeschecker' in self.choices_lowered:
            stop_times_checker.stop_times_checker_()
            stop_times_checker.print_results()

        if 'ondemandstopchecker' in self.choices_lowered:
            on_demand_stop_checker.on_demand_stop_checker_()
            on_demand_stop_checker.print_results()


class DataTypeChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.correct_data_types = {
            "bus_id": int,
            "stop_id": int,
            "stop_name": str,
            "next_stop": int,
            "stop_type": str,
            "a_time": str
        }
        self.errors = {
            'total': 0,
            "bus_id": 0,
            "stop_id": 0,
            "stop_name": 0,
            "next_stop": 0,
            "stop_type": 0,
            "a_time": 0
        }
        self.json_string = data
        self.json_data = json.loads(self.json_string)

    def type_checker_(self):
        for dic in self.json_data:
            dic = dict(dic)
            for field, dtype in self.correct_data_types.items():
                if type(dic[field]) is not dtype:
                    self.errors[field] += 1
                    self.errors['total'] += 1
                elif field == 'stop_type':
                    if type(dic[field]) is dtype and dic[field] not in ['S', 'O', 'F', '']:
                        self.errors[field] += 1
                        self.errors['total'] += 1
                elif field == 'stop_name':
                    if len(dic[field]) == 0:
                        self.errors[field] += 1
                        self.errors['total'] += 1
                elif field == 'a_time':
                    if len(dic[field]) == 0:
                        self.errors[field] += 1
                        self.errors['total'] += 1

    def print_results(self):
        print(f"Type and required field validation: {self.errors['total']} errors\nbus_id: {self.errors['bus_id']}\n"
              f"stop_id: {self.errors['stop_id']}\nstop_name: {self.errors['stop_name']}\n"
              f"next_stop: {self.errors['next_stop']}\nstop_type: {self.errors['stop_type']}"
              f"\na_time: {self.errors['a_time']}")


class FormatChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.json_string = data
        self.json_data = json.loads(self.json_string)
        self.errors = {
            'total': 0,
            "stop_name": 0,
            "stop_type": 0,
            "a_time": 0
        }

    def format_checker_(self):
        for dic in self.json_data:
            for field in dic:
                if field == 'stop_name':
                    stop_name = dic[field].split(' ')
                    if len(stop_name) < 2:
                        self.errors[field] += 1
                        self.errors['total'] += 1
                    elif len(stop_name) == 2:
                        if stop_name[0].lower() in ['road', 'boulevard', 'avenue', 'street', 'av.', 'st.'] or \
                           stop_name[-1].lower() not in ['road', 'boulevard', 'avenue', 'street'] \
                           or not stop_name[0].istitle() or not stop_name[1].istitle():
                            self.errors[field] += 1
                            self.errors['total'] += 1
                    elif len(stop_name) > 2:
                        if [stop_name[0].lower(), stop_name[1].lower()] in ['road', 'boulevard', 'avenue', 'street', 'av.', 'st.'] or \
                           stop_name[-1].lower() not in ['road', 'boulevard', 'avenue', 'street'] \
                           or not [stop_name[0].istitle(), stop_name[1].istitle(), stop_name[2].istitle()]:
                            self.errors[field] += 1
                            self.errors['total'] += 1

                if field == 'stop_type':
                    if len(dic[field]) > 1 or dic[field] not in ['S', 'O', 'F', '']:
                        self.errors[field] += 1
                        self.errors['total'] += 1

                if field == 'a_time':
                    if not isinstance(dic[field], str):
                        self.errors[field] += 1
                        self.errors['total'] += 1

                    if not re.match(r'^\d{2}:\d{2}$', dic[field]) or int((dic[field][0])) > 2 or int((dic[field][3])) > 5 or int((dic[field][0])) == 2 and int((dic[field][1])) >= 4:
                        self.errors[field] += 1
                        self.errors['total'] += 1

    def print_results(self):
        print(f"Type and required field validation: {self.errors['total']} errors\nstop_name: {self.errors['stop_name']}"
              f"\nstop_type: {self.errors['stop_type']}\na_time: {self.errors['a_time']}")


class BusLineChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.json_string = data
        self.json_data = json.loads(self.json_string)
        self.bus_lines = []
        self.bus_stops = {}

    def bus_line_checker_(self):
        for dic in self.json_data:
            for field in dic:
                if field == 'bus_id':
                    if dic[field] not in self.bus_lines:
                        self.bus_lines.append(dic[field])
                        self.bus_stops[dic[field]] = 1
                    elif dic[field] in self.bus_lines:
                        self.bus_stops[dic[field]] += 1

    def print_results(self):
        print(f'Line names and number of stops:')
        for i in range(len(self.bus_lines)):
            print(f'bus_id: {self.bus_lines[i]}, stops: {self.bus_stops[self.bus_lines[i]]}')


class BusStopChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.json_string = data
        self.json_data = json.loads(self.json_string)
        self.bus_sf = {}
        self.sf_names = {}
        self.t_names = []

    def bus_stop_checker_(self):
        stops_name_buses = {}

        for dic in self.json_data:
            if dic['bus_id'] not in self.bus_sf:
                if dic['stop_type'] in ['S', 'F']:
                    self.bus_sf[dic['bus_id']] = [dic['stop_type']]
            elif dic['bus_id'] in self.bus_sf.keys() and dic['stop_type'] not in self.bus_sf[dic['bus_id']]:
                if dic['stop_type'] in ['S', 'F']:
                    self.bus_sf[dic['bus_id']].append(dic['stop_type'])

        for key, values in self.bus_sf.items():
            if 'S' not in values or 'F' not in values:
                print(f'There is no start or end for the line: {key}')
                break

        for dic in self.json_data:
            for field in dic:
                if field == 'stop_type':
                    if dic[field] == 'S':
                        if 'S' not in self.sf_names.keys():
                            self.sf_names['S'] = [dic['stop_name']]
                        elif dic['stop_name'] not in self.sf_names['S']:
                            self.sf_names['S'].append(dic['stop_name'])

                    elif dic[field] == 'F':
                        if 'F' not in self.sf_names.keys():
                            self.sf_names['F'] = [dic['stop_name']]
                        elif dic['stop_name'] not in self.sf_names['F']:
                            self.sf_names['F'].append(dic['stop_name'])

        for dic in self.json_data:
            for field in dic:
                if field == 'stop_name':
                    if dic[field] not in stops_name_buses:
                        stops_name_buses[dic[field]] = [dic['bus_id']]
                    elif dic[field] in stops_name_buses.keys():
                        stops_name_buses[dic[field]].append(dic['bus_id'])

        for name, b_id in stops_name_buses.items():
            if len(b_id) > 1:
                self.t_names.append(name)

    def print_results(self):
        print(f"Start stops: {len(self.sf_names['S'])} {sorted(self.sf_names['S'])}\n"
              f"Transfer stops: {len(self.t_names)} {sorted(self.t_names)}\n"
              f"Finish stops: {len(self.sf_names['F'])} {sorted(self.sf_names['F'])}\n")


class StopTimesChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.json_string = data
        self.json_data = json.loads(self.json_string)
        self.ordered_lines = {}
        self.incorrect_stops = {}

    def stop_times_checker_(self):
        stop = False

        for dic in self.json_data:
            bus_id = dic['bus_id']
            stop_id = dic['stop_id']
            a_time = dic['a_time']
            stop_name = dic['stop_name']
            next_stop = dic['next_stop']
            stop_type = dic['stop_type']

            if bus_id not in self.ordered_lines:
                self.ordered_lines[dic['bus_id']] = {}

            if stop_id not in self.ordered_lines[bus_id]:
                self.ordered_lines[bus_id][stop_id] = {}
                self.ordered_lines[bus_id][stop_id]['a_time'] = a_time
                self.ordered_lines[bus_id][stop_id]['stop_name'] = stop_name
                self.ordered_lines[bus_id][stop_id]['next_stop'] = next_stop
                self.ordered_lines[bus_id][stop_id]['stop_type'] = stop_type

        for bus, stops in self.ordered_lines.items():
            sorted_values = sorted(stops.items(), key=lambda x: (x[1]['stop_type'] != 'S', x[1]['next_stop']
                                   if x[1]['stop_type'] == 'S' else float('inf')))
            self.ordered_lines[bus] = dict(sorted_values)

        while stop is False:
            stop = False
            for bus, stops in self.ordered_lines.items():
                stop_ids = list(stops.keys())
                for stop, a_times_names in stops.items():
                    if len(stop_ids) > 2:
                        for i in range(len(stop_ids) - 1):
                            if stops[stop_ids[i]]['a_time'] >= stops[stop_ids[i + 1]]['a_time']:
                                self.incorrect_stops[bus] = stops[stop_ids[i + 1]]['stop_name']
                                stop = True
                                break
                    else:
                        if stops[stop_ids[0]]['a_time'] >= stops[stop_ids[1]]['a_time']:
                            self.incorrect_stops[bus] = stops[stop_ids[1]]['stop_name']
                            stop = True
                            break

    def print_results(self):
        if len(self.incorrect_stops) == 0:
            print('Arrival time test:\nOK')
        else:
            print('Arrival time test:')
            for bus, stop_name in self.incorrect_stops.items():
                print(f'bus_id line {bus}: Wrong time on station {stop_name}')


class OnDemandStopChecker:
    def __init__(self, data=input('Enter JSON formatted string data:\n> ')):
        self.json_string = data
        self.json_data = json.loads(self.json_string)
        self.incorrect_stop_types = []
        bus_stop_checker = BusStopChecker(data=self.json_string)
        bus_stop_checker.bus_stop_checker_()
        self.sf_names = bus_stop_checker.sf_names
        self.t_names = bus_stop_checker.t_names

    def on_demand_stop_checker_(self):
        for dic in self.json_data:
            stop_type = dic['stop_type']
            stop_name = dic['stop_name']
            bus_id = dic['bus_id']

            if stop_name in self.sf_names.values():
                if stop_type == 'O':
                    self.incorrect_stop_types[bus_id].append(stop_name)

            if stop_name in self.t_names:
                if stop_type == 'O':
                    self.incorrect_stop_types.append(stop_name)

    def print_results(self):
        self.incorrect_stop_types = sorted(self.incorrect_stop_types)
        if len(self.incorrect_stop_types) > 0:
            print(f'On demand stops test:\nWrong stop type: {self.incorrect_stop_types}')
        else:
            print('OK')


checker = RunCheckers()
checker.run_()
