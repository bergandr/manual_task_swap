# add and remove functions


def remove_task(task, plan):
    error_code = False

    for item in plan:
        if task == item["id"]:
            plan.remove(item)
        else:
            error_code = True

    return error_code


def add_task(task, plan):
    plan.append(task)


def apply_changes(change_request):
    remove_error = False
    plan = change_request["plan"]

    if "remove" in change_request:
        remove_error = remove_task(change_request["remove"], plan)

    if remove_error:
        return {"error": "Task not found in original plan."}

    if "add" in change_request:
        add_task(change_request["add"], plan)

    return plan


def validate_plan(duration, plan):
    is_valid = False
    plan_total = 0

    for item in plan:
        task_time = item["duration"]
        plan_total = plan_total + task_time

    if plan_total < duration:
        is_valid = True

    return is_valid
