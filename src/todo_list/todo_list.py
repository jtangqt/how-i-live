from datetime import date
import datetime
from task import Task

from todo_list_db import *


def insert_task(task_name):
    return insert_row(task_name)


def unpack_tasks(records):
    tasks = []
    for record in records:
        task_entry = Task()
        task_entry.unpack_records(record)
        tasks.append(task_entry)
    return tasks


def get_records_for_task_name(task_name):
    records, err = find_records_for_task_name(task_name)
    if err is not None:
        return None, err
    print("Info: got {} record successfully from task name".format(len(records)))
    return records, None


def get_task_entry_by_idx(idx):
    record, err = find_record_for_task_id(idx)
    if err is not None:
        return None, err
    task_entry = unpack_tasks([record])[0]
    print("Info: got 1 record successfully from idx: {}".format(idx))
    return task_entry, None


def get_tasks_for_date(date):
    records, err = find_records_for_date(date)
    if err is not None:
        return None, err
    tasks = unpack_tasks(records)
    print("Info: got {} record successfully for date: {}".format(len(records), date))
    return tasks, None


def update_task_entry(task_name, task: Task):
    records, err = find_records_for_task_name(task_name)
    if err is not None:
        return err
    indexes = {}
    items = "Please indicate which index you'd like to update\n"
    for record in records:
        indexes[str(record[0])] = 0
        items += "{}: {}\n".format(record[0], record[1:])
    ans = input(
        items
    )
    if ans in indexes:
        task_entry, _ = get_task_entry_by_idx(int(ans))
        task_entry.update(task)
        return update_task_entry_for_task_id(int(ans), task_entry)
    else:
        raise Exception("Error: user chose an index that is not present for task name: {}".format(task_name))


def delete_task_entries(task_name):
    records, err = find_records_for_task_name(task_name)
    if err is not None:
        return err
    indexes = {}
    items = "Please indicate which index you'd like to delete\n"
    for record in records:
        indexes[str(record[0])] = 0
        items += "{}: {}\n".format(record[0], record[1:])
    items += "or you can indicate (all/n) "
    ans = input(
        items
    )
    if ans in indexes:
        return delete_task_entry_for_task_id(int(ans))
    elif ans == "all":
        return delete_all_task_entries_for_task_name(task_name)
    elif ans == "n":
        print("Info: user cancelled delete entry for task name: {}".format(task_name))
    else:
        raise Exception("Error: user chose an index that is not present for task name: {}".format(task_name))
    return None


def postpone_tasks_from_yesterday():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    tasks, err = get_tasks_for_date(yesterday)
    if err is not None:
        return err
    for task in tasks:
        if not task.is_active and task.is_active is not None:
            continue
        task.update_next_occurrence()
        err = update_task_entry_for_task_id(task.idx, task)
        if err is not None:
            return err
    return None


if __name__ == "__main__":

    task = Task()
    today = date.today()
    err = task.schedule.update_schedule("weekly", ["Thursday"])  # test weekly
    # err = task.schedule.update_schedule("daily", None)  # test daily
    # err = task.schedule.update_schedule("monthly", [0, 1, 17])  # test monthly
    if err is not None:
        print("{}".format(err))
    task.add_next_occurrence()

    # if insert_task("leetcode") is not None:
    #     print("Error: insert in to-do list did not insert properly")
    # task.next_occurrence = datetime.date.today() - datetime.timedelta(days=1)

    task.next_occurrence = today - datetime.timedelta(days = 1)
    print(task.next_occurrence)
    print("here!!!")
    err = update_task_entry("leetcode", task)
    if err is not None:
        print("{}".format(err))

    new_tasks = get_records_for_task_name("leetcode")
    err = postpone_tasks_from_yesterday()
    if err is not None:
        print("{}".format(err))

    # deleted_err = delete_task_entries("leetcode")
    # if deleted_err is not None:
    #     print("{}".format(err))
