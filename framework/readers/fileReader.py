import openpyxl
import pandas as pd
from pathlib import Path
from framework.mobile.prints import text_print

class FileReader:
    _base_files_path = Path(__file__).parent.parent.parent / 'files' # Assumes 'files' is at project root

    @staticmethod
    def read_xlsx(file_name):
        file_path = FileReader._base_files_path / file_name
        try:
            if not file_path.exists():
                text_print(f"Error: File not found at {file_path}")
                return None
            df = pd.read_excel(file_path)
            text_print(f"Successfully read {file_name}")
            return df
        except Exception as e:
            text_print(f"Error reading Excel file {file_name}: {e}")
            return None

    @staticmethod
    def get_cell_value_from_excel(sheet_name, cell_name):
        excel_file_path = FileReader._base_files_path / 'fill-test-data-.xlsx'
        # print(f"[DEBUG] Excel file path being accessed for reading: {excel_file_path}") # Optional debug print
        try:
            if not excel_file_path.exists():
                text_print(f"Error: Excel file not found at {excel_file_path}")
                return None
            
            wb = openpyxl.load_workbook(excel_file_path)
            if sheet_name not in wb.sheetnames:
                text_print(f"Error: Sheet '{sheet_name}' not found in {excel_file_path}. Available sheets: {wb.sheetnames}")
                wb.close()
                return None
            
            sheet = wb[sheet_name]
            # openpyxl handles invalid cell names by raising a KeyError or similar, 
            # so direct check might be redundant unless specific pre-validation is needed.
            value = sheet[cell_name].value
            wb.close()
            return value
        except Exception as e:
            text_print(f"Error reading cell '{cell_name}' from sheet '{sheet_name}' in {excel_file_path}: {e}")
            if 'wb' in locals() and wb is not None:
                wb.close()
            return None

    @staticmethod
    def set_cell_value_in_excel(sheet_name, cell_name, value_to_enter):
        excel_file_path = FileReader._base_files_path / 'fill-test-data-.xlsx'
        # print(f"[DEBUG] Excel file path being accessed for writing: {excel_file_path}") # Optional debug print
        try:
            if not excel_file_path.exists():
                text_print(f"Error: Excel file not found at {excel_file_path}. Cannot write value.")
                return False

            wb = openpyxl.load_workbook(excel_file_path)

            if sheet_name not in wb.sheetnames:
                text_print(f"Info: Sheet '{sheet_name}' not found in {excel_file_path}. Creating new sheet.")
                sheet = wb.create_sheet(title=sheet_name)
            else:
                sheet = wb[sheet_name]
            
            sheet[cell_name] = value_to_enter
            wb.save(excel_file_path)  # Save the changes to the workbook
            wb.close()
            text_print(f"Successfully wrote '{value_to_enter}' to cell '{cell_name}' in sheet '{sheet_name}' of {excel_file_path}")
            return True
        except Exception as e:
            text_print(f"Error writing to cell '{cell_name}' in sheet '{sheet_name}' of {excel_file_path}: {e}")
            if 'wb' in locals() and wb is not None:
                wb.close()
            return False

# Example usage (optional, for testing directly in this file):
# if __name__ == '__main__':
#     # Test reading
#     sheet_to_read = 'Sheet2' # Make sure this sheet exists or adjust
#     cell_to_read = 'A1' # Make sure this cell has data or adjust
#     retrieved_value = FileReader.get_cell_value_from_excel(sheet_to_read, cell_to_read)
#     if retrieved_value is not None:
#         text_print(f"Value from '{sheet_to_read}|{cell_to_read}': {retrieved_value}")
#     else:
#         text_print(f"Could not read from '{sheet_to_read}|{cell_to_read}'.")

#     # Test writing
#     sheet_to_write = 'Sheet2' 
#     cell_to_write = 'C5' # Cell to write to
#     value_to_write = 'Hello from Python!'
#     success = FileReader.set_cell_value_in_excel(sheet_to_write, cell_to_write, value_to_write)
#     if success:
#         text_print(f"Write operation successful for '{sheet_to_write}|{cell_to_write}'.")
#         # Optionally, verify by reading back
#         written_value = FileReader.get_cell_value_from_excel(sheet_to_write, cell_to_write)
#         text_print(f"Read back value from '{sheet_to_write}|{cell_to_write}': {written_value}")
#     else:
#         text_print(f"Write operation failed for '{sheet_to_write}|{cell_to_write}'.")

#     # Test writing to a new sheet
#     new_sheet_name = 'MyNewSheet'
#     new_cell_to_write = 'B2'
#     new_value = 12345
#     success_new_sheet = FileReader.set_cell_value_in_excel(new_sheet_name, new_cell_to_write, new_value)
#     if success_new_sheet:
#         text_print(f"Write operation successful for '{new_sheet_name}|{new_cell_to_write}'.")
#         read_back_new = FileReader.get_cell_value_from_excel(new_sheet_name, new_cell_to_write)
#         text_print(f"Read back value from '{new_sheet_name}|{new_cell_to_write}': {read_back_new}")

        