from rapidfuzz import fuzz


class SearchEngine:
    def __init__(self, threshold):
        self.threshold = threshold


    def search(self, query, dataset):
        return [file_name for file_name in dataset if fuzz.partial_token_set_ratio(query, dataset[file_name]["image_text"] + dataset[file_name]["tags"]) >= self.threshold]
