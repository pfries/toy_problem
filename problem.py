#!/usr/local/env python
import unittest, copy
from datetime import date, datetime, timedelta

def project_to_dates(start_date, end_date):
    day = start_date
    while day <= end_date:
        yield day
        day += timedelta(days=1)

def calculate(p):
    projects = copy.deepcopy(p)
    for idx,p in enumerate(projects):
        days_costed = set({})
        start_date = p["start_date"]
        end_date = p["end_date"]
        dates_in_project = list(project_to_dates(start_date, end_date))
        cost_of_project = 0
        for idx_d, d in enumerate(dates_in_project):
            if d in days_costed:
                # TODO: if costing same day, use greater value
                continue

            is_travel_day = False
            is_full_day = False

            if idx_d == 0 or idx_d == len(dates_in_project) - 1:
                is_travel_day = True
            else:
                is_full_day = True

            # is there any overlap with prev project?
            if idx_d == 0 and idx > 0:
                prev = projects[idx - 1]
                day_before_start_of_project = start_date - timedelta(days=1)
                extended_project_dates = [day_before_start_of_project] + dates_in_project
                prev_project_dates = project_to_dates(prev["start_date"], prev["end_date"])
                s = set(extended_project_dates).intersection(set(prev_project_dates))
                if len(s) > 0:
                    is_full_day = True

            # is there any overlap with next project?
            if idx_d == len(dates_in_project) and idx < len(dates_in_project) - 1:
                nxt = dates_in_project[idx + 1]
                day_after_end_of_project = end_date + timedelta(days=1)
                extended_project_dates = dates_in_project + day_after_end_of_project
                next_project_dates = project_to_dates(nxt["start_date"], nxt["end_date"])
                s = set(extended_project_dates).intersection(set(next_project_dates))
                if len(s) > 0:
                    is_full_day = True

            day_cost = 0
            if is_travel_day:
                day_cost = p['travel_day_rate'] 
            if is_full_day:
                day_cost = p['full_day_rate'] 

            cost_of_project += day_cost
            days_costed.add(d)

        p["cost"] = cost_of_project
    return projects

class TestReimbursementCalculator(unittest.TestCase):

    def test_project_dates(self):
        start = date(2015,9,1)
        end = date(2015,9,5)
        dates = list(project_to_dates(start, end))
        self.assertEqual(len(dates),5)

    def test_single_project(self):
        p = {
            "travel_day_rate": 55,
            "full_day_rate": 85, 
            "start_date": date(2015,9,2),
            "end_date": date(2015,9,6)
        }
        costed_out = calculate([p])

    def test_set_2(self):
        p1 = {
            "travel_day_rate": 45,
            "full_day_rate": 75, 
            "start_date": date(2015,9,1),
            "end_date": date(2015,9,1)
        }
        p2 = {
            "travel_day_rate": 55,
            "full_day_rate": 85, 
            "start_date": date(2015,9,2),
            "end_date": date(2015,9,6)
        }
        p3 = {
            "travel_day_rate": 45,
            "full_day_rate": 75, 
            "start_date": date(2015,9,6),
            "end_date": date(2015,9,8)
        }
        projects = [p1,p2,p3]
        projects_with_costs = calculate(projects)
        for p in projects_with_costs:
            print(p["cost"])

if __name__ == '__main__':
    unittest.main()
