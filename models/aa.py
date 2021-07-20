from models import user_simpleton, prompt

for p in user_simpleton.get_one_user(1).prompts:
    print(prompt.prompt_id)