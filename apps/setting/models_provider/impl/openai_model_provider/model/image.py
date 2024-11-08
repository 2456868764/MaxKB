import base64
import os
from typing import Dict

from openai import OpenAI

from common.config.tokenizer_manage_config import TokenizerManage
from setting.models_provider.base_model_provider import MaxKBBaseModel
from setting.models_provider.impl.base_image import BaseImage


def custom_get_token_ids(text: str):
    tokenizer = TokenizerManage.get_tokenizer()
    return tokenizer.encode(text)


class OpenAIImage(MaxKBBaseModel, BaseImage):
    api_base: str
    api_key: str
    model: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get('api_key')
        self.api_base = kwargs.get('api_base')

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = {}
        if 'max_tokens' in model_kwargs and model_kwargs['max_tokens'] is not None:
            optional_params['max_tokens'] = model_kwargs['max_tokens']
        if 'temperature' in model_kwargs and model_kwargs['temperature'] is not None:
            optional_params['temperature'] = model_kwargs['temperature']
        return OpenAIImage(
            model=model_name,
            api_base=model_credential.get('api_base'),
            api_key=model_credential.get('api_key'),
            **optional_params,
        )

    def check_auth(self):
        client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key
        )
        response_list = client.models.with_raw_response.list()
        # print(response_list)
        # cwd = os.path.dirname(os.path.abspath(__file__))
        # with open(f'{cwd}/img_1.png', 'rb') as f:
        #     self.image_understand(f, "一句话概述这个图片")

    def image_understand(self, image_file, text):
        client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key
        )
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
