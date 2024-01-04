tag: user.openai_defined

-

# Uses Talon-AI-Tools community standard
^echo {user.staticPrompt}$:
    text = edit.selected_text()
    result = user.gpt_apply_prompt(user.staticPrompt, text)
    user.cancel_current_speaker()
    user.tts(result)

echo ask <user.text>:
    result = user.gpt_answer_question(text)
    user.cancel_current_speaker()
    user.tts(result)

describe image:
    user.describe_image()
