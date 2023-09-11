from dataclasses import dataclass


@dataclass
class Post:
    post_link: str
    description: str
    image_url: str