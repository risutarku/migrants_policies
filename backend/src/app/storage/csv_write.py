# import os, aiofiles, asyncio
# from app.models.to_csv import RegisterUser


# AMEND_DT_FIELDS = [
#     "birthday",
#     "passport issue date",
#     "passport expiry date",
# ]


# def validate_date_format(date_str: str) -> str:
#     """Validate and format date string to yyyy-mm-dd."""
#     try:
#         return date_str.strftime("%Y-%m-%d")
#     except AttributeError:
#         raise ValueError("Date must be a datetime object or in format dd:mm:yy")


# def row_from_model(user: dict, headers: list[str]) -> list[str]:
#     for field in AMEND_DT_FIELDS:
#         if field in user and user[field] is not None:
#             user[field] = validate_date_format(user[field])

#     return [str(user.get(header, "")) for header in headers]


# _LOCK = asyncio.Lock()


# def flatten(d: dict) -> dict:
#     """
#     {'a': {'b': 1}} → {'b': 1}
#     """
#     flat = {}
#     for k, v in d.items():
#         if isinstance(v, dict):
#             flat.update(flatten(v))
#         else:
#             flat[k] = v
#     return flat


# async def write_to_csv(user: RegisterUser, filepath: str) -> None:
#     dump = user.model_dump(by_alias=True, exclude_none=False)
#     flattened = flatten(dump)
#     headers = list(flattened.keys())
#     row = row_from_model(flattened, headers)
#     async with _LOCK:
#         new_file = not os.path.exists(filepath)

#         async with aiofiles.open(filepath, "a", encoding="utf-8", newline="") as f:
#             if new_file:
#                 await f.write(",".join(headers) + "\n")

#             safe_row = [
#                 val.replace('"', '""') if isinstance(val, str) else val for val in row
#             ]
#             await f.write(",".join(f'"{v}"' for v in safe_row) + "\n")
