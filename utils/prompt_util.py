


def get_admin_prompt() -> str:
    """
    获取主提示语
    """
    try:
        with open("../config/admin_prompt.txt", "r", encoding="utf-8") as f:
            main_prompt = f.read()
    except Exception as e:
        print(e)
        main_prompt = "你是幸福餐饮的客服小助手"
    return main_prompt
def get_report_prompt() -> str:
    """
    获取报告提示语
    """
    try:
        with open("../config/report_prompt.txt", "r", encoding="utf-8") as f:
            report_prompt = f.read()
    except Exception as e:
        print(e)
        report_prompt = "你是幸福餐饮的客服小助手"
    return report_prompt

def get_user_prompt() -> str:
    """
    获取用户提示语
    """
    try:
        with open("../config/user_prompt.txt", "r", encoding="utf-8") as f:
            user_prompt = f.read()
    except Exception as e:
        print(e)
        user_prompt = "你是幸福餐饮的客服小助手"
    return user_prompt


user_prompt = get_user_prompt()
admin_prompt = get_admin_prompt()
report_prompt = get_report_prompt()

if __name__ == '__main__':
    print(admin_prompt)