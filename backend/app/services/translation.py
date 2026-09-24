class KannadaTranslator:
    provider = "offline_stub"

    def translate(self, text_kn: str) -> str:
        if not text_kn:
            return ""
        return "[configure IndicTrans2] " + text_kn

