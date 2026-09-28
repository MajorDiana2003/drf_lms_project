from rest_framework import serializers


class YoutubeUrlValidator:
    """Валидатор для проверки, что ссылка ведет только на youtube.com"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        # Если ссылка передана, проверяем ее содержимое
        if url and "youtube.com" not in url:
            raise serializers.ValidationError(
                "Разрешены ссылки только на сторонний ресурс youtube.com!"
            )
