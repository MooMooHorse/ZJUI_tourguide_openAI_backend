def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
        """
            Returns the number of tokens used by a list of messages.
            Source:
                https://platform.openai.com/docs/guides/text-generation/managing-tokens
        """
        import tiktoken
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
        See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

def truncate_string_by_tokens(text, limit = 8191):
    def _meet_token_limit(text, limit = 8191):
        tokens = num_tokens_from_messages([{"role": "user", "content": text}])
        return tokens <= limit
    def _str_truncate_by_binary_search(text, limit = 8191):
        l, r = 0, len(text)
        while l < r:
            mid = (l + r) // 2
            if _meet_token_limit(text[:mid], limit):
                l = mid + 1
            else:
                r = mid
        return text[:l]
    if _meet_token_limit(text, limit):
        return text
    return _str_truncate_by_binary_search(text, limit)


def test_prompt_tokens(prompt_name = 'few-shots.prompt'):
    '''
        test the number of tokens used by the prompt
    '''
    import os, sys
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.dirname((cur_dir)))
    from paths import prompt_dir
    with open(os.path.join(prompt_dir, prompt_name), 'r') as f:
        prompt = f.read()
    return num_tokens_from_messages([{"role": "user", "content": prompt}])

if __name__ == "__main__":
    print(test_prompt_tokens())