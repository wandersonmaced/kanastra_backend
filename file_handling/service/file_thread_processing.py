import os
import threading
import pandas as pd
from file_handling.model.file_models import Debt

class FileProcessingThread(threading.Thread):
    semaphore = threading.Semaphore(os.environ.get("THREADS"))  # thread limiting

    def __init__(self, file_path, chunk_size):
        super().__init__()
        self.file_path = file_path
        self.chunk_size = chunk_size

    def run(self):
        with self.semaphore:
            self.process_file_from_server()

    def process_file_from_server(self):
        for chunk in pd.read_csv(self.file_path, chunksize=self.chunk_size):
            debts_to_create = []
            for index, row in chunk.iterrows():
                debt = Debt(
                    name=row["name"],
                    governmentId=row["governmentId"],
                    email=row["email"],
                    debtAmount=row["debtAmount"],
                    debtDueDate=row["debtDueDate"],
                    debtId=row["debtId"],
                )
                debts_to_create.append(debt)

            Debt.objects.bulk_create(debts_to_create)
