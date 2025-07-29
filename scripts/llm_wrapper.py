"""
llm_wrapper.py

Wrapper LLM pour usage local offline dans environnement de hunt.
Utilise transformers & torch avec un modèle GGUF compatible (ex : Mistral 7B Q4).
"""

from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextStreamer,
)
import torch


class HuntLLM:
    def __init__(
        self,
        model_path: str,
        max_tokens: int = 256,
        stream: bool = False,
    ):
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Modèle introuvable : {model_path}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="cpu",
            torch_dtype=torch.float32,
        )
        self.max_tokens = max_tokens
        self.stream = TextStreamer(self.tokenizer, skip_prompt=True) if stream else None

        # Vérifie si on peut utiliser apply_chat_template()
        self.has_chat_template = hasattr(self.tokenizer, "apply_chat_template")

    def ask(self, question: str, context: str | None = None) -> str:
        if self.has_chat_template:
            # Modèle avec support des messages (SmolLM, LLaMA3, Minstral, etc.)
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            messages.append({"role": "user", "content": question})

            # Génère le prompt via chat_template (en texte brut)
            prompt_input = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=False  # important : on récupère un str
            )

            # Tokenize ensuite normalement
            inputs = self.tokenizer(prompt_input, return_tensors="pt")
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        else:
            # Modèle sans chat_template (Phi, anciens LLaMA2...)
            prompt = ""
            if context:
                prompt += f"[System]\n{context}\n\n"
            prompt += f"[User]\n{question}\n[Assistant]\n"

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                return_token_type_ids=False,
            )
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            streamer=self.stream,
        )

        response = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True,
        )
        return response.strip()
