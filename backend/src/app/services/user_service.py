# import os
# from datetime import datetime
# from app.storage.csv_write import write_to_csv
# from app.models.user import User


# async def get_file_path() -> str:
#     """
#     Returns the absolute path to the CSV data directory.
#     Creates the directory if it does not exist.
#     """
#     folder = os.path.abspath(
#         os.path.join(os.path.dirname(__file__), "../../../../data/csv_data")
#     )
#     os.makedirs(folder, exist_ok=True)
#     filename = datetime.now().strftime("%Y-%m-%d") + ".csv"
#     filepath = os.path.join(folder, filename)
#     return filepath


# async def record_user_data_service(user_data: User) -> None:
#     """
#     Service function to handle user data.
#     It writes the user data to a CSV file.

#     :param user_data: An instance of User containing user information.
#     """
#     filepath = await get_file_path()
#     await write_to_csv(user_data, filepath)
#     return


# async def register_user(draft: User, tx_id: str):
#     """Финальная запись CSV (или БД)"""
#     draft.tx_id = tx_id
#     filepath = await get_file_path()
#     await write_to_csv(draft, filepath)
