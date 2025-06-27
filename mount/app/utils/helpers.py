from app.repositories.base_repo import BaseRepository
from slugify import slugify


def page_to_offset(page: int, limit: int):
	offset = (page - 1) * limit
	return offset


def calculate_pagination(total_data: int, page: int, limit: int):
	# Ensure limit is valid
	if limit <= 0:
		raise ValueError('Limit must be greater than 0.')

	offset = page_to_offset(page, limit)
	# Calculate current page and total pages
	current_page = (offset // limit) + 1
	total_pages = (total_data + limit - 1) // limit  # Ceiling division

	# Determine pages before and after
	page_before = current_page - 1 if current_page > 1 else 0
	page_after = current_page + 1 if current_page < total_pages else 0

	# Return pagination details
	return {
		'total_data': total_data,
		'total_pages': total_pages,
		'current_page': current_page,
		'prev_page': page_before,
		'next_page': page_after,
	}


async def generate_unique_slug(name: str, repo: BaseRepository):
	slug_data = slugify(name)
	slug_exists = await repo.get_by_field('slug', slug_data)
	slug_count = 0
	while slug_exists:
		slug_count += 1
		temp_slug_data = slug_data + '-' + str(slug_count)
		temp_slug_exists = await repo.get_by_field('slug', temp_slug_data)
		if not temp_slug_exists:
			slug_data = temp_slug_data
			break
	return slug_data
