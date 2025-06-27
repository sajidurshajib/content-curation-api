from enum import Enum


class ArticleStatus(Enum):
	PUBLISHED = 'published'
	DRAFT = 'draft'
	ARCHIVED = 'archived'
