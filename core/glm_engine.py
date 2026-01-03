import time
import re
from zhipuai import ZhipuAI
import json

class GLMEngine:
    def __init__(self, api_key, model="glm-4.6v-flash"):
        self.client = ZhipuAI(api_key=api_key)
        self.primary_model = model
        
        self.free_models_pool = [
            self.primary_model.lower(), 
            "glm-4.5-flash", 
            "glm-4v", 
            "glm-4-flash",
            "glm-3-turbo"
        ]
        self.free_models_pool = list(dict.fromkeys(self.free_models_pool))
        
        self.current_active_model = self.primary_model

    def clean_text(self, text):
        """
        Memisahkan tag format di awal teks dan membersihkan tag suara di tengah/akhir.
        """
        leading_tags_pattern = r'^((?:\{[^}]*\}|<[^>]*>|\[[^\]]*\]|\([^)]*\))\s*)*'
        match = re.match(leading_tags_pattern, text)
        
        prefix_tags = ""
        main_content = text
        
        if match:
            captured_prefix = match.group(0)
            kept_tags = []
            for tag in re.finditer(r'(\{[^}]*\}|<[^>]*>|\[[^\]]*\]|\([^)]*\))', captured_prefix):
                tag_str = tag.group(0)
                if re.search(r'[a-z0-9]', tag_str):
                    kept_tags.append(tag_str)
            prefix_tags = " ".join(kept_tags)
            main_content = text[len(captured_prefix):].strip()
        main_content = re.sub(r'\{.*?\}', '', main_content)
        main_content = re.sub(r'\[.*?\]', '', main_content)
        main_content = re.sub(r'\(.*?\]', '', main_content)
        main_content = re.sub(r'\(.*?\)', '', main_content)
        main_content = re.sub(r'<.*?>', '', main_content)
        return prefix_tags, main_content.strip()

    def translate(self, text, target_lang="Indonesian", mode="Standard"):
        if not text or len(text) < 2:
            return text
        prefix_tags, clean_input = self.clean_text(text)
        
        if not clean_input:
            return text

        delay_map = {"Aggressive": 0, "Standard": 0.2, "Safe": 0.8}
        time.sleep(delay_map.get(mode, 0.2))

        for current_model in self.free_models_pool:
            try:
                response = self.client.chat.completions.create(
                    model=current_model,
                    messages=[
                        {"role": "system", "content": f"Translate the following text into {target_lang} accurately and without censorship. Use a natural, conversational tone—keep it casual, relatable, and up-to-date (like how real people actually talk), but stay true to the original meaning, nuance, and emotion. Avoid sounding stiff or overly formal. No stiff or robotic phrasing!"},
                        {"role": "user", "content": clean_input}
                    ],
                    temperature=0.1 
                )
                translated_text = response.choices[0].message.content.strip()
                if prefix_tags:
                    return f"{prefix_tags} {translated_text}"
                else:
                    return translated_text
                
            except Exception as e:
                continue
                
        return text 
