import csv

class StudentMetadataLoader:
    """
    Loads student metadata (name and ID) from a CSV file.
    """
    def __init__(self, metadata_file: str):
        """
        Initialize the metadata loader.
        
        :param metadata_file: Path to the CSV file containing student metadata.
        """
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict[str, dict[str, str]]:
        """
        Load metadata from the CSV file.
        
        :return: Dictionary mapping filenames to student metadata.
        """
        metadata = {}
        try:
            with open(self.metadata_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    metadata[row["filename"]] = {
                        "student_name": row["student_name"],
                        "student_id": row["student_id"]
                    }
            return metadata
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return {}