from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import requests
from bs4 import BeautifulSoup


@dataclass
class ExtractionConfig:
    """
    Конфигурация для извлечения текста со страницы.

    Параметры:
        url (str): URL-адрес страницы для парсинга.
        container (Dict[str, Any]): Словарь с параметрами контейнера,
            например: {"tag": "div", "attrs": {"class": "col-12 col-lg-9 order-1 supertop"}}
        child_tag (str): Имя тега дочерних элементов, из которых извлекается текст.
        child_attrs (Dict[str, str]): Атрибуты для поиска дочерних элементов.
        additional_texts (List[str]): Дополнительные тексты, которые будут объединены с результатами.
        verify_ssl (bool): Флаг проверки SSL-сертификата при запросе.
        headers (Optional[Dict[str, str]]): HTTP-заголовки для запроса.
    """

    url: str
    container: Dict[str, Any]
    child_tag: str = "span"
    child_attrs: Dict[str, str] = field(default_factory=lambda: {"class": "card-title"})
    additional_texts: List[str] = field(default_factory=list)
    verify_ssl: bool = True
    headers: Optional[Dict[str, str]] = field(
        default_factory=lambda: {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/109.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    )


class TextExtractor:
    """
    Универсальный класс для извлечения текста со страницы по списку конфигураций ExtractionConfig.
    """

    def __init__(self, configs: List[ExtractionConfig]) -> None:
        self.configs = configs

    def fetch_page(
        self, url: str, verify_ssl: bool, headers: Optional[Dict[str, str]]
    ) -> BeautifulSoup:
        response = requests.get(url, verify=verify_ssl, headers=headers)
        return BeautifulSoup(response.content, "html.parser")

    def extract_text(self) -> List[str]:
        """
        Извлекает и объединяет текст из всех указанных конфигураций.
        """
        all_texts = []
        for config in self.configs:
            soup = self.fetch_page(config.url, config.verify_ssl, config.headers)
            container_tag = config.container.get("tag", "div")
            container_attrs = config.container.get("attrs", {})
            container_element = soup.find(container_tag, attrs=container_attrs)
            if container_element:
                elements = container_element.find_all(
                    config.child_tag, attrs=config.child_attrs
                )
                texts = [el.get_text(strip=True) for el in elements]
                all_texts.extend(texts)
            all_texts.extend(config.additional_texts)
        return all_texts
