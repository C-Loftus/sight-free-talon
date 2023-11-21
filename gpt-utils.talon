tag: user.openai_defined

-

# TODO: This is currently dependent upon my own implementation, going forward
# I need to check if there's going to be some sort of community standard and how
# it might be best to integrate my code with a broader more community based solution
^echo {user.promptNoArgument}$:
    result = user.gpt_prompt_no_argument(user.promptNoArgument)
    user.robot_tts(result)
