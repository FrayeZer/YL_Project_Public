import openai
import json_reader

openai.api_key = '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'


def chatgpt_response(interaction, prompt: str) -> str:
    """
    Делает запросы к API chatgpt с использованием модели gpt-3.5-turbo. Возвращает текстовый ответ.
    """
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': prompt}],
        temperature=0.6,
        max_tokens=json_reader.get_value(f'{interaction.guild.id}/config.json', 'max_tokens'),
    )
    return response['choices'][0]['message']['content'].strip()
