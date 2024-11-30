from src.service import prepare_files as _
from src.parsing.Cyan import Cyan

if __name__ == '__main__':
    cyan_api = Cyan()
    offers = cyan_api.get_parsed_offers()
    cyan_api.dump_to_csv(offers=offers)
