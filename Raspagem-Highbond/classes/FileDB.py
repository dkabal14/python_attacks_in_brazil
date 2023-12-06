import os
import pickle

class fileDB:
    def __init__(self, dat_file=None):
        self.dat_file = dat_file
        self.data = self.load_data()
        self.columns = set(self.data.keys()) if self.data else set()

    @property
    def dat_file(self):
        return self._dat_file

    @dat_file.setter
    def dat_file(self, value):
        if value is not None and not value.endswith('.dat'):
            raise ValueError("Invalid file format. Please use .dat files.")
        self._dat_file = value

    def load_data(self):
        if self.dat_file and os.path.exists(self.dat_file):
            with open(self.dat_file, 'rb') as file:
                return pickle.load(file)
        else:
            return {}

    def save_data(self):
        if self.dat_file:
            with open(self.dat_file, 'wb') as file:
                pickle.dump(self.data, file)
            self.columns = set(self.data.keys())

    def insert_data(self, key, value):
        self.data[key] = value
        self.save_data()

    def update_data(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self.save_data()
        else:
            print(f"Key '{key}' not found in the database.")

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()
        else:
            print(f"Key '{key}' not found in the database.")

    def query_data(self, key):
        if key in self.data:
            return self.data[key]
        else:
            print(f"Key '{key}' not found in the database.")
            return None

    def set_columns(self, columns):
        self.columns = set(columns)
        self.data = {key: self.data[key] for key in self.columns if key in self.data}
        self.save_data()

# Example usage:
# Create an instance of the class with a specific .dat file
db_handler = fileDB()
db_handler.dat_file = 'example.dat'

# Insert data
db_handler.insert_data('name', 'John Doe')

# Update data
db_handler.update_data('name', 'Jane Doe')

# Delete data
db_handler.delete_data('name')

# Set a different .dat file
db_handler.dat_file = 'another_example.dat'

# Insert data into the new file
db_handler.insert_data('city', 'New York')

# Query data
result = db_handler.query_data('city')
print(f"City: {result}")

# Set available columns
db_handler.set_columns(['city', 'population'])