# functions to add and remove tasks from a task management plan
# and a function to validate a plan against the plan's time constraints


def remove_task(task, plan):
    """
    Removes a task from a task management plan.
    :param task: name of task to remove
    :param plan: an array of tasks of the form {"id": "task name", "duration": int (minutes)}
    :return: boolean error_code:
             False if the task could be removed
             True if the task to be removed was not found on the plan
    The task list (i.e. the plan) is updated if the task could be removed.
    """
    error_code = True  # will be False if task is found

    # look for the task in the plan and remove it if it's found
    for item in plan:
        if task == item["id"]:
            plan.remove(item)
            error_code = False

    return error_code


def add_task(task, plan):
    """
    Adds a task to a plan. This is just an append since adding a task does not depend on existing data.
    :param task: name of task to add
    :param plan: an array of tasks of the form {"id": "task name", "duration": int (minutes)}
    The task list (i.e. the plan) is updated with the new task.
    """
    plan.append(task)


def apply_changes(change_request):
    """
    Takes a request to change a task management plan and attempts to apply the changes.
    :param change_request: A JSON request containing entries for:
        tasks to add
        tasks to remove
        an existing plan
        a total time allocation for the tasks in the plan
    :return: result of the changes is either
             a modified plan
             an error message stating that the plan could not be modified
    """
    remove_error = False  # only the "remove" action can result in a clear error
    plan = change_request["plan"]  # the list of existing tasks from the JSON

    # if there's an entry for "remove", run the remove function and check for an error
    if "remove" in change_request:
        remove_error = remove_task(change_request["remove"], plan)

    # do not attempt to add to a plan after encountering a remove error
    # return the error right away
    if remove_error:
        return {"error": "Task not found in original plan."}

    # if the plan includes an "add" request, run the add function
    if "add" in change_request:
        add_task(change_request["add"], plan)

    return plan


def validate_plan(total_duration, plan):
    """
    Validates that a modified plan's tasks fit within the original plan's time constraints
    :param total_duration: Represents the total number of minutes allocated for the entire plan
    :param plan: an array of tasks of the form {"id": "task name", "duration": int (minutes)}
    :return: boolean
             True if the plan is valid
             False if the plan exceeds the time constraints
    """
    is_valid = False
    plan_total = 0

    # sum up the task durations
    for item in plan:
        task_time = item["duration"]
        plan_total += task_time

    # check the aggregate times
    if plan_total < total_duration:
        is_valid = True

    return is_valid
